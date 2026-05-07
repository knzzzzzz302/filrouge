import pg from 'pg';
const { Client } = pg;

const connectionString = process.env.DATABASE_URL || 'postgres://yplaza:yplaza@localhost:5432/yplaza';
const client = new Client({ connectionString });

async function run() {
  await client.connect();
  await client.query(`
    CREATE TABLE IF NOT EXISTS properties (
      id SERIAL PRIMARY KEY,
      reference TEXT NOT NULL UNIQUE,
      city TEXT NOT NULL,
      price NUMERIC NOT NULL,
      area_m2 NUMERIC NOT NULL,
      status TEXT NOT NULL DEFAULT 'AVAILABLE'
    );
  `);
  await client.query(`
    CREATE TABLE IF NOT EXISTS clients (
      id SERIAL PRIMARY KEY,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      budget_max NUMERIC NOT NULL DEFAULT 0
    );
  `);
  await client.query(`
    CREATE TABLE IF NOT EXISTS transactions (
      id SERIAL PRIMARY KEY,
      property_id INTEGER REFERENCES properties(id),
      amount NUMERIC NOT NULL,
      status TEXT NOT NULL DEFAULT 'OPEN'
    );
  `);
  console.log('Migrations applied');
  await client.end();
}

run().catch(async (err) => {
  console.error(err);
  await client.end();
  process.exit(1);
});
