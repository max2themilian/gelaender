from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.content import router as content_router
from app.routes.orders import router as orders_router
from app.routes.products import router as products_router
from app.routes.tour import router as tour_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "gelaender-api"}


app.include_router(products_router)
app.include_router(tour_router)
app.include_router(content_router)
app.include_router(orders_router)
