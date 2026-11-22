set windows-shell := ["bash", "-cu"]

default:
    @just --list

# Lance le backend (8000) et le frontend (5173) en parallèle (à lancer depuis Git Bash)
dev:
    (cd backend && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000) & (cd frontend && pnpm dev) & wait

test:
    cd backend && uv run pytest
    cd frontend && pnpm test

lint:
    cd backend && uv run ruff check . && uv run ruff format --check .
    cd frontend && pnpm lint

typecheck:
    cd backend && uv run mypy
    cd frontend && pnpm typecheck

build:
    cd frontend && pnpm build

# Régénère le schéma OpenAPI et les types TypeScript
gen-api:
    cd backend && uv run python -c "import json; from app.main import app; open('../frontend/openapi.json', 'w', encoding='utf-8').write(json.dumps(app.openapi(), indent=2, ensure_ascii=False) + '\n')"
    cd frontend && pnpm gen-api && pnpm exec prettier --write openapi.json

# Étape 2 (Docker)
up:
    @echo "Pas encore disponible : voir étape 2 (Docker)." && exit 1

# Étape 4 (base de données)
migrate:
    @echo "Pas encore disponible : voir étape 4 (SQLAlchemy / Alembic)." && exit 1

# Tout ce qui est requis avant un commit
check: lint typecheck test build
