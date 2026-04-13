import pygame
from direction import Direction
from constants import *


class Infrastructure:
    """
    Инфраструктурный слой представляет собой методы для обращения к
    библиотеке PyGame.
    Только в этом файле import pygame.
    """

    def __init__(self):
        """
        Конструктор, создаёт экземпляр класса Infrastructure, отвечающий за
        связь логики
        и отображения. Запускает PyGame, инициализирует экран и часы
        """
        pygame.init()
        self.font = pygame.font.Font(None, SCALE)
        self.screen = pygame.display.set_mode([WIDTH * SCALE, HEIGHT * SCALE])
        self.clock = pygame.time.Clock()

        self._events = []

    def pump_events(self):
        self._events = pygame.event.get()

    def is_quit_event(self) -> bool:
        """
        Функция проверяет, нажал ли игрок крестик(закрыть окно)
        :return: True или False
        """
        return any(event.type == pygame.QUIT for event in self._events)

    def get_mouse_position(self) -> tuple[int, int]:
        return pygame.mouse.get_pos()

    def was_mouse_clicked(self, button: int = 1) -> bool:
        """Была ли нажата левая кнопка мыши в этом кадре"""
        return any(
            event.type == pygame.MOUSEBUTTONDOWN and event.button == button
            for event in self._events
        )

    def any_input_event(self) -> bool:
        """Любое нажатие клавиши или кнопки мыши"""
        return any(
            event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)
            for event in self._events
        )

    def get_pressed_key(self) -> Direction | None:
        """
        Проверяет, какая стрелка была нажата
        :return: соответствующий кнопке Direction или None
        """
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w]:
            return Direction.DOWN
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            return Direction.RIGHT
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            return Direction.UP
        if key[pygame.K_LEFT] or key[pygame.K_a]:
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
            self.screen,  # Где рисовать?
            pygame.Color(color),  # Какого цвета рисовать?
            (x * SCALE, y * SCALE, ELEMENT_SIZE, ELEMENT_SIZE),
            # Позиция и размер прямоугольника
            0,  # Толщина границы (0 = заливка)
            RADIUS,  # Радиус скругления углов
        )

    def draw_score(self, score: int):
        """
        Функция отображения счёта игры в углу экрана
        :param score: Количество очков
        :return:
        """
        self.screen.blit(  # Наклеивает созданную картинку с текстом на экран
            self.font.render(  # Создаёт текстовый объект
                f"Score: {score}",
                True,  # Сглаживание текста
                pygame.Color(SCORE_COLOR)),
            (5, 5)  # Координаты, где будет расположен текст
        )

    def draw_game_over(self):
        """
        Функция рисует большую красную надпись GAME OVER посередине экрана.
        :return:
        """
        message = self.font.render("GAME OVER", True,
                                   pygame.Color(GAME_OVER_COLOR))
        self.screen.blit(
            message,
            message.get_rect(
                center=((WIDTH // 2 * SCALE), (HEIGHT // 2 * SCALE)))
            # Помещает надпись в центр прямоугольника
        )

    def draw_centered_text(self, text: str, color: str, y: int = None,
                           font=None):
        """
        Универсальный метод для рисования текста по центру экрана.
        Используется в игре и в меню — дублирование убрано.
        """
        if font is None:
            font = self.font
        rendered = font.render(text, True, pygame.Color(color))
        if y is None:
            y = HEIGHT * SCALE // 2
        rect = rendered.get_rect(center=(WIDTH * SCALE // 2, y))
        self.screen.blit(rendered, rect)

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

    def draw_level_info(self, level_num: int, target: int):
        """Отображает текущий уровень и цель"""
        text = f"Уровень {level_num}  |  Цель: {target}"
        rendered = self.font.render(text, True, pygame.Color("white"))
        self.screen.blit(rendered, (5, 40))  # ниже счёта

    def draw_level_complete(self, level_num: int):
        """Сообщение о прохождении уровня"""
        if level_num < 3:
            message = self.font.render(f"Уровень {level_num} пройден!", True,
                                       pygame.Color("green"))
            # system.sleep(0.5)
        else:
            message = self.font.render("ИГРА ПРОЙДЕНА!", True,
                                       pygame.Color("green"))
        self.screen.blit(message, message.get_rect(
            center=(WIDTH * SCALE // 2, HEIGHT * SCALE // 2 - 50)))

    def draw_level_start_hint(self):
        """Рисует подсказку для начала движения"""
        self.draw_centered_text("Нажмите любую стрелку,", "white",
                                y=HEIGHT * SCALE // 2 + 50)
        self.draw_centered_text("чтобы начать движение", "white",
                                y=HEIGHT * SCALE // 2 + 80)
