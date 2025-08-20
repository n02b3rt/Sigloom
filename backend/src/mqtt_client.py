from __future__ import annotations
import json, threading, time, random, string, urllib.parse
from typing import Optional
import paho.mqtt.client as mqtt

from .settings import settings
from .shadow import DeviceShadow

_shadow = DeviceShadow(settings.shadow_offline_after_sec)
_client: Optional[mqtt.Client] = None
_stop = threading.Event()

def _rand_client_id(prefix="backend-"):
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}{suffix}"

def _parse_mqtt_url(url: str):
    # mqtt://user:pass@host:1883
    u = urllib.parse.urlparse(url)
    assert u.scheme in ("mqtt", "mqtts"), f"unsupported scheme: {u.scheme}"
    host = u.hostname or "localhost"
    port = u.port or (8883 if u.scheme == "mqtts" else 1883)
    username = urllib.parse.unquote(u.username) if u.username else None
    password = urllib.parse.unquote(u.password) if u.password else None
    tls = (u.scheme == "mqtts")
    return host, port, username, password, tls

def _on_connect(client, userdata, flags, reason_code, properties=None):
    # sub on state and lwt (retained will be applied immediately)
    client.subscribe("pico/+/state", qos=1)
    client.subscribe("pico/+/lwt", qos=1)

def _on_message(client, userdata, msg):
    try:
        topic = msg.topic  # e.g. pico/abcd1234/state
        parts = topic.split("/")
        if len(parts) < 3:  # unknown format
            return
        device_id = parts[1]
        kind = parts[2]
        payload = json.loads(msg.payload.decode("utf-8") or "{}")
        retained = bool(getattr(msg, "retain", False))

        if kind == "state":
            _shadow.upsert_state(device_id, payload, retained=retained)
        elif kind == "lwt":
            _shadow.apply_lwt(device_id, payload, retained=retained)
    except Exception:
        # deliberately without crash – add login in production
        pass

def _loop_thread(client: mqtt.Client):
    # in the background: paho loop + periodic sweep timeouts
    last_sweep = 0.0
    while not _stop.is_set():
        client.loop(timeout=1.0)
        now = time.time()
        if now - last_sweep >= settings.shadow_sweep_interval_sec:
            _shadow.sweep_timeouts()
            last_sweep = now

def start():
    global _client
    if _client is not None:
        return
    host, port, username, password, tls = _parse_mqtt_url(settings.mqtt_url)
    client_id = settings.mqtt_client_id or _rand_client_id()

    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id, clean_session=True)
    if username:
        c.username_pw_set(username, password)
    if tls:
        c.tls_set()  # default CA – we don't usually use mqtts in LAN

    c.on_connect = _on_connect
    c.on_message = _on_message
    c.connect(host, port, keepalive=60)

    t = threading.Thread(target=_loop_thread, args=(c,), name="mqtt-loop", daemon=True)
    t.start()
    _client = c

def stop():
    global _client
    _stop.set()
    try:
        if _client:
            _client.disconnect()
    finally:
        _client = None

def get_shadow() -> DeviceShadow:
    return _shadow
