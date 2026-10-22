/**
 * Base URL of the Digital Eye API.
 * Set VITE_API_URL (e.g. in .env.local) to point the dashboard at another host.
 */
export const API_URL = (
  import.meta.env.VITE_API_URL || "http://localhost:5000"
).replace(/\/$/, "");
