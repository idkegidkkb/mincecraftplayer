from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .adapters import MockMinecraftAdapter
from .orchestrator import LayeredMinecraftAgent
from .planner_layer import PlannerLayer
from .reflex_layer import ReflexLayer
from .task_layer import TaskLayer


class Runtime:
    def __init__(self) -> None:
        self.agent = LayeredMinecraftAgent(
            adapter=MockMinecraftAdapter(),
            reflex=ReflexLayer(),
            task=TaskLayer(),
            planner=PlannerLayer(),
        )
        self.running = True
        self.last_action = "idle"

    async def run_loop(self) -> None:
        while self.running:
            action = await self.agent.tick()
            self.last_action = f"{action.name}: {action.reason}"
            await asyncio.sleep(1.0)


runtime = Runtime()
templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(runtime.run_loop())
    try:
        yield
    finally:
        runtime.running = False
        await task


app = FastAPI(title="Layered Minecraft Player", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": {}})


@app.websocket("/ws")
async def ws_chat(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_json({"type": "status", "message": "Connected to layered Minecraft agent."})
    while True:
        data = await websocket.receive_json()
        user_text = str(data.get("message", ""))
        result = await runtime.agent.handle_chat(user_text)
        await websocket.send_json(
            {
                "type": "chat",
                "user": user_text,
                "goal": result["goal"],
                "plan": result["plan"],
                "last_action": runtime.last_action,
            }
        )
