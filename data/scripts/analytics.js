const fs = require('node:fs');

const rows = fs.readFileSync('data/sample/sales.clean.csv', 'utf8').trim().split('\n').slice(1)
  .map((line) => {
    const [reference, city, areaM2, rooms, price, views] = line.split(',');
    return { reference, city, areaM2: +areaM2, rooms: +rooms, price: +price, views: +views };
  });

const avg = rows.reduce((sum, r) => sum + r.price, 0) / rows.length;
const popular = [...rows].sort((a, b) => b.views - a.views).slice(0, 2);

console.log({ averagePrice: Math.round(avg), popular });
