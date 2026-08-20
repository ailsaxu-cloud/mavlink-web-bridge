# mavlink-web-bridge

A standalone learning project to practice ArduPilot, MAVLink, and FastAPI —
not tied to `gcs-server` or any other Marlin service.

Goal: simulate a vessel with ArduPilot SITL, read its position/heading over
MAVLink, expose that data through a self-contained FastAPI server, and package
the whole thing as a Docker image so a browser can call the API running
inside the container.

## Development steps

- [x] Step 1: Set up `sim_vehicle.py` (ArduPilot SITL + MAVProxy daemon) to simulate the vessel
- [ ] Step 2: Build a FastAPI service exposing coordinates/heading via web API — at least 2 endpoints:
      one single-fetch endpoint, and one SSE endpoint that streams continuously with a
      user-adjustable push frequency
- [ ] Step 3: Create a Docker image to package the project; run it in Docker and expose the
      vessel's live coordinates/heading externally through the APIs from step 2
