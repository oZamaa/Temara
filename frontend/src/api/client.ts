import type { paths } from "./schema";

type HealthResponse =
  paths["/api/v1/health"]["get"]["responses"]["200"]["content"]["application/json"];

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch("/api/v1/health");
  if (!response.ok) throw new Error(`health: HTTP ${response.status}`);
  return (await response.json()) as HealthResponse;
}
