import { Router } from 'express';
import jwt from 'jsonwebtoken';
import { z } from 'zod';

const router = Router();
type Role = 'CLIENT' | 'COMMERCIAL' | 'AGENCY_MANAGER' | 'ADMIN';
type User = { email: string; password: string; role: Role };

const users: User[] = [
  { email: 'admin@yplaza.local', password: 'admin123', role: 'ADMIN' },
  { email: 'manager@yplaza.local', password: 'manager123', role: 'AGENCY_MANAGER' },
  { email: 'commercial@yplaza.local', password: 'commercial123', role: 'COMMERCIAL' },
];

router.post('/register', (req, res) => {
  const payload = z
    .object({
      email: z.string().email(),
      password: z.string().min(8),
    })
    .safeParse(req.body);
  if (!payload.success) {
    return res.status(400).json(payload.error.flatten());
  }

  const exists = users.some((item) => item.email === payload.data.email);
  if (exists) {
    return res.status(409).json({ message: 'Email already exists' });
  }

  users.push({ email: payload.data.email, password: payload.data.password, role: 'CLIENT' });
  return res.status(201).json({ message: 'Account created' });
});

router.post('/login', (req, res) => {
  const payload = z
    .object({
      email: z.string().email(),
      password: z.string().min(6),
    })
    .safeParse(req.body);
  if (!payload.success) {
    return res.status(400).json(payload.error.flatten());
  }
  const { email, password } = payload.data;
  const user = users.find((item) => item.email === email && item.password === password);
  if (!user) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }
  const token = jwt.sign({ sub: email, role: user.role }, process.env.JWT_SECRET ?? 'change-me', {
    expiresIn: '8h',
  });
  return res.json({ token, user: { email, role: user.role } });
});

router.get('/me', (_req, res) => {
  res.json({ email: 'admin@yplaza.local', role: 'ADMIN' });
});

export { router as authRouter };
