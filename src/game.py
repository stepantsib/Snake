from infrastructure import Infrastructure
from utils import *
from food import Food, FoodType
from constants import *
from random import choices

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

        self.food = self._generate_food()  # храним Food объект
        self.tick_counter = 0                                 # Счётчик кадров для контроля скорости
        self.snake_speed_delay = INITIAL_SPEED_DELAY       # Задержка движения змейки (чем больше — тем медленнее)

        # Для эффекта ускорения
        self.speed_boost_end_tick = 0
        self.is_speed_boost_active = False

        self.is_running = True
        self.is_game_over = False


    def _generate_food(self) -> Food:
        """Генерирует случайный объект еды случайного типа"""

        element = gen_apple(self.snake)
        types = [FoodType.NORMAL, FoodType.SPEED, FoodType.SHRINK]
        weights = [75, 20, 5]  # вероятности выпадения яблок
        food_type = choices(types, weights=weights, k=1)[0]

        return Food(element, food_type)


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

        # Выбирает нужный цвет
        color = {
            FoodType.NORMAL: NORMAL_FOOD_COLOR,
            FoodType.SPEED: SPEED_FOOD_COLOR,
            FoodType.SHRINK: SHRINK_FOOD_COLOR
        }[self.food.type]

        # Рисует еду с нужным цветом
        self.infrastructure.draw_element(self.food.x, self.food.y, color)

        # Рисует текущий счёт
        current_score = len(self.snake.snake)
        self.infrastructure.draw_score(current_score)

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

        if self.is_speed_boost_active and self.tick_counter >= self.speed_boost_end_tick:
            self.is_speed_boost_active = False
            self.snake_speed_delay = INITIAL_SPEED_DELAY

        # Двигает змейку только через определённые интервалы для контроля скорости
        if not self.tick_counter % self.snake_speed_delay:
            # Вычисляет позицию новой головы
            head = self.snake.get_new_head()

            # Проверяет не врезались ли в себя
            if is_good_head(head, self.snake):
                self.snake.enqueue(head) # Добавляем новую голову

                if head == self.food.element:  # Съели еду
                    self._eat_food()
                else:
                    # Убирает хвост (обычное движение)
                    self.snake.dequeue()
            else:
                self.is_game_over = True

    def _eat_food(self):
        """Обработка съедания еды"""
        if self.food.type == FoodType.SPEED:
            self.is_speed_boost_active = True
            self.snake_speed_delay = INITIAL_SPEED_DELAY // 2  # в 2 раза быстрее
            self.speed_boost_end_tick = self.tick_counter + (5 * FPS)

        elif self.food.type == FoodType.SHRINK:
            self._shrink_snake()

        # Генерируем новую еду
        self.food = self._generate_food()


    def _shrink_snake(self):
        """Уменьшает длину змейки в 2 раза (минимум 1 сегмент)"""
        target_length = max(1, len(self.snake.snake) // 2)
        while len(self.snake.snake) > target_length:
            self.snake.dequeue()


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