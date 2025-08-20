from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from . import mqtt_client

app = FastAPI(title="SigLoom Backend", version="0.1.0")

# CORS: na start allow-all; można zawęzić ENV-ami
if settings.api_cors_allow_all:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
elif settings.api_cors_allow_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_allow_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

MOCK_DEVICES = [
    {"id": "pico-01", "online": True, "app_ver": "1.0.0", "rssi": -55},
    {"id": "pico-02", "online": False, "app_ver": "1.0.0", "rssi": None},
]

@app.on_event("startup")
def _startup():
    mqtt_client.start()

@app.on_event("shutdown")
def _shutdown():
    mqtt_client.stop()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/devices")
def devices():
    return {"items": MOCK_DEVICES}
