import { SEVERITIES } from "../constants/severity";

/**
 * Turn the API's severity-by-host rows into one row per host.
 *
 * Input:  [{ name: "Critical", "web-01": 2, "db-01": 0 }, ...]
 * Output: [{ hostname: "web-01", Critical: 2, High: 0, ..., total: 2 }, ...]
 * sorted so the host with the most incidents comes first.
 */
export function buildRiskRanking(rowsBySeverity, hostNames) {
  if (!rowsBySeverity) return null;

  const bySeverity = Object.fromEntries(
    rowsBySeverity.map((row) => [row.name, row])
  );

  return hostNames
    .map((hostname) => {
      const counts = Object.fromEntries(
        SEVERITIES.map((severity) => [
          severity,
          bySeverity[severity]?.[hostname] ?? 0,
        ])
      );
      const total = SEVERITIES.reduce((sum, severity) => sum + counts[severity], 0);
      return { hostname, ...counts, total };
    })
    .sort((a, b) => b.total - a.total);
}
