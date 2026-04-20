from src.food import Food, FoodType
from src.element import Element


def test_food_creation():
    elem = Element(5, 5)
    food = Food(elem, FoodType.NORMAL)
    assert food.x == 5
    assert food.y == 5
    assert food.type == FoodType.NORMAL

    food2 = Food(elem, FoodType.SPEED)
    assert food2.type == FoodType.SPEED


def test_food_type_enum():
    assert FoodType.NORMAL.value == 1
    assert FoodType.SPEED.value == 2
    assert FoodType.SHRINK.value == 3