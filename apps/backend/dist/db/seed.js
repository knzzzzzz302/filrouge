import { pool } from './pool.js';
async function seed() {
    await pool.query("INSERT INTO properties(reference, city, price, area_m2, status) VALUES ('AIX-001', 'Aix-en-Provence', 350000, 78, 'AVAILABLE') ON CONFLICT (reference) DO NOTHING");
    await pool.query("INSERT INTO properties(reference, city, price, area_m2, status) VALUES ('MAR-004', 'Marseille', 420000, 95, 'UNDER_OFFER') ON CONFLICT (reference) DO NOTHING");
    await pool.query("INSERT INTO properties(reference, city, price, area_m2, status) VALUES ('MTP-021', 'Montpellier', 295000, 68, 'AVAILABLE') ON CONFLICT (reference) DO NOTHING");
    await pool.query("INSERT INTO clients(first_name, last_name, email, budget_max) VALUES ('Lina', 'Durand', 'lina@client.fr', 450000) ON CONFLICT (email) DO NOTHING");
    console.log('Seed applied');
    await pool.end();
}
seed().catch(async (err) => {
    console.error(err);
    await pool.end();
    process.exit(1);
});
