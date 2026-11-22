from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

API_PREFIX = "/api/v1"


class HealthResponse(BaseModel):
    status: str


router = APIRouter(prefix=API_PREFIX)


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")


def create_app() -> FastAPI:
    app = FastAPI(title="JobTrack", openapi_url=f"{API_PREFIX}/openapi.json")
    app.include_router(router)
    return app


app = create_app()
