import pygame
from src.direction import Direction
from src.constants import *
from src.food import FoodType


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
        pygame.mixer.init()

        self.font = pygame.font.Font(None, SCALE)
        self.screen = pygame.display.set_mode([WIDTH * SCALE, HEIGHT * SCALE])
        self.clock = pygame.time.Clock()

        self._events = []

        self.sounds = {}
        self.sfx_enabled = True
        try:
            self.sounds['eat_normal'] = pygame.mixer.Sound("sounds/red "
                                                           "apple.mp3")
            self.sounds['eat_speed'] = pygame.mixer.Sound("sounds/cyan "
                                                          "apple.mp3")
            self.sounds['eat_shrink'] = pygame.mixer.Sound(
                "sounds/white apple.mp3")
            self.sounds['crash_wall'] = pygame.mixer.Sound(
                "sounds/crash_wall.mp3")
            self.sounds['crash_self'] = pygame.mixer.Sound("sounds/crash "
                                                           "self.mp3")
        except FileNotFoundError:
            print(
                "Предупреждение: Звуковые файлы SFX не найдены. Игра "
                "запустится без эффектов.")
            self.sfx_enabled = False
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")
            self.sfx_enabled = False

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
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            return Direction.RIGHT
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            return Direction.UP
        elif key[pygame.K_LEFT] or key[pygame.K_a]:
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
        self.screen.blit(rendered, (5, 40))

    def draw_level_start_hint(self):
        """Рисует подсказку для начала движения"""
        self.draw_centered_text("Нажмите любую стрелку,", "white",
                                y=HEIGHT * SCALE // 2 + 50)
        self.draw_centered_text("чтобы начать движение", "white",
                                y=HEIGHT * SCALE // 2 + 80)

    def play_sound(self, sound_name: str):
        """Универсальный метод проигрывания звука по ключу"""
        if self.sfx_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_eat_sound(self, food_type: FoodType):
        """Проигрывает звук в зависимости от типа съеденной еды"""
        if food_type == FoodType.NORMAL:
            self.play_sound('eat_normal')
        elif food_type == FoodType.SPEED:
            self.play_sound('eat_speed')
        elif food_type == FoodType.SHRINK:
            self.play_sound('eat_shrink')

    def play_crash_wall_sound(self):
        """Звук удара о препятствие или стену"""
        self.play_sound('crash_wall')

    def play_crash_self_sound(self):
        """Звук укуса собственного хвоста"""
        self.play_sound('crash_self')

    def is_console_toggle_event(self) -> bool:
        """Проверяет, была ли нажата клавиша ~ (тильда) для открытия консоли"""
        return any(
            event.type == pygame.KEYDOWN and event.key == pygame.K_BACKQUOTE
            for event in self._events
        )

    def process_text_input(self, current_text: str) -> tuple[str, bool]:
        """
        Обрабатывает ввод текста.
        Возвращает обновленный текст и флаг, был ли нажат Enter.
        """
        text = current_text
        enter_pressed = False
        for event in self._events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter_pressed = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key != pygame.K_BACKQUOTE:
                    if event.unicode.isprintable():
                        text += event.unicode
        return text, enter_pressed

    def draw_console(self, text: str):
        """Отрисовка полупрозрачной консоли поверх игры"""
        surface = pygame.Surface((WIDTH * SCALE, 60))
        surface.set_alpha(220)
        surface.fill((0, 0, 0))
        self.screen.blit(surface, (0, 0))

        rendered = self.font.render(f"> {text}_", True, pygame.Color("lime"))
        self.screen.blit(rendered, (15, 18))
