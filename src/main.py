"""FastAPI uygulamasını başlatır ve yapılandırır."""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.health_router import router as healthcheck_router
from src.api.routers.perspectra_router import router as perspectra_router
from src.core.logger import Logger

logger = Logger()
logger.init_log_worker(log_level=logging.DEBUG)


app = FastAPI(title="Perspectra API", version="1.0.0", docs_url="/swagger")

# CORS ayarları: Her yerden gelen isteklere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck_router)
app.include_router(perspectra_router)

if __name__ == "__main__":
    uvicorn.run(app, port=5000, host="0.0.0.0")
