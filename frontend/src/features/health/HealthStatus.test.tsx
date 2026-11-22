import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";

import { fr } from "@/i18n/fr";
import { HealthStatus } from "./HealthStatus";

function renderWithClient() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <HealthStatus />
    </QueryClientProvider>,
  );
}

afterEach(() => vi.unstubAllGlobals());

test("affiche l'état opérationnel quand health répond ok", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json({ status: "ok" })));
  renderWithClient();
  expect(await screen.findByText(fr.health.ok)).toBeInTheDocument();
});

test("affiche une erreur quand le serveur est injoignable", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network")));
  renderWithClient();
  expect(await screen.findByRole("alert")).toHaveTextContent(fr.health.error);
});
