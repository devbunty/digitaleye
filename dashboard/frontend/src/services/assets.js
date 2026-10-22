import { request } from "./http";

export const getAssets = () => request("/assets");
