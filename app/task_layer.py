from __future__ import annotations

from .models import Action, Observation, TaskState


class TaskLayer:
    """Mid-level intent tracker for mining/building tasks."""

    def __init__(self) -> None:
        self.state = TaskState()

    def update_goal(self, user_text: str) -> TaskState:
        text = user_text.lower()
        if "diamond" in text:
            self.state.high_level_goal = "mine_diamonds"
            self.state.target_block = "diamond_ore"
            self.state.build_mode = False
        elif "iron" in text:
            self.state.high_level_goal = "mine_iron"
            self.state.target_block = "iron_ore"
            self.state.build_mode = False
        elif "build" in text:
            self.state.high_level_goal = "build_structure"
            self.state.target_block = None
            self.state.build_mode = True
        elif "stop" in text:
            self.state.high_level_goal = "survive"
            self.state.target_block = None
            self.state.build_mode = False
        return self.state

    def choose_task_action(self, obs: Observation) -> Action | None:
        if self.state.high_level_goal == "mine_diamonds":
            if "underground" not in obs.context_tags:
                return Action("move_to_cave", "Need cave depth for diamond mining")
            return Action("scan_for_block", "Searching for diamond ore", {"block": "diamond_ore"})

        if self.state.high_level_goal == "mine_iron":
            return Action("scan_for_block", "Searching for iron ore", {"block": "iron_ore"})

        if self.state.build_mode:
            return Action("place_blueprint_block", "Continue building active blueprint")

        return None
