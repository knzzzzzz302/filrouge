import { FormEvent } from 'react';
import { Client, Kpis, Property, Transaction } from './types';

export function StatusMessages({ error, notice }: { error: string; notice: string }) {
  return (
    <>
      {error ? <p className="error">{error}</p> : null}
      {notice ? <p className="notice">{notice}</p> : null}
    </>
  );
}

export function Dashboard({
  kpis,
  popular,
  predictedPrice,
  onPredict,
}: {
  kpis: Kpis | null;
  popular: Array<{ reference: string; views: number }>;
  predictedPrice: number | null;
  onPredict: (event: FormEvent) => Promise<void>;
}) {
  return (
    <section>
      <h2>Dashboard</h2>
      {kpis ? (
        <p>Ventes: {kpis.salesCount} | Prix moyen: {kpis.averageSalePrice.toLocaleString()} EUR | Conversion: {(kpis.conversionRate * 100).toFixed(0)}%</p>
      ) : (
        <p>Connecte-toi pour charger les indicateurs.</p>
      )}
      <p>Biens populaires: {popular.map((p) => `${p.reference} (${p.views})`).join(', ') || 'n/a'}</p>
      <form onSubmit={onPredict}>
        <button type="submit">Lancer prediction prix type (80m2, 3 pieces)</button>
      </form>
      {predictedPrice ? <p>Prix predit: {predictedPrice.toLocaleString()} EUR</p> : null}
    </section>
  );
}

export function PropertyList({
  properties,
  onEdit,
  onDelete,
}: {
  properties: Property[];
  onEdit: (property: Property) => void;
  onDelete: (id: number) => void;
}) {
  if (!properties.length) {
    return <p>Aucun bien trouve pour ce filtre.</p>;
  }
  return (
    <ul>
      {properties.map((property) => (
        <li key={property.id}>
          <strong>{property.reference}</strong> - {property.city} - {Number(property.price).toLocaleString()} EUR - {property.status}
          <div className="actions">
            <button type="button" onClick={() => onEdit(property)}>Editer</button>
            <button type="button" onClick={() => onDelete(property.id)}>Supprimer</button>
          </div>
        </li>
      ))}
    </ul>
  );
}

export function ClientsList({ clients }: { clients: Client[] }) {
  if (!clients.length) return <p>Aucun client pour le moment.</p>;
  return <ul>{clients.map((c) => <li key={c.id}>{c.first_name} {c.last_name} - {c.email} - {Number(c.budget_max).toLocaleString()} EUR</li>)}</ul>;
}

export function TransactionsList({
  transactions,
  onStatusChange,
}: {
  transactions: Transaction[];
  onStatusChange: (id: number, status: Transaction['status']) => void;
}) {
  if (!transactions.length) return <p>Aucune transaction enregistree.</p>;
  return (
    <ul>
      {transactions.map((tx) => (
        <li key={tx.id}>
          TX#{tx.id} - Property:{tx.property_id} - {Number(tx.amount).toLocaleString()} EUR - {tx.status}
          <div className="actions">
            <button type="button" onClick={() => onStatusChange(tx.id, 'OPEN')}>OPEN</button>
            <button type="button" onClick={() => onStatusChange(tx.id, 'SIGNED')}>SIGNED</button>
            <button type="button" onClick={() => onStatusChange(tx.id, 'CANCELLED')}>CANCELLED</button>
          </div>
        </li>
      ))}
    </ul>
  );
}
