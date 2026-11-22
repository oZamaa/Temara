import { useQuery } from "@tanstack/react-query";

import { fetchHealth } from "@/api/client";
import { fr } from "@/i18n/fr";

export function HealthStatus() {
  const { data, isPending, isError } = useQuery({ queryKey: ["health"], queryFn: fetchHealth });

  if (isPending) return <p role="status">{fr.health.loading}</p>;
  if (isError || data.status !== "ok") return <p role="alert">{fr.health.error}</p>;
  return <p role="status">{fr.health.ok}</p>;
}
