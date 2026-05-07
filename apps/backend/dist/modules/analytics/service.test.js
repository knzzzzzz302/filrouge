import { describe, expect, it } from "vitest";
import { calculateKpis, popularProperties, predictPrice } from "./service.js";
describe("analytics service", () => {
    it("returns stable KPI keys", () => {
        const kpis = calculateKpis();
        expect(kpis.salesCount).toBeGreaterThan(0);
        expect(kpis.averageSalePrice).toBeGreaterThan(0);
        expect(kpis.conversionRate).toBeGreaterThan(0);
    });
    it("predicts price from features", () => {
        const value = predictPrice(80, 3, 1.1);
        expect(value).toBeGreaterThan(0);
    });
    it("returns popular properties sorted by views", () => {
        const popular = popularProperties();
        expect(popular.length).toBeGreaterThan(0);
        expect(popular[0].views).toBeGreaterThanOrEqual(popular[1].views);
    });
    it("increases prediction with stronger city factor", () => {
        const low = predictPrice(80, 3, 1);
        const high = predictPrice(80, 3, 1.2);
        expect(high).toBeGreaterThan(low);
    });
});
