from __future__ import annotations

import json
from pathlib import Path

from .models import Action, Observation


class ReflexLayer:
    """Fast survival policy: hunger, danger, and emergency movement."""

    def __init__(self, q_table_path: str = "data/reflex_q_table.json") -> None:
        self.q_table_path = Path(q_table_path)
        self.q_table_path.parent.mkdir(parents=True, exist_ok=True)
        self.q_table = self._load_q_table()

    def _load_q_table(self) -> dict:
        if self.q_table_path.exists():
            return json.loads(self.q_table_path.read_text())
        return {}

    def save(self) -> None:
        self.q_table_path.write_text(json.dumps(self.q_table, indent=2))

    def choose_survival_action(self, obs: Observation) -> Action | None:
        if obs.lava_distance is not None and obs.lava_distance < 4.0:
            if obs.has_blocks:
                return Action("pillar_up", "Lava nearby: pillar up to avoid burn", {"height": 4})
            return Action("sprint_away", "Lava nearby: no blocks, run away")

        if obs.hunger <= 8 and obs.inventory_food > 0:
            return Action("eat_food", "Low hunger threshold reached")

        if obs.mob_distance is not None and obs.mob_distance < 4.0:
            if obs.health >= 12:
                return Action("attack", "Mob in close range and healthy", {"combo": 2})
            if obs.has_blocks:
                return Action("pillar_up", "Mob close while low health", {"height": 3})
            return Action("sprint_away", "Mob close and low health")

        if obs.is_on_fire:
            return Action("jump_and_strafe", "Extinguish and reposition")

        return None

    def update_from_feedback(self, state_key: str, action_name: str, reward: float) -> None:
        action_map = self.q_table.setdefault(state_key, {})
        prev = float(action_map.get(action_name, 0.0))
        action_map[action_name] = round(prev * 0.8 + reward * 0.2, 4)
        self.save()
