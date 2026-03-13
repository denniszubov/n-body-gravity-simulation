from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import CreateRequest, StepRequest, SimState, PresetInfo
from app.sim_service import SimService, PRESETS

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI()
service = SimService()


@app.get("/api/presets")
def get_presets() -> list[PresetInfo]:
    return list(PRESETS.values())


@app.post("/api/sim/create")
def create_sim(req: CreateRequest) -> SimState:
    try:
        return service.create(req.preset, n_bodies=req.n_bodies, seed=req.seed)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/sim/step")
def step_sim(req: StepRequest) -> SimState:
    try:
        return service.step(req.dt, req.n_steps)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/sim/state")
def get_state() -> SimState:
    try:
        return service.state()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
