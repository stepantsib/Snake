from src.level import GameLevel, Level
from src.constants import OBSTACLES_LEVEL_2, OBSTACLES_LEVEL_3


def test_level_targets():
    assert GameLevel(Level.ONE).target_score == 20
    assert GameLevel(Level.TWO).target_score == 25
    assert GameLevel(Level.THREE).target_score == 25


def test_obstacles():
    lvl2 = GameLevel(Level.TWO)
    assert len(lvl2.obstacles) == len(OBSTACLES_LEVEL_2)
    assert lvl2.is_obstacle(6, 4) is True
    assert lvl2.is_obstacle(0, 0) is False

    lvl3 = GameLevel(Level.THREE)
    assert len(lvl3.obstacles) == len(OBSTACLES_LEVEL_3)
    assert lvl3.is_obstacle(18, 12) is True