from app.models import Observation
from app.reflex_layer import ReflexLayer
from app.task_layer import TaskLayer


def test_reflex_prioritizes_lava_escape():
    reflex = ReflexLayer(q_table_path="/tmp/reflex_test.json")
    obs = Observation(
        health=20,
        hunger=20,
        lava_distance=2.0,
        inventory_food=1,
        has_blocks=True,
    )
    action = reflex.choose_survival_action(obs)
    assert action is not None
    assert action.name == "pillar_up"


def test_task_goal_updates_from_chat():
    task = TaskLayer()
    state = task.update_goal("please mine diamond today")
    assert state.high_level_goal == "mine_diamonds"
    assert state.target_block == "diamond_ore"
