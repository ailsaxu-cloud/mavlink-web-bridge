# mavlink-web-bridge

MAVLink-to-Web-API bridge for vessel position/heading.

Task: [SSAD-531](https://app.clickup.com/t/z91dg53kk9) — Build MAVLink-to-Web-API bridge for vessel position/heading

Connects to a vessel over MAVLink to read its coordinates (lat/lon) and heading,
then exposes that data as a web API for `gcs-server` to consume.

## Development steps

- [ ] Step 1: Set up `sim_vehicle.py` (ArduPilot SITL + MAVProxy daemon) to simulate the vessel
- [ ] Step 2: Build a FastAPI service exposing coordinates/heading via web API — at least 2 endpoints:
      one single-fetch endpoint, and one SSE endpoint that streams continuously with a
      user-adjustable push frequency
- [ ] Step 3: Create a Docker image to package the project; run it in Docker and expose the
      vessel's live coordinates/heading externally through the APIs from step 2
