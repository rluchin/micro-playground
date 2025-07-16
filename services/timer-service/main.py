from fastapi import FastAPI
from datetime import datetime, timezone
import asyncio

app = FastAPI(title="Timer Service")
state = {}
lock = asyncio.Lock()

def now():
    return datetime.now(tz=timezone.utc)

@app.post("/timer/start")
async def start():
    async with lock:
        state["start"] = now()
        state.pop("stop", None)
    return {"status": "started", "started_at": state["start"]}

@app.post("/timer/stop")
async def stop():
    async with lock:
        state["stop"] = now()
    return {"status": "stopped", "stopped_at": state["stop"]}

@app.get("/timer")
async def current():
    if "start" not in state:
        return {"elapsed": 0}
    end = state.get("stop") or now()
    return {"elapsed": (end - state['start']).total_seconds()}

