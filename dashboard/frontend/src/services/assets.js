<<<<<<< HEAD
import { request } from "./http";

export const getAssets = () => request("/assets");
=======
<<<<<<< HEAD
import { request } from "./http";

export const getAssets = () => request("/assets");
=======
import { apiUrl } from "../config";

export async function getAssets() {
  const response = await fetch(apiUrl("/assets"), { cache: "no-store" });

  if (!response.ok) {
    throw new Error("Failed to fetch assets");
  }

  return await response.json();
}

export async function getHosts() {
  const response = await fetch(apiUrl("/hosts"), { cache: "no-store" });

  if (!response.ok) {
    throw new Error("Failed to fetch hosts");
  }

  return await response.json();
}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
