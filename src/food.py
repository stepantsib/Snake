from enum import Enum
from element import Element


class FoodType(Enum):
    NORMAL = 1
    SPEED = 2
    SHRINK = 3


class Food:
    def __init__(self, element: Element, food_type: FoodType):
        self.element = element
        self.type = food_type

    @property
    def x(self):
        return self.element.x

    @property
    def y(self):
        return self.element.y