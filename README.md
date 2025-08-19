# Sigloom

*A small, local panel for monitoring and simply managing my Raspberry Pi Pico W devices. Online/offline status, simple commands, and quick config swaps — all on the LAN.*

## The problem I'm solving

* Maintaining several **Raspberry Pi Pico W** boards is tedious: manual fixes over USB and no quick view of whether devices are "alive".
* There's no **central place** to send simple commands (e.g., restart) and replace small config files.
* I want to work **locally** (Windows → Docker Compose) and eventually **deploy on a Pi 5** next to Home Assistant — without running around with a USB cable.

**Status:** Concept / MVP (in progress)

**Sigloom** is my conceptual manager for a small home fleet of **Raspberry Pi Pico W (MicroPython)**. I want to make device management easier (status, simple operations, remote tweaks). The scope will evolve as I go.

---

## Stack (for now)

* **Backend:** FastAPI
* **Frontend:** Next.js
* **Communication:** MQTT (Mosquitto)
* **Orchestration:** Docker Compose

---

## Quick start (local)

```powershell
docker compose -f ops/compose-min.yml up -d --build
# Backend:  http://localhost:8080/health
# Frontend: http://localhost:3000
```

> Note: this is a skeleton for further development — I'll add functionality iteratively.

---

## License

**Apache-2.0** (see `LICENSE`).
