from infrastructure import Infrastructure
from utils import *


class Game:
    """
    Главный класс игры Snake.
    Отвечает за управление игровым процессом, состоянием игры и главным циклом.
    """

    def __init__(self, infrastructure: Infrastructure):
        """
        Конструктор, инициализирует новую игру.
        """
        self.infrastructure = infrastructure

        # Начальная позиция змейки — центр поля
        head = get_center_element()
        self.snake = Snake(head)

        # Генерируем первое яблоко в случайном месте (не на змейке)
        self.apple = gen_apple(self.snake)

        self.tick_counter = 0                                 # Счётчик кадров для контроля скорости
        self.score = 0                                        # Текущий счёт игрока
        self.snake_speed_delay = INITIAL_SPEED_DELAY       # Задержка движения змейки (чем больше — тем медленнее)

        self.is_running = True
        self.is_game_over = False

    def process_events(self):
        """Обработка ввода от пользователя"""

        # Проверка нажатия крестика в окне
        if self.infrastructure.is_quit_event():
            self.is_running = False

        # Получаем направление из нажатых клавиш
        new_direction = self.infrastructure.get_pressed_key()
        if new_direction is not None:
            self.snake.set_direction(new_direction)

    def render(self):
        """
        Метод отрисовки одного кадра игры на экране
        """
        # Очищает экран
        self.infrastructure.fill_screen()

        # Рисует все сегменты тела змейки
        for e in self.snake.snake:
            self.infrastructure.draw_element(e.x, e.y, SNAKE_COLOR)

        # Рисует яблоко
        self.infrastructure.draw_element(self.apple.x, self.apple.y, APPLE_COLOR)

        # Рисует текущий счёт
        self.infrastructure.draw_score(self.score)

        # Если игра окончена — показывает надпись GAME OVER
        if self.is_game_over:
            self.infrastructure.draw_game_over()

        # Обновляет изображение на экране и ограничивает скорость
        self.infrastructure.update_and_tick()

    def update_state(self):
        """
        Вычисление следующего состояния всех объектов на экране.
        Выполняется каждый кадр, но движение змейки происходит не каждый кадр,
        а только когда счётчик tick_counter достигает snake_speed_delay.
        """

        if self.is_game_over:
            return

        self.tick_counter += 1

        # Двигает змейку только через определённые интервалы для контроля скорости
        if not self.tick_counter % self.snake_speed_delay:

            # Вычисляет позицию новой головы
            head = self.snake.get_new_head()

            # Проверяет не врезались ли в стену или себя
            if is_good_head(head, self.snake):
                self.snake.enqueue(head) # Добавляем новую голову

                # Проверяет, съели ли яблоко
                if head == self.apple:
                    self.score += 1
                    self.apple = gen_apple(self.snake)
                else:
                    # Убирает хвост (обычное движение)
                    self.snake.dequeue()
            else:
                self.is_game_over = True


    def loop(self):
        """
        Главный цикл игры
        В каждом цикле происходит:
            1. Обработка ввода (process_events)
            2. Обновление состояния игры (update_state)
            3. Отрисовка кадра (render)
        """
        while self.is_running:
            self.process_events()
            self.update_state()
            self.render()

        # Корректное завершение pygame при выходе из игры
        self.infrastructure.quit()