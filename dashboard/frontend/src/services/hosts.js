import { request } from "./http";

export const getHosts = () => request("/hosts");

export const createDemoHost = ({ hostname, ip, os, kernel }) =>
  request("/hosts/demo", { method: "POST", body: { hostname, ip, os, kernel } });

export const deleteHost = (hostname) =>
  request(`/hosts/${encodeURIComponent(hostname)}`, { method: "DELETE" });
