import asyncio
import json
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse

from mavlink_web_bridge.telemetry import VesselPosition, VesselTelemetry

MAVLINK_CONNECTION = os.environ.get("MAVLINK_CONNECTION", "udp:127.0.0.1:14550")

telemetry = VesselTelemetry(MAVLINK_CONNECTION)


@asynccontextmanager
async def lifespan(app: FastAPI):
    telemetry.start()
    yield
    telemetry.stop()


app = FastAPI(title="mavlink-web-bridge", lifespan=lifespan)


def _serialize(position: VesselPosition) -> dict:
    return {
        "lat": position.lat,
        "lon": position.lon,
        "heading_deg": position.heading_deg,
        "timestamp": position.timestamp,
    }


@app.get("/vessel/position")
def get_position():
    position = telemetry.latest()
    if position is None:
        raise HTTPException(status_code=503, detail="No telemetry received yet")
    return _serialize(position)


@app.get("/vessel/position/stream")
async def stream_position(hz: float = Query(1.0, gt=0, le=20)):
    interval = 1 / hz

    async def event_generator():
        while True:
            position = telemetry.latest()
            if position is not None:
                yield f"data: {json.dumps(_serialize(position))}\n\n"
            await asyncio.sleep(interval)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
