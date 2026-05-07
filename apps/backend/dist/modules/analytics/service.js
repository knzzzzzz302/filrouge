export function calculateKpis() {
    return {
        salesCount: 42,
        averageSalePrice: 289000,
        conversionRate: 0.37,
    };
}
export function popularProperties() {
    return [
        { reference: 'AIX-001', views: 180 },
        { reference: 'LYO-013', views: 152 },
    ];
}
export function predictPrice(areaM2, rooms, cityFactor) {
    const base = 2800;
    return Math.round(areaM2 * base * cityFactor + rooms * 9000);
}
