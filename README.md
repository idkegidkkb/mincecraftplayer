# mincecraftplayer

A layered Minecraft control app with:

1. **Reflex layer** (fast survival): eat food, fight/escape mobs, avoid lava, pillar up.
2. **Task layer** (mid-level objective): parse user intent like mining diamonds/iron or building.
3. **Planner layer** (Gemini): turns chat into compact step plans and instructs other layers.

It includes a web chat interface and a runtime loop that controls a Minecraft adapter.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Gemini setup (optional)

```bash
export GEMINI_API_KEY=your_key_here
```

Without a key, the planner falls back to a local rule-based plan string.

## Important integration note

The current project ships with `MockMinecraftAdapter` for safe local testing.
To control a real game through your screen/client, replace `app/adapters.py` with an adapter that:

- Captures game frames (OpenCV/mss).
- Detects mobs/blocks/hunger/lava from HUD and world.
- Sends keyboard/mouse actions to Minecraft.

The orchestration layer is already wired for that adapter contract.

## Tests

```bash
pytest
```
