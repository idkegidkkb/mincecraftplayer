from __future__ import annotations

from .adapters import MinecraftAdapter
from .models import Action, ChatMessage
from .planner_layer import PlannerLayer
from .reflex_layer import ReflexLayer
from .task_layer import TaskLayer


class LayeredMinecraftAgent:
    def __init__(
        self,
        adapter: MinecraftAdapter,
        reflex: ReflexLayer,
        task: TaskLayer,
        planner: PlannerLayer,
    ) -> None:
        self.adapter = adapter
        self.reflex = reflex
        self.task = task
        self.planner = planner
        self.chat_history: list[ChatMessage] = []

    async def tick(self) -> Action:
        obs = await self.adapter.read_observation()

        reflex_action = self.reflex.choose_survival_action(obs)
        if reflex_action is not None:
            await self.adapter.execute(reflex_action)
            return reflex_action

        task_action = self.task.choose_task_action(obs)
        if task_action is None:
            task_action = Action("patrol", "No immediate objective, patrol area")

        await self.adapter.execute(task_action)
        return task_action

    async def handle_chat(self, text: str) -> dict[str, str]:
        self.chat_history.append(ChatMessage(role="user", content=text))
        state = self.task.update_goal(text)
        status = f"goal={state.high_level_goal}, target={state.target_block or 'none'}"
        plan = await self.planner.plan(self.chat_history, status)
        self.chat_history.append(ChatMessage(role="assistant", content=plan))
        return {"goal": state.high_level_goal, "plan": plan}
