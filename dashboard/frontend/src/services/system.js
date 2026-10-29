import { API_URL } from "../config";
import { request } from "./http";

export { API_URL };

/** Name, version and route list reported by the API root. */
export const getApiInfo = () => request("/");
