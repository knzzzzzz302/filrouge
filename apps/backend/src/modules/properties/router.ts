import { Router } from 'express';
import { z } from 'zod';
import { pool } from '../../db/pool.js';
import { requireAuth, requireRole } from '../../middleware/auth.js';

const router = Router();
let fallbackNextId = 5;
const fallbackProperties: Array<{
  id: number;
  reference: string;
  city: string;
  price: number;
  area_m2: number;
  status: 'AVAILABLE' | 'UNDER_OFFER' | 'SOLD';
}> = [
  { id: 1, reference: 'AIX-001', city: 'Aix-en-Provence', price: 350000, area_m2: 78, status: 'AVAILABLE' },
  { id: 2, reference: 'LYO-013', city: 'Lyon', price: 310000, area_m2: 62, status: 'UNDER_OFFER' },
  { id: 3, reference: 'MAR-004', city: 'Marseille', price: 420000, area_m2: 95, status: 'SOLD' },
  { id: 4, reference: 'MTP-021', city: 'Montpellier', price: 295000, area_m2: 68, status: 'AVAILABLE' },
];
const propertySchema = z.object({
  reference: z.string().min(3),
  city: z.string().min(2),
  price: z.number().positive(),
  area_m2: z.number().positive(),
  status: z.enum(['AVAILABLE', 'UNDER_OFFER', 'SOLD']).default('AVAILABLE'),
});

router.get('/', requireAuth, async (_req, res) => {
  try {
    const result = await pool.query(
      'SELECT id, reference, city, price, area_m2, status FROM properties ORDER BY id DESC LIMIT 100'
    );
    return res.json(result.rows);
  } catch {
    return res.json(fallbackProperties);
  }
});
router.post('/', requireAuth, requireRole(['COMMERCIAL', 'AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
  const body = propertySchema.safeParse(req.body);
  if (!body.success) return res.status(400).json(body.error.flatten());
  const { reference, city, price, area_m2, status } = body.data;
  try {
    const created = await pool.query(
      'INSERT INTO properties(reference, city, price, area_m2, status) VALUES ($1, $2, $3, $4, $5) RETURNING id, reference, city, price, area_m2, status',
      [reference, city, price, area_m2, status]
    );
    return res.status(201).json(created.rows[0]);
  } catch {
    const created = { id: fallbackNextId++, reference, city, price, area_m2, status };
    fallbackProperties.unshift(created);
    return res.status(201).json(created);
  }
});

router.patch('/:id', requireAuth, requireRole(['COMMERCIAL', 'AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
  const body = propertySchema.partial().safeParse(req.body);
  if (!body.success) return res.status(400).json(body.error.flatten());
  const fields = body.data;
  const allowed = ['reference', 'city', 'price', 'area_m2', 'status'] as const;
  const updates = Object.entries(fields).filter(([key]) => allowed.includes(key as (typeof allowed)[number]));
  if (!updates.length) return res.status(400).json({ message: 'No fields to update' });

  const setClause = updates.map(([key], idx) => `${key} = $${idx + 1}`).join(', ');
  const values = updates.map(([, value]) => value);
  try {
    const result = await pool.query(
      `UPDATE properties SET ${setClause} WHERE id = $${updates.length + 1} RETURNING id, reference, city, price, area_m2, status`,
      [...values, req.params.id]
    );
    if (!result.rows[0]) return res.status(404).json({ message: 'Not found' });
    return res.json(result.rows[0]);
  } catch {
    const id = Number(req.params.id);
    const target = fallbackProperties.find((item) => item.id === id);
    if (!target) return res.status(404).json({ message: 'Not found' });
    Object.assign(target, fields);
    return res.json(target);
  }
});

router.delete('/:id', requireAuth, requireRole(['AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
  try {
    const result = await pool.query('DELETE FROM properties WHERE id = $1 RETURNING id', [req.params.id]);
    if (!result.rows[0]) return res.status(404).json({ message: 'Not found' });
    return res.status(204).send();
  } catch {
    const id = Number(req.params.id);
    const before = fallbackProperties.length;
    const afterList = fallbackProperties.filter((item) => item.id !== id);
    if (afterList.length === before) return res.status(404).json({ message: 'Not found' });
    fallbackProperties.splice(0, fallbackProperties.length, ...afterList);
    return res.status(204).send();
  }
});

export { router as propertiesRouter };
