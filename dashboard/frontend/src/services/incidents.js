import { request } from "./http";

export const getIncidents = ({ status = null, hostname = null } = {}) =>
  request("/incidents", { params: { status, hostname } });
