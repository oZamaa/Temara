"""Serve the built single-page frontend, with a fallback to index.html."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, Response

from app.api_prefix import API_PREFIX

_NO_CACHE = {"Cache-Control": "no-cache"}
_IMMUTABLE = {"Cache-Control": "public, max-age=31536000, immutable"}


def mount_frontend(app: FastAPI, static_dir: Path) -> None:
    root = static_dir.resolve()
    index = root / "index.html"
    if not index.is_file():
        raise RuntimeError(f"Frontend build not found: {index}")

    @app.get("/{path:path}", include_in_schema=False)
    def serve_frontend(path: str) -> Response:
        # Unknown API routes must stay 404, never fall back to the SPA.
        if f"/{path}".startswith(f"{API_PREFIX}/") or f"/{path}" == API_PREFIX:
            return JSONResponse(
                {"error": {"code": "not_found", "message": "Ressource introuvable."}},
                status_code=404,
            )
        candidate = (root / path).resolve()
        if candidate.is_file() and candidate.is_relative_to(root):
            headers = _IMMUTABLE if candidate.is_relative_to(root / "assets") else _NO_CACHE
            return FileResponse(candidate, headers=headers)
        if Path(path).suffix:
            # A missing asset (e.g. /assets/old.js) is a real 404, not the SPA shell.
            raise HTTPException(status_code=404)
        return FileResponse(index, headers=_NO_CACHE)
