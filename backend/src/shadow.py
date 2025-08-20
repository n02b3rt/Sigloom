from __future__ import annotations
import time, threading
from typing import Dict, Any, List

class DeviceShadow:
    def __init__(self, offline_after_sec: int = 60):
        self._lock = threading.RLock()
        self._by_id: Dict[str, Dict[str, Any]] = {}
        self._offline_after = offline_after_sec

    def upsert_state(self, device_id: str, payload: Dict[str, Any], retained: bool):
        now = int(time.time())
        ts = int(payload.get("ts") or now)
        with self._lock:
            cur = self._by_id.get(device_id, {})
            cur.update({
                "id": device_id,
                "online": True,
                "last_seen": ts,
                "app_ver": payload.get("app_ver") or payload.get("app") or cur.get("app_ver"),
                "rssi": payload.get("rssi", cur.get("rssi")),
                "source": "state_retained" if retained else "state_live",
                "updated_at": now,
            })
            self._by_id[device_id] = cur

    def apply_lwt(self, device_id: str, payload: Dict[str, Any], retained: bool):
        now = int(time.time())
        online = bool(payload.get("online", False))
        with self._lock:
            cur = self._by_id.get(device_id, {"id": device_id})
            cur.update({
                "online": online,
                "last_seen": int(payload.get("ts") or now),
                "source": "lwt_retained" if retained else "lwt_live",
                "updated_at": now,
            })
            self._by_id[device_id] = cur

    def sweep_timeouts(self):
        """Mark offline if there have been no heartbeats for offline_after."""
        cutoff = int(time.time()) - self._offline_after
        with self._lock:
            for d in self._by_id.values():
                if d.get("online") and int(d.get("last_seen", 0)) < cutoff:
                    d["online"] = False
                    d["source"] = "timeout"

    def list(self) -> List[Dict[str, Any]]:
        with self._lock:
            # you can sort, e.g. online first
            return sorted(self._by_id.values(), key=lambda x: (not x.get("online", False), x["id"]))
