const fs = require('node:fs');

const input = 'data/sample/sales.csv';
const output = 'data/sample/sales.clean.csv';

const lines = fs.readFileSync(input, 'utf8').trim().split('\n');
const [header, ...rows] = lines;
const cleaned = rows
  .map((line) => line.replace(/\s+/g, ''))
  .filter((line) => line.split(',').length === 6);

fs.writeFileSync(output, [header, ...cleaned].join('\n'));
console.log(`cleaned rows: ${cleaned.length}`);
