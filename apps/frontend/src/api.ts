const API = 'http://localhost:4000/api';

export async function apiRequest<T>(
  path: string,
  token: string,
  init?: RequestInit,
  requiresAuth = true
): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (init?.headers && !Array.isArray(init.headers) && !(init.headers instanceof Headers)) {
    Object.assign(headers, init.headers);
  }
  if (requiresAuth && token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API}${path}`, { ...init, headers });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || `HTTP ${res.status}`);
  }
  if (res.status === 204) return {} as T;
  return (await res.json()) as T;
}

export { API };
