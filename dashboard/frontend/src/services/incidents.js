<<<<<<< HEAD
import { request } from "./http";

export const getIncidents = ({ status = null, hostname = null } = {}) =>
  request("/incidents", { params: { status, hostname } });
=======
import { apiUrl } from "../config";

export async function getIncidents({ status = null, hostname = null } = {}) {
  const params = new URLSearchParams();

  if (status) params.set("status", status);
  if (hostname) params.set("hostname", hostname);

  const query = params.toString();
  const url = apiUrl(query ? `/incidents?${query}` : "/incidents");

  const response = await fetch(url, { cache: "no-store" });

  if (!response.ok) {
    throw new Error("Failed to fetch incidents");
  }

  return await response.json();
}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
