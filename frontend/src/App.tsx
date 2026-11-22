import { HealthStatus } from "@/features/health/HealthStatus";
import { fr } from "@/i18n/fr";

export function App() {
  return (
    <main className="mx-auto max-w-xl p-8">
      <h1 className="text-3xl font-bold">{fr.app.name}</h1>
      <HealthStatus />
    </main>
  );
}
