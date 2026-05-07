import { FormEvent, useEffect, useMemo, useState } from 'react';
import { Link, Navigate, Route, Routes, useNavigate } from 'react-router-dom';
import { API } from './api';

function Header() {
  const hasToken = Boolean(localStorage.getItem('yplaza_token'));
  return (
    <header className="nav">
      <div className="brand">Y-Plaza</div>
      <nav>
        <Link to="/">Accueil</Link>
        {hasToken ? <Link to="/hub">Hub</Link> : null}
        <Link to="/inscription">Inscription</Link>
        <Link to="/connexion">Connexion</Link>
      </nav>
    </header>
  );
}

function LandingPage() {
  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Immobilier nouvelle generation</p>
        <h1>Achetez et vendez plus intelligemment.</h1>
        <p className="subtitle">
          Une plateforme moderne pour centraliser vos operations immobilieres,
          analyser le marche et accelerer vos decisions.
        </p>
        <div className="heroActions">
          <Link className="btn primary" to="/inscription">Commencer</Link>
          <Link className="btn ghost" to="/connexion">J'ai deja un compte</Link>
        </div>
      </section>
    </main>
  );
}

function SignupPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError('');
    setSuccess('');
    if (password !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas.');
      return;
    }
    try {
      const res = await fetch(`${API}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const payload = await res.json().catch(() => ({}));
        throw new Error(payload.message ?? 'Inscription impossible');
      }
      const loginRes = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!loginRes.ok) throw new Error('Compte cree mais connexion automatique impossible');
      const loginPayload = (await loginRes.json()) as { token: string };
      localStorage.setItem('yplaza_token', loginPayload.token);
      setSuccess('Compte cree. Redirection vers votre hub...');
      setTimeout(() => navigate('/hub'), 500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    }
  }

  return (
    <main className="page">
      <section className="card authCard">
        <h2>Creer un compte</h2>
        <p className="muted">Inscrivez-vous pour acceder a la plateforme Y-Plaza.</p>
        <form className="authForm" onSubmit={onSubmit}>
          <input type="email" placeholder="Email professionnel" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <input type="password" placeholder="Mot de passe (8+ caracteres)" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <input type="password" placeholder="Confirmer le mot de passe" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          <button className="btn primary" type="submit">S'inscrire</button>
        </form>
        {error ? <p className="error">{error}</p> : null}
        {success ? <p className="success">{success}</p> : null}
      </section>
    </main>
  );
}

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@yplaza.local');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const [connected, setConnected] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError('');
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        throw new Error('Identifiants invalides');
      }
      const payload = (await res.json()) as { token: string };
      localStorage.setItem('yplaza_token', payload.token);
      setConnected(true);
      setTimeout(() => navigate('/hub'), 350);
    } catch (err) {
      setConnected(false);
      setError(err instanceof Error ? err.message : 'Connexion impossible');
    }
  }

  return (
    <main className="page">
      <section className="card authCard">
        <h2>Connexion</h2>
        <p className="muted">Connectez-vous pour acceder a votre espace.</p>
        <form className="authForm" onSubmit={onSubmit}>
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <input type="password" placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <button className="btn primary" type="submit">Se connecter</button>
        </form>
        {error ? <p className="error">{error}</p> : null}
        {connected ? <p className="success">Connexion reussie. Token sauvegarde localement.</p> : null}
      </section>
    </main>
  );
}

function HubPage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [searchingMarket, setSearchingMarket] = useState(false);
  const [error, setError] = useState('');
  const [marketError, setMarketError] = useState('');
  const [kpis, setKpis] = useState<{ salesCount: number; averageSalePrice: number; conversionRate: number } | null>(null);
  const [properties, setProperties] = useState<
    Array<{ id: number; reference: string; city: string; price: number; area_m2: number; status: string }>
  >([]);
  const [marketListings, setMarketListings] = useState<
    Array<{
      id: string;
      title: string;
      city: string;
      postalCode: string;
      surfaceM2: number;
      estimatedPrice: number;
      source: string;
    }>
  >([]);
  const token = localStorage.getItem('yplaza_token');
  if (!token) {
    return <Navigate to="/connexion" replace />;
  }

  useEffect(() => {
    let cancelled = false;
    async function loadHubData() {
      setLoading(true);
      setError('');
      try {
        const [kpiRes, propRes] = await Promise.all([
          fetch(`${API}/analytics/kpis`),
          fetch(`${API}/properties`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);
        if (!kpiRes.ok || !propRes.ok) {
          throw new Error('Impossible de charger les donnees live');
        }
        const kpiData = (await kpiRes.json()) as { salesCount: number; averageSalePrice: number; conversionRate: number };
        const propertyData = (await propRes.json()) as Array<{
          id: number;
          reference: string;
          city: string;
          price: number;
          area_m2: number;
          status: string;
        }>;
        if (!cancelled) {
          setKpis(kpiData);
          setProperties(propertyData);
        }
      } catch {
        if (!cancelled) {
          setError('API indisponible. Verifiez que le backend tourne sur le port 4000.');
          setKpis({ salesCount: 42, averageSalePrice: 289000, conversionRate: 0.37 });
          setProperties([
            { id: 1, reference: 'AIX-001', city: 'Aix-en-Provence', price: 350000, area_m2: 78, status: 'AVAILABLE' },
            { id: 2, reference: 'LYO-013', city: 'Lyon', price: 310000, area_m2: 62, status: 'UNDER_OFFER' },
            { id: 3, reference: 'MAR-004', city: 'Marseille', price: 420000, area_m2: 95, status: 'SOLD' },
            { id: 4, reference: 'MTP-021', city: 'Montpellier', price: 295000, area_m2: 68, status: 'AVAILABLE' },
          ]);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    loadHubData();
    return () => {
      cancelled = true;
    };
  }, [token]);

  useEffect(() => {
    let cancelled = false;
    async function loadIRLResults() {
      if (query.trim().length < 2) {
        setMarketListings([]);
        setMarketError('');
        return;
      }
      setSearchingMarket(true);
      setMarketError('');
      try {
        const res = await fetch(`${API}/market/search?q=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error();
        const payload = (await res.json()) as Array<{
          id: string;
          title: string;
          city: string;
          postalCode: string;
          surfaceM2: number;
          estimatedPrice: number;
          source: string;
        }>;
        if (!cancelled) setMarketListings(payload);
      } catch {
        if (!cancelled) {
          setMarketError("Recherche IRL indisponible temporairement.");
          setMarketListings([]);
        }
      } finally {
        if (!cancelled) setSearchingMarket(false);
      }
    }
    const timer = setTimeout(loadIRLResults, 280);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [query]);

  const filteredProperties = useMemo(() => {
    return properties.filter((item) => {
      const blob = `${item.reference} ${item.city} ${item.status}`.toLowerCase();
      return blob.includes(query.toLowerCase());
    });
  }, [properties, query]);

  return (
    <main className="page">
      <section className="card hubCard">
        <p className="eyebrow">Hub Y-Plaza</p>
        <h2>Plateforme immobilier operationnelle</h2>
        <p className="muted">Consultez les indicateurs et pilotez les annonces depuis un seul espace.</p>
        <div className="kpiGrid">
          <article className="kpiCard">
            <p className="kpiLabel">Ventes</p>
            <h3>{kpis?.salesCount ?? '-'}</h3>
          </article>
          <article className="kpiCard">
            <p className="kpiLabel">Prix moyen</p>
            <h3>{kpis ? `${kpis.averageSalePrice.toLocaleString()} EUR` : '-'}</h3>
          </article>
          <article className="kpiCard">
            <p className="kpiLabel">Conversion</p>
            <h3>{kpis ? `${(kpis.conversionRate * 100).toFixed(0)}%` : '-'}</h3>
          </article>
        </div>
        <div className="hubToolbar">
          <input
            className="hubSearch"
            placeholder="Rechercher une annonce (ville, reference, statut)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div className="heroActions">
            <Link className="btn ghost" to="/">Retour accueil</Link>
            <button
              className="btn primary"
              type="button"
              onClick={() => {
                localStorage.removeItem('yplaza_token');
                navigate('/connexion');
              }}
            >
              Se deconnecter
            </button>
          </div>
        </div>
        {error ? <p className="error">{error}</p> : null}
        {loading ? <p className="muted">Chargement des annonces...</p> : null}
        <div className="listingGrid">
          {filteredProperties.map((item) => (
            <article className="listingCard" key={item.id}>
              <p className="listingRef">{item.reference}</p>
              <h4>{item.city}</h4>
              <p>{Number(item.area_m2).toLocaleString()} m2</p>
              <p className="listingPrice">{Number(item.price).toLocaleString()} EUR</p>
              <span className="badge">{item.status}</span>
            </article>
          ))}
          {!loading && !filteredProperties.length ? <p className="muted">Aucune annonce trouvee.</p> : null}
        </div>

        <h3 className="sectionTitle">Annonces IRL (open data)</h3>
        {searchingMarket ? <p className="muted">Recherche en cours...</p> : null}
        {marketError ? <p className="error">{marketError}</p> : null}
        <div className="listingGrid">
          {marketListings.map((item) => (
            <article className="listingCard" key={item.id}>
              <p className="listingRef">{item.title}</p>
              <h4>
                {item.city} ({item.postalCode})
              </h4>
              <p>{item.surfaceM2} m2 (estime)</p>
              <p className="listingPrice">{item.estimatedPrice.toLocaleString()} EUR</p>
              <div className="metaRow">
                <span className="badge badgeNeutral">Estimation marche</span>
                <span className="badge badgeInfo">
                  {item.source.includes('geo.api.gouv.fr') ? 'Confiance: elevee' : 'Confiance: moyenne'}
                </span>
              </div>
            </article>
          ))}
          {!searchingMarket && query.trim().length >= 2 && !marketListings.length ? (
            <p className="muted">Aucun resultat IRL pour cette recherche.</p>
          ) : null}
        </div>
      </section>
    </main>
  );
}

export function App() {
  return (
    <div className="siteShell">
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/inscription" element={<SignupPage />} />
        <Route path="/connexion" element={<LoginPage />} />
        <Route path="/hub" element={<HubPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
