import { API_URL } from "../config";

/**
 * Thin wrapper around fetch for the Digital Eye API.
 *
 * - `params` entries that are null/undefined/"" are dropped from the query string
 * - `body` is sent as JSON
 * - non-2xx responses throw an Error carrying the server's `error` message
 */
export async function request(path, { method = "GET", params, body } = {}) {
  const query = new URLSearchParams(
    Object.entries(params ?? {}).filter(
      ([, value]) => value !== null && value !== undefined && value !== ""
    )
  ).toString();

  const response = await fetch(`${API_URL}${path}${query ? `?${query}` : ""}`, {
    method,
    cache: "no-store",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.error || `Request failed (${response.status})`);
  }

  return data;
}
