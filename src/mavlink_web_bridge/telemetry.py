import threading
import time
from dataclasses import dataclass

from pymavlink import mavutil


@dataclass
class VesselPosition:
    lat: float
    lon: float
    heading_deg: float
    timestamp: float


class VesselTelemetry:
    """Reads GLOBAL_POSITION_INT off a MAVLink connection in a background
    thread and keeps the latest reading available for the API layer."""

    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._lock = threading.Lock()
        self._latest: VesselPosition | None = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2)

    def latest(self) -> VesselPosition | None:
        with self._lock:
            return self._latest

    def _run(self) -> None:
        conn = mavutil.mavlink_connection(self._connection_string)
        conn.wait_heartbeat()
        while not self._stop.is_set():
            msg = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout=1)
            if msg is None:
                continue
            with self._lock:
                self._latest = VesselPosition(
                    lat=msg.lat / 1e7,
                    lon=msg.lon / 1e7,
                    heading_deg=msg.hdg / 100,
                    timestamp=time.time(),
                )
