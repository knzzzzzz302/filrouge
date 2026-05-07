import request from 'supertest';
import { describe, expect, it } from 'vitest';
import { app } from './app.js';
describe('api integration', () => {
    it('returns health status', async () => {
        const response = await request(app).get('/health');
        expect(response.status).toBe(200);
        expect(response.body.status).toBe('ok');
    });
    it('rejects protected route without token', async () => {
        const response = await request(app).get('/api/properties');
        expect(response.status).toBe(401);
    });
    it('authenticates demo admin account', async () => {
        const response = await request(app)
            .post('/api/auth/login')
            .send({ email: 'admin@yplaza.local', password: 'admin123' });
        expect(response.status).toBe(200);
        expect(response.body.token).toBeTypeOf('string');
    });
    it('returns 404 on unknown routes', async () => {
        const response = await request(app).get('/api/unknown');
        expect(response.status).toBe(404);
    });
});
