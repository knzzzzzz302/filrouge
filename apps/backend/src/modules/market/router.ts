import { Router } from 'express';
import { z } from 'zod';

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

router.get('/images', async (req, res) => {
  const query = String(req.query.q ?? '').trim();
  if (query.length < 2) {
    return res.json([]);
  }

  try {
    const url = `https://api.openverse.org/v1/images/?q=${encodeURIComponent(
      `real estate ${query} house apartment`
    )}&license_type=commercial,modification&filter_dead=true&page_size=12`;

    const response = await fetch(url, {
      headers: {
        'User-Agent': 'y-plaza/1.0 (student project)',
      },
    });
    if (!response.ok) {
      return res.status(503).json({ message: 'Openverse unavailable' });
    }
    const payload = (await response.json()) as {
      results?: Array<{
        id: string;
        title?: string;
        thumbnail?: string;
        url?: string;
        creator?: string;
        source?: string;
        license?: string;
      }>;
    };

    const images = (payload.results ?? [])
      .filter((item) => item.thumbnail || item.url)
      .slice(0, 10)
      .map((item, index) => ({
        id: item.id || `img-${index}`,
        title: item.title || `Photo immobiliere ${index + 1}`,
        imageUrl: item.thumbnail || item.url,
        author: item.creator || 'Unknown',
        license: item.license || 'CC',
        source: item.source || 'Openverse',
      }));

    return res.json(images);
  } catch {
    return res.status(503).json({ message: 'IRL images API unavailable' });
  }
});

const estimateSchema = z.object({
  city: z.string().min(2),
  postalCode: z.string().min(4).max(6).optional(),
  areaM2: z.number().positive(),
  rooms: z.number().int().positive().max(12),
  propertyType: z.enum(['APARTMENT', 'HOUSE', 'PRO']).default('APARTMENT'),
  condition: z.enum(['TO_RENOVATE', 'GOOD', 'EXCELLENT']).default('GOOD'),
  energyClass: z.enum(['A', 'B', 'C', 'D', 'E', 'F', 'G']).default('D'),
  distanceToCenterKm: z.number().nonnegative().max(80).default(5),
});

router.post('/estimate', async (req, res) => {
  const parsed = estimateSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json(parsed.error.flatten());
  }

  const data = parsed.data;
  const locationSeed = (data.city + (data.postalCode ?? '00000'))
    .split('')
    .reduce((acc, char) => acc + char.charCodeAt(0), 0);

  const locationFactor = 0.9 + (locationSeed % 45) / 100;
  const typeFactor = data.propertyType === 'HOUSE' ? 1.12 : data.propertyType === 'PRO' ? 1.22 : 1;
  const conditionFactor =
    data.condition === 'EXCELLENT' ? 1.08 : data.condition === 'GOOD' ? 1 : 0.87;
  const energyFactor =
    data.energyClass === 'A'
      ? 1.08
      : data.energyClass === 'B'
      ? 1.05
      : data.energyClass === 'C'
      ? 1.02
      : data.energyClass === 'D'
      ? 1
      : data.energyClass === 'E'
      ? 0.94
      : data.energyClass === 'F'
      ? 0.89
      : 0.84;
  const distanceFactor = Math.max(0.75, 1 - data.distanceToCenterKm * 0.015);

  const basePerM2 = 2800;
  const roomsBoost = data.rooms * 8500;
  const estimateRaw =
    data.areaM2 * basePerM2 * locationFactor * typeFactor * conditionFactor * energyFactor * distanceFactor +
    roomsBoost;
  const estimatedValue = Math.round(estimateRaw);

  const lowRange = Math.round(estimatedValue * 0.92);
  const highRange = Math.round(estimatedValue * 1.08);
  const confidenceScore = Math.max(62, Math.min(91, Math.round(88 - data.distanceToCenterKm * 0.6)));

  const suggestions: string[] = [];
  if (data.condition === 'TO_RENOVATE') {
    suggestions.push('Une renovation cuisine/salle d eau peut augmenter la valeur de 8 a 15%.');
  }
  if (['F', 'G', 'E'].includes(data.energyClass)) {
    suggestions.push('Un gain de classe energetique ameliore la valorisation et la vitesse de vente.');
  }
  if (data.distanceToCenterKm > 12) {
    suggestions.push('Mettez en avant transports et commodites pour compenser l eloignement du centre.');
  }
  if (suggestions.length === 0) {
    suggestions.push('Le bien est bien positionne: optimisez les photos et le home staging pour maximiser les offres.');
  }

  return res.json({
    estimatedValue,
    lowRange,
    highRange,
    confidenceScore,
    model: 'Y-Plaza Assisted Valuation v1',
    assumptions: {
      locationFactor,
      typeFactor,
      conditionFactor,
      energyFactor,
      distanceFactor,
    },
    suggestions,
  });
});

export { router as marketRouter };
