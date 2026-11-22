# JobTrack

Application web de suivi de candidatures : tableau Kanban, fiche détaillée par candidature et statistiques.

Auto-hébergée, gratuite et 100 % open source. Les données restent chez vous (SQLite), sans service externe ni télémétrie : l'application fonctionne hors ligne.

> **Statut : en développement.** Rien n'est encore utilisable.

## Fonctionnalités prévues

- Kanban à colonnes, glisser-déposer (souris, tactile, clavier)
- Fiche détaillée avec historique, notes, tags, contacts, entretiens
- Statistiques et relances
- Import / export CSV
- Thèmes clair et sombre
- Multi-utilisateurs avec deux rôles (`admin` et `user`) : chacun ne voit que ses propres données

## Stack

- **Backend** : Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, SQLite
- **Frontend** : React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, dnd-kit, TanStack Query, Recharts
- **Livraison** : une seule image Docker

## Lancement prévu

```bash
docker compose up -d
```

L'application sera alors disponible sur `http://127.0.0.1:8000`. Au premier lancement, un écran permet de créer le compte administrateur. Les données sont stockées dans le volume `/data`.

## Principes de sécurité

- Pas d'inscription publique : seuls les administrateurs créent des comptes.
- Mots de passe hachés avec argon2id, 12 caractères minimum.
- Sessions côté serveur, cookie `HttpOnly` et `SameSite=Strict`, protection CSRF.
- Verrouillage temporaire après des échecs de connexion répétés.
- Isolation stricte des données entre utilisateurs, y compris pour les administrateurs.
- Conteneur non-root, système de fichiers en lecture seule, capacités Linux supprimées.
- Aucune ressource externe (pas de CDN, pas de télémétrie).

Pour signaler une vulnérabilité, voir [SECURITY.md](SECURITY.md).

## Licence

[MIT](LICENSE)
