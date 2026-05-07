import { Router } from 'express';
import { pool } from '../../db/pool.js';
import { requireAuth, requireRole } from '../../middleware/auth.js';
import { z } from 'zod';
const router = Router();
let fallbackNextClientId = 2;
const fallbackClients = [
    { id: 1, first_name: 'Lina', last_name: 'Durand', email: 'lina@client.fr', budget_max: 450000 },
];
const clientSchema = z.object({
    first_name: z.string().min(1),
    last_name: z.string().min(1),
    email: z.string().email(),
    budget_max: z.number().nonnegative(),
});
router.get('/', requireAuth, async (_req, res) => {
    try {
        const result = await pool.query('SELECT id, first_name, last_name, email, budget_max FROM clients ORDER BY id DESC LIMIT 100');
        return res.json(result.rows);
    }
    catch {
        return res.json(fallbackClients);
    }
});
router.post('/', requireAuth, requireRole(['COMMERCIAL', 'AGENCY_MANAGER', 'ADMIN']), async (req, res) => {
    const body = clientSchema.safeParse(req.body);
    if (!body.success)
        return res.status(400).json(body.error.flatten());
    try {
        const created = await pool.query('INSERT INTO clients(first_name, last_name, email, budget_max) VALUES ($1,$2,$3,$4) RETURNING id, first_name, last_name, email, budget_max', [body.data.first_name, body.data.last_name, body.data.email, body.data.budget_max]);
        return res.status(201).json(created.rows[0]);
    }
    catch {
        const created = { id: fallbackNextClientId++, ...body.data };
        fallbackClients.unshift(created);
        return res.status(201).json(created);
    }
});
export { router as clientsRouter };
