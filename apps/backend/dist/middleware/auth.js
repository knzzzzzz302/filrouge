import jwt from 'jsonwebtoken';
export function requireAuth(req, res, next) {
    const auth = req.headers.authorization;
    if (!auth?.startsWith('Bearer ')) {
        return res.status(401).json({ message: 'Missing token' });
    }
    try {
        const token = auth.slice(7);
        req.user = jwt.verify(token, process.env.JWT_SECRET ?? 'change-me');
        return next();
    }
    catch {
        return res.status(401).json({ message: 'Invalid token' });
    }
}
export function requireRole(roles) {
    return (req, res, next) => {
        if (!req.user || !roles.includes(req.user.role)) {
            return res.status(403).json({ message: 'Forbidden' });
        }
        return next();
    };
}
