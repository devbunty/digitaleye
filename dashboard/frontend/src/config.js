/**
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
 * Base URL of the Digital Eye API.
 * Set VITE_API_URL (e.g. in .env.local) to point the dashboard at another host.
 */
export const API_URL = (
  import.meta.env.VITE_API_URL || "http://localhost:5000"
).replace(/\/$/, "");
<<<<<<< HEAD
=======
=======
 * Central API base URL. Override with VITE_API_URL when deploying
 * against a different collector/backend host.
 */
export const API_URL =
  import.meta.env.VITE_API_URL || "http://192.168.175.195:5000";

export function apiUrl(path = "") {
  const base = API_URL.replace(/\/$/, "");
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${base}${suffix}`;
}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
