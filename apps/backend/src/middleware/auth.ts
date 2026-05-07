import { NextFunction, Request, Response } from 'express';
import jwt from 'jsonwebtoken';

type Role = 'CLIENT' | 'COMMERCIAL' | 'AGENCY_MANAGER' | 'ADMIN';

export interface AuthRequest extends Request {
  user?: { sub: string; role: Role };
}

export function requireAuth(req: AuthRequest, res: Response, next: NextFunction) {
  const auth = req.headers.authorization;
  if (!auth?.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Missing token' });
  }
  try {
    const token = auth.slice(7);
    req.user = jwt.verify(token, process.env.JWT_SECRET ?? 'change-me') as {
      sub: string;
      role: Role;
    };
    return next();
  } catch {
    return res.status(401).json({ message: 'Invalid token' });
  }
}

export function requireRole(roles: Role[]) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ message: 'Forbidden' });
    }
    return next();
  };
}
