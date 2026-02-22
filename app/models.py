from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ThreatType(str, Enum):
    MOB = "mob"
    LAVA = "lava"
    FALL = "fall"
    HUNGER = "hunger"


@dataclass
class Observation:
    health: int
    hunger: int
    is_on_fire: bool = False
    mob_distance: float | None = None
    mob_strength: int = 0
    lava_distance: float | None = None
    inventory_food: int = 0
    has_blocks: bool = False
    context_tags: set[str] = field(default_factory=set)


@dataclass
class Action:
    name: str
    reason: str
    payload: dict[str, str | int | float | bool] = field(default_factory=dict)


@dataclass
class TaskState:
    high_level_goal: str = "survive"
    target_block: str | None = None
    build_mode: bool = False


@dataclass
class ChatMessage:
    role: str
    content: str
