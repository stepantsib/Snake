from enum import Enum
from constants import *

class Level(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class GameLevel:
    def __init__(self, level: Level):
        self.level = level
        self.target_score = self._get_target_score()
        self.obstacles = self._get_obstacles()
        self.start_time = None

    def _get_target_score(self):
        if self.level == Level.ONE:
            return LEVEL_1_TARGET
        elif self.level == Level.TWO:
            return LEVEL_2_TARGET
        else:
            return LEVEL_3_TARGET

    def _get_obstacles(self):
        if self.level == Level.ONE:
            return []
        elif self.level == Level.TWO:
            return OBSTACLES_LEVEL_2
        else:
            return OBSTACLES_LEVEL_3

    def is_obstacle(self, x: int, y: int) -> bool:
        return (x, y) in self.obstacles

    def get_level_name(self) -> str:
        return f"Уровень {self.level.value}"