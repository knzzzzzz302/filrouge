export type Property = {
  id: number;
  reference: string;
  city: string;
  price: number;
  area_m2: number;
  status: string;
};

export type Client = {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  budget_max: number;
};

export type Transaction = {
  id: number;
  property_id: number;
  amount: number;
  status: 'OPEN' | 'SIGNED' | 'CANCELLED';
};

export type Kpis = {
  salesCount: number;
  averageSalePrice: number;
  conversionRate: number;
};
