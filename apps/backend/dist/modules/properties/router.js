import { Router } from 'express';
import { z } from 'zod';
import { pool } from '../../db/pool.js';
import { requireAuth, requireRole } from '../../middleware/auth.js';
const router = Router();
let fallbackNextId = 13;
const fallbackProperties = [
    { id: 1, reference: 'AIX-001', city: 'Aix-en-Provence', price: 350000, area_m2: 78, status: 'AVAILABLE' },
    { id: 2, reference: 'LYO-013', city: 'Lyon', price: 310000, area_m2: 62, status: 'UNDER_OFFER' },
    { id: 3, reference: 'MAR-004', city: 'Marseille', price: 420000, area_m2: 95, status: 'SOLD' },
    { id: 4, reference: 'MTP-021', city: 'Montpellier', price: 295000, area_m2: 68, status: 'AVAILABLE' },
    { id: 5, reference: 'PAR-101', city: 'Paris', price: 689000, area_m2: 54, status: 'UNDER_OFFER' },
    { id: 6, reference: 'NAN-020', city: 'Nantes', price: 298000, area_m2: 70, status: 'AVAILABLE' },
    { id: 7, reference: 'TLS-033', city: 'Toulouse', price: 332000, area_m2: 76, status: 'AVAILABLE' },
    { id: 8, reference: 'NIC-014', city: 'Nice', price: 515000, area_m2: 66, status: 'UNDER_OFFER' },
    { id: 9, reference: 'BDX-019', city: 'Bordeaux', price: 389000, area_m2: 82, status: 'AVAILABLE' },
    { id: 10, reference: 'LIL-011', city: 'Lille', price: 271000, area_m2: 64, status: 'SOLD' },
    { id: 11, reference: 'REN-026', city: 'Rennes', price: 318000, area_m2: 73, status: 'AVAILABLE' },
    { id: 12, reference: 'STR-017', city: 'Strasbourg', price: 342000, area_m2: 71, status: 'UNDER_OFFER' },
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
        const result = await pool.query('SELECT id, reference, city, price, area_m2, status FROM properties ORDER BY id DESC LIMIT 100');
        return res.json(result.rows);
    }
    catch {
        return res.json(fallbackProperties);
    }
});
router.post('/', requireAuth, requireRole(['COMMERCIAL', 'AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
    const body = propertySchema.safeParse(req.body);
    if (!body.success)
        return res.status(400).json(body.error.flatten());
    const { reference, city, price, area_m2, status } = body.data;
    try {
        const created = await pool.query('INSERT INTO properties(reference, city, price, area_m2, status) VALUES ($1, $2, $3, $4, $5) RETURNING id, reference, city, price, area_m2, status', [reference, city, price, area_m2, status]);
        return res.status(201).json(created.rows[0]);
    }
    catch {
        const created = { id: fallbackNextId++, reference, city, price, area_m2, status };
        fallbackProperties.unshift(created);
        return res.status(201).json(created);
    }
});
router.patch('/:id', requireAuth, requireRole(['COMMERCIAL', 'AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
    const body = propertySchema.partial().safeParse(req.body);
    if (!body.success)
        return res.status(400).json(body.error.flatten());
    const fields = body.data;
    const allowed = ['reference', 'city', 'price', 'area_m2', 'status'];
    const updates = Object.entries(fields).filter(([key]) => allowed.includes(key));
    if (!updates.length)
        return res.status(400).json({ message: 'No fields to update' });
    const setClause = updates.map(([key], idx) => `${key} = $${idx + 1}`).join(', ');
    const values = updates.map(([, value]) => value);
    try {
        const result = await pool.query(`UPDATE properties SET ${setClause} WHERE id = $${updates.length + 1} RETURNING id, reference, city, price, area_m2, status`, [...values, req.params.id]);
        if (!result.rows[0])
            return res.status(404).json({ message: 'Not found' });
        return res.json(result.rows[0]);
    }
    catch {
        const id = Number(req.params.id);
        const target = fallbackProperties.find((item) => item.id === id);
        if (!target)
            return res.status(404).json({ message: 'Not found' });
        Object.assign(target, fields);
        return res.json(target);
    }
});
router.delete('/:id', requireAuth, requireRole(['AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
    try {
        const result = await pool.query('DELETE FROM properties WHERE id = $1 RETURNING id', [req.params.id]);
        if (!result.rows[0])
            return res.status(404).json({ message: 'Not found' });
        return res.status(204).send();
    }
    catch {
        const id = Number(req.params.id);
        const before = fallbackProperties.length;
        const afterList = fallbackProperties.filter((item) => item.id !== id);
        if (afterList.length === before)
            return res.status(404).json({ message: 'Not found' });
        fallbackProperties.splice(0, fallbackProperties.length, ...afterList);
        return res.status(204).send();
    }
});
export { router as propertiesRouter };
