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

### 1. Start SITL + MAVProxy (Step 1)

`sim_vehicle.py` is ArduPilot's own official launcher (in
`ardupilot/Tools/autotest/sim_vehicle.py`), not something written for this
project. It needs a persistent terminal (MAVProxy exits immediately if its
stdin hits EOF), so run it inside a detached `tmux` session:

```bash
cd ardupilot
tmux new-session -d -s vessel_sitl \
  "source ../ardupilot-venv/bin/activate && \
   python3 Tools/autotest/sim_vehicle.py -v Rover -f motorboat -N -w \
     --out=127.0.0.1:14551 \
     2>&1 | tee /tmp/sim_vehicle.log"
```

- `-v Rover -f motorboat`: simulate a motorboat (ArduPilot's closest "vessel" frame)
- `-N`: don't rebuild (skip if you changed ArduPilot source)
- `-w`: wipe EEPROM / start from clean params
- `--out=127.0.0.1:14551`: an **extra** MAVLink UDP output, on top of the
  default `127.0.0.1:14550`. Useful so a second consumer (e.g. QGroundControl,
  or the sniffer tool below) can listen without fighting this project's
  FastAPI service for the same port — only one process can bind a given UDP
  port at a time.

This creates two tmux windows: window `0` runs MAVProxy (the relay/console —
this is where the interactive `MAV>`/`MANUAL>` prompt lives), window `1` runs
the actual `ardurover` SITL binary. They're wired together by `sim_vehicle.py`
itself; don't try to restart just one — killing window 0 auto-kills window 1
(and killing window 1 alone leaves window 0 stuck retrying a dead link). To
restart cleanly:

```bash
tmux kill-session -t vessel_sitl   # tears down both windows
# then re-run the tmux new-session command above
```

Attach to watch/interact with MAVProxy (detach again with `Ctrl+B` then `D` —
do **not** Ctrl+C or exit, that kills the sim):

```bash
tmux attach -t vessel_sitl:0
```

Sanity-check the MAVLink feed without any of this project's code, using the
standalone sniffer at `~/Work/tools/mavlink_sniffer.py` (see its own README
for the full list of categories):

```bash
uv run /Users/ailsaxu/Work/tools/mavlink_sniffer.py --connection udp:127.0.0.1:14550 --show heartbeat --show position
```

### 2. Start the FastAPI service (Step 2)

```bash
uv run uvicorn mavlink_web_bridge.main:app --port 8000
```

- `GET /vessel/position` — latest lat/lon/heading as JSON
- `GET /vessel/position/stream?hz=2` — Server-Sent Events stream, `hz` sets the push rate
