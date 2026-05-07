import { Router } from 'express';
import { pool } from '../../db/pool.js';
import { requireAuth, requireRole } from '../../middleware/auth.js';
import { z } from 'zod';

const router = Router();
let fallbackNextTxId = 2;
const fallbackTransactions: Array<{ id: number; property_id: number; amount: number; status: 'OPEN' | 'SIGNED' | 'CANCELLED' }> = [
  { id: 1, property_id: 1, amount: 345000, status: 'OPEN' },
];
const txSchema = z.object({
  property_id: z.number().int().positive(),
  amount: z.number().positive(),
  status: z.enum(['OPEN', 'SIGNED', 'CANCELLED']).default('OPEN'),
});

router.get('/', requireAuth, async (_req, res) => {
  try {
    const result = await pool.query('SELECT id, property_id, amount, status FROM transactions ORDER BY id DESC LIMIT 100');
    return res.json(result.rows);
  } catch {
    return res.json(fallbackTransactions);
  }
});
router.post('/', requireAuth, requireRole(['COMMERCIAL', 'AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
  const body = txSchema.safeParse(req.body);
  if (!body.success) return res.status(400).json(body.error.flatten());
  const { property_id, amount, status } = body.data;
  try {
    const created = await pool.query(
      'INSERT INTO transactions(property_id, amount, status) VALUES ($1,$2,$3) RETURNING id, property_id, amount, status',
      [property_id, amount, status]
    );
    return res.status(201).json(created.rows[0]);
  } catch {
    const created = { id: fallbackNextTxId++, property_id, amount, status };
    fallbackTransactions.unshift(created);
    return res.status(201).json(created);
  }
});
router.patch('/:id/status', requireAuth, requireRole(['COMMERCIAL', 'AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
  const status = z.enum(['OPEN', 'SIGNED', 'CANCELLED']).safeParse(req.body.status);
  if (!status.success) return res.status(400).json({ message: 'Invalid status' });
  try {
    const updated = await pool.query(
      'UPDATE transactions SET status = $1 WHERE id = $2 RETURNING id, property_id, amount, status',
      [status.data, req.params.id]
    );
    if (!updated.rows[0]) return res.status(404).json({ message: 'Not found' });
    return res.json(updated.rows[0]);
  } catch {
    const id = Number(req.params.id);
    const target = fallbackTransactions.find((item) => item.id === id);
    if (!target) return res.status(404).json({ message: 'Not found' });
    target.status = status.data;
    return res.json(target);
  }
});

export { router as transactionsRouter };
