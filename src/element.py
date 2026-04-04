class Element:
    """
    Класс задаёт одну точку игрового поля
    x, y - координаты элемента внутри игрового поля
    0 <= x < WIDTH
    0 <= y < HEIGHT
    """

    def __init__(self, x: int, y: int):
        """
        Конструктор, инициализирует одну точку игрового поля
        :param x: координата x
        :param y: координата y
        """
        self.x = x
        self.y = y

    def __eq__(self, o) -> bool:
        """
        Метод, проверяющий равенство двух точек поля
        :param o: точка
        :return: True или False
        """
        return self.x == o.x and self.y == o.y
