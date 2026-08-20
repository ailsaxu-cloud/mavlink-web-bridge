# mavlink-web-bridge

A standalone learning project to practice ArduPilot, MAVLink, and FastAPI —
not tied to `gcs-server` or any other Marlin service.

Goal: simulate a vessel with ArduPilot SITL, read its position/heading over
MAVLink, expose that data through a self-contained FastAPI server, and package
the whole thing as a Docker image so a browser can call the API running
inside the container.

## Development steps

- [x] Step 1: Set up `sim_vehicle.py` (ArduPilot SITL + MAVProxy daemon) to simulate the vessel
- [x] Step 2: Build a FastAPI service exposing coordinates/heading via web API — at least 2 endpoints:
      one single-fetch endpoint, and one SSE endpoint that streams continuously with a
      user-adjustable push frequency
- [ ] Step 3: Create a Docker image to package the project; run it in Docker and expose the
      vessel's live coordinates/heading externally through the APIs from step 2

## Running

Step 1 must already be running (SITL + MAVProxy broadcasting on UDP 14550 —
see `ardupilot-venv` and `sim_vehicle.py -v Rover -f motorboat`).

```bash
uv run uvicorn mavlink_web_bridge.main:app --port 8000
```

- `GET /vessel/position` — latest lat/lon/heading as JSON
- `GET /vessel/position/stream?hz=2` — Server-Sent Events stream, `hz` sets the push rate
