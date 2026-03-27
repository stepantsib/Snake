import pygame
from direction import Direction
from constants import *


class Infrastructure:
    """
    Инфраструктурный слой представляет собой методы для обращения к библиотеке PyGame.
    Только в этом файле import pygame.
    """

    def __init__(self):
        """
        Конструктор, создаёт экземпляр класса Infrastructure, отвечающий за связь логики
        и отображения. Запускает PyGame, инициализирует экран и часы
        """
        pygame.init()
        self.font = pygame.font.Font(None, SCALE)
        self.screen = pygame.display.set_mode([WIDTH * SCALE, HEIGHT * SCALE])
        self.clock = pygame.time.Clock()

    def is_quit_event(self) -> bool:
        """
        Функция проверяет, нажал ли игрок крестик(закрыть окно)
        :return: True или False
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def get_pressed_key(self) -> Direction | None:
        """
        Проверяет, какая стрелка была нажата
        :return: соответствующий кнопке Direction или None
        """
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            return Direction.DOWN
        if key[pygame.K_RIGHT]:
            return Direction.RIGHT
        if key[pygame.K_DOWN]:
            return Direction.UP
        if key[pygame.K_LEFT]:
            return Direction.LEFT
        return None

    def fill_screen(self):
        """
        Функция заливает экран выбранным цветом
        :return:
        """
        self.screen.fill(SCREEN_COLOR)

    def draw_element(self, x, y, color):
        """
        Функция рисует одну клетку на экране
        :param x: координата X
        :param y: координата Y
        :param color: Цвет клетки
        :return:
        """
        pygame.draw.rect(
            self.screen,                                        # Где рисовать?
            pygame.Color(color),                                # Какого цвета рисовать?
            (x * SCALE, y * SCALE, ELEMENT_SIZE, ELEMENT_SIZE), # Позиция и размер прямоугольника
            0,                                                  # Толщина границы (0 = заливка)
            RADIUS,                                             # Радиус скругления углов
        )

    def draw_score(self, score: int):
        """
        Функция отображения счёта игры в углу экрана
        :param score: Количество очков
        :return:
        """
        self.screen.blit(                    # Наклеивает созданную картинку с текстом на экран
            self.font.render(                # Создаёт текстовый объект
                f"Score: {score}",
                True,                        # Сглаживание текста
                pygame.Color(SCORE_COLOR)),
                (5, 5)                       # Координаты, где будет расположен текст
        )

    def draw_game_over(self):
        """
        Функция рисует большую красную надпись GAME OVER посередине экрана.
        :return:
        """
        message = self.font.render("GAME OVER", True, pygame.Color(GAME_OVER_COLOR))
        self.screen.blit(
            message,
            message.get_rect(center=((WIDTH // 2 * SCALE), (HEIGHT // 2 * SCALE))) # Помещает надпись в центр прямоугольника
        )

    def update_and_tick(self):
        """
        Функция обновляет экран и показывает всё, что нарисовали.
        :return:
        """
        pygame.display.update()
        self.clock.tick(FPS)

    def quit(self):
        """
        Функция завершает работу pygame
        :return:
        """
        pygame.quit()