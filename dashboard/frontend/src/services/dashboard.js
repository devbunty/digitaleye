import { request } from "./http";

export const getDashboardSummary = () => request("/dashboard/summary");
export const getHostResources = () => request("/dashboard/resources");
export const getThreatFeed = () => request("/dashboard/threat-feed");
export const getThreatIntelligence = () => request("/dashboard/threat-intelligence");
export const getTopMitre = () => request("/dashboard/top-mitre");
