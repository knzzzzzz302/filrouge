import { Router } from 'express';
import { calculateKpis, popularProperties, predictPrice } from './service.js';
const router = Router();
router.get('/kpis', (_req, res) => res.json(calculateKpis()));
router.get('/popular-properties', (_req, res) => res.json(popularProperties()));
router.post('/predict-price', (req, res) => {
    const { areaM2, rooms, cityFactor } = req.body;
    res.json({ predictedPrice: predictPrice(areaM2, rooms, cityFactor ?? 1) });
});
export { router as analyticsRouter };
