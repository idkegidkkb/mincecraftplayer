from __future__ import annotations

import os

from .models import ChatMessage

try:
    import google.generativeai as genai
except ImportError:  # Optional at runtime if not installed yet
    genai = None


class PlannerLayer:
    """LLM planning layer; routes user chat to Gemini and emits compact instructions."""

    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        self.model_name = model_name
        self.enabled = False
        self._model = None

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and genai is not None:
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(model_name)
            self.enabled = True

    async def plan(self, messages: list[ChatMessage], status_summary: str) -> str:
        if not self.enabled:
            latest = messages[-1].content if messages else ""
            return f"Fallback planner: convert '{latest}' into safe Minecraft steps considering {status_summary}."

        history = "\n".join([f"{m.role}: {m.content}" for m in messages[-6:]])
        prompt = (
            "You are a Minecraft planner. Return 2-5 concrete steps only. "
            "Prioritize survival first, then progress.\n"
            f"Status: {status_summary}\nChat:\n{history}"
        )
        resp = self._model.generate_content(prompt)
        return (resp.text or "No plan returned.").strip()
