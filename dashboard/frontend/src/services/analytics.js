import { request } from "./http";

export const getAnalytics = ({ hostname = null, hours = 72 } = {}) =>
  request("/analytics", { params: { hostname, hours } });
