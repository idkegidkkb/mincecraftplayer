from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Action, Observation


class MinecraftAdapter(ABC):
    @abstractmethod
    async def read_observation(self) -> Observation:
        """Read game state from screen vision, game API, or simulator."""

    @abstractmethod
    async def execute(self, action: Action) -> None:
        """Execute a low-level control action in Minecraft."""


class MockMinecraftAdapter(MinecraftAdapter):
    """A safe adapter for development without attaching to a real Minecraft client."""

    def __init__(self) -> None:
        self.tick = 0

    async def read_observation(self) -> Observation:
        self.tick += 1
        hunger = 7 if self.tick % 3 == 0 else 16
        mob_distance = 3.0 if self.tick % 5 == 0 else None
        lava_distance = 2.5 if self.tick % 7 == 0 else None
        return Observation(
            health=15,
            hunger=hunger,
            mob_distance=mob_distance,
            mob_strength=3,
            lava_distance=lava_distance,
            inventory_food=2,
            has_blocks=True,
            context_tags={"mining", "underground"},
        )

    async def execute(self, action: Action) -> None:
        # Replace with key/mouse controls for your Minecraft client.
        print(f"[MOCK EXECUTE] {action.name} -> {action.reason} ({action.payload})")
