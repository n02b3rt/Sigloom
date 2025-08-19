
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pico OTA Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_DEVICES = [
    {"id": "pico-01", "online": True, "app_ver": "1.0.0", "rssi": -55},
    {"id": "pico-02", "online": False, "app_ver": "1.0.0", "rssi": None},
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/devices")
def devices():
    return {"items": MOCK_DEVICES}
