from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from app.api_prefix import API_PREFIX
from app.config import Settings, get_settings
from app.static import mount_frontend


class HealthResponse(BaseModel):
    status: str


router = APIRouter(prefix=API_PREFIX)


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="JobTrack", openapi_url=f"{API_PREFIX}/openapi.json")
    app.include_router(router)
    if settings.static_dir is not None:
        # Registered last: the catch-all route must not shadow API routes.
        mount_frontend(app, settings.static_dir)
    return app


app = create_app()
