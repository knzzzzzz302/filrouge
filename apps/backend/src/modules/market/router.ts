import { Router } from 'express';

const router = Router();

type CommuneResult = {
  nom: string;
  code: string;
  population?: number;
  codesPostaux?: string[];
  centre?: { coordinates: [number, number] };
};

type AddressResult = {
  properties?: {
    city?: string;
    postcode?: string;
    label?: string;
  };
  geometry?: { coordinates: [number, number] };
};

function estimatedPriceBase(city: string, postalCode: string): number {
  const seed = `${city}-${postalCode}`.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  return 180000 + (seed % 220000);
}

router.get('/search', async (req, res) => {
  const query = String(req.query.q ?? '').trim();
  if (query.length < 2) {
    return res.json([]);
  }

  try {
    const communeUrl = `https://geo.api.gouv.fr/communes?nom=${encodeURIComponent(
      query
    )}&fields=nom,code,codesPostaux,population,centre&boost=population&limit=6`;
    const addressUrl = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&limit=6`;

    const [communeRes, addressRes] = await Promise.all([fetch(communeUrl), fetch(addressUrl)]);
    const communes = (await communeRes.json()) as CommuneResult[];
    const addressesPayload = (await addressRes.json()) as { features?: AddressResult[] };
    const addresses = addressesPayload.features ?? [];

    const communeListings = communes.map((item, index) => {
      const postalCode = item.codesPostaux?.[0] ?? '00000';
      const base = estimatedPriceBase(item.nom, postalCode);
      return {
        id: `commune-${item.code}-${index}`,
        title: `Bien potentiel a ${item.nom}`,
        city: item.nom,
        postalCode,
        surfaceM2: 45 + (index * 12) % 90,
        estimatedPrice: base,
        lat: item.centre?.coordinates?.[1] ?? null,
        lon: item.centre?.coordinates?.[0] ?? null,
        source: 'geo.api.gouv.fr',
      };
    });

    const addressListings = addresses.slice(0, 4).map((feature, index) => {
      const city = feature.properties?.city ?? query;
      const postalCode = feature.properties?.postcode ?? '00000';
      const base = estimatedPriceBase(city, postalCode);
      return {
        id: `address-${postalCode}-${index}`,
        title: feature.properties?.label ?? `Annonce locale ${index + 1}`,
        city,
        postalCode,
        surfaceM2: 35 + (index * 18) % 85,
        estimatedPrice: base + index * 12000,
        lat: feature.geometry?.coordinates?.[1] ?? null,
        lon: feature.geometry?.coordinates?.[0] ?? null,
        source: 'api-adresse.data.gouv.fr',
      };
    });

    const merged = [...communeListings, ...addressListings].slice(0, 8);
    return res.json(merged);
  } catch {
    return res.status(503).json({ message: 'IRL market API unavailable' });
  }
});

export { router as marketRouter };
