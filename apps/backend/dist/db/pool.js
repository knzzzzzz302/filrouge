import pg from 'pg';
const { Pool } = pg;
const connectionString = process.env.DATABASE_URL ?? 'postgres://yplaza:yplaza@localhost:5432/yplaza';
export const pool = new Pool({ connectionString });
