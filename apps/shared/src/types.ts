export type UserRole = 'CLIENT' | 'COMMERCIAL' | 'AGENCY_MANAGER' | 'ADMIN';

export interface Property {
  id: string;
  reference: string;
  city: string;
  price: number;
  areaM2: number;
  status: 'AVAILABLE' | 'UNDER_OFFER' | 'SOLD';
}
