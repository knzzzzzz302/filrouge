import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import { authRouter } from './modules/auth/router.js';
import { propertiesRouter } from './modules/properties/router.js';
import { clientsRouter } from './modules/clients/router.js';
import { transactionsRouter } from './modules/transactions/router.js';
import { analyticsRouter } from './modules/analytics/router.js';
import { marketRouter } from './modules/market/router.js';

export const app = express();
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use((req, _res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

app.get('/health', (_req, res) => res.json({ status: 'ok' }));
app.use('/api/auth', authRouter);
app.use('/api/properties', propertiesRouter);
app.use('/api/clients', clientsRouter);
app.use('/api/transactions', transactionsRouter);
app.use('/api/analytics', analyticsRouter);
app.use('/api/market', marketRouter);
app.use((_req, res) => {
  res.status(404).json({ message: 'Route not found' });
});
app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error(err);
  res.status(500).json({ message: 'Internal server error' });
});
