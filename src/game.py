from infrastructure import Infrastructure
from utils import *
from food import Food, FoodType
from constants import *
from random import choices
from level import GameLevel, Level
import time
from element import Element


class Game:
    def __init__(self, infrastructure: Infrastructure):
        self.infrastructure = infrastructure

        self.current_level_num = 1
        self.level = GameLevel(Level.ONE)
        self.game_start_time = time.time()
        self.start_level_time = time.time()

        head = self._get_spawn_element_for_level()
        self.snake = Snake(head)

        self.food = self._generate_food()
        self.tick_counter = 0
        self.snake_speed_delay = INITIAL_SPEED_DELAY

        self.speed_boost_end_tick = 0
        self.is_speed_boost_active = False

        self.is_running = True
        self.is_game_over = False
        self.is_level_completed = False

    def _generate_food(self) -> Food:
        element = gen_apple(self.snake,
                            self.level)  # передаём уровень для
        # избежания препятствий
        types = [FoodType.NORMAL, FoodType.SPEED, FoodType.SHRINK]
        weights = [75, 23, 2]
        food_type = choices(types, weights=weights, k=1)[0]
        return Food(element, food_type)

    def process_events(self):
        if self.infrastructure.is_quit_event():
            self.is_running = False

        new_direction = self.infrastructure.get_pressed_key()
        if new_direction is not None:
            self.snake.set_direction(new_direction)

    def render(self):
        self.infrastructure.fill_screen()

        # Рисуем змейку
        for e in self.snake.snake:
            self.infrastructure.draw_element(e.x, e.y, SNAKE_COLOR)

        # Рисуем препятствия
        for ox, oy in self.level.obstacles:
            self.infrastructure.draw_element(ox, oy, "gray")

        # Рисуем еду
        color = {
            FoodType.NORMAL: NORMAL_FOOD_COLOR,
            FoodType.SPEED: SPEED_FOOD_COLOR,
            FoodType.SHRINK: SHRINK_FOOD_COLOR
        }[self.food.type]
        self.infrastructure.draw_element(self.food.x, self.food.y,
                                         color)

        # Счёт и уровень
        current_score = len(self.snake.snake)
        self.infrastructure.draw_score(current_score)
        self.infrastructure.draw_level_info(self.current_level_num,
                                            self.level.target_score)

        if self.is_game_over:
            self.infrastructure.draw_game_over()
        elif self.is_level_completed:
            self.infrastructure.draw_level_complete(self.current_level_num)

        self.infrastructure.update_and_tick()

    def update_state(self):
        if self.is_game_over or self.is_level_completed:
            return

        self.tick_counter += 1

        if (self.is_speed_boost_active and self.tick_counter >=
                self.speed_boost_end_tick):
            self.is_speed_boost_active = False
            self.snake_speed_delay = INITIAL_SPEED_DELAY

        if not self.tick_counter % self.snake_speed_delay:
            new_head = self.snake.get_new_head()

            if self.level.is_obstacle(new_head.x, new_head.y):
                self.is_game_over = True
                self.is_running = False
                return

            will_eat = (new_head == self.food.element)

            collision = False
            if self.snake.is_contains(new_head):
                if will_eat:
                    collision = True
                else:
                    tail = self.snake.snake[-1]
                    if new_head != tail:
                        collision = True

            if collision:
                self.is_game_over = True
                self.is_running = False
            else:
                self.snake.enqueue(new_head)
                if will_eat:
                    self._eat_food()
                else:
                    self.snake.dequeue()

            # Проверка победы
            current_score = len(self.snake.snake)
            if current_score >= self.level.target_score:
                self._complete_level()

    def _eat_food(self):
        if self.food.type == FoodType.SPEED:
            self.is_speed_boost_active = True
            self.snake_speed_delay = INITIAL_SPEED_DELAY // 2
            self.speed_boost_end_tick = self.tick_counter + (5 * FPS)

        elif self.food.type == FoodType.SHRINK:
            self._shrink_snake()

        self.food = self._generate_food()

    def _shrink_snake(self):
        target_length = max(1, len(self.snake.snake) // 2)
        while len(self.snake.snake) > target_length:
            self.snake.dequeue()

    def _complete_level(self):
        self.is_level_completed = True
        if self.current_level_num < 3:
            # Переход на следующий уровень
            self.current_level_num += 1
            self.level = GameLevel(Level(self.current_level_num))
            self.start_level_time = time.time()
            # Сброс змейки
            head = self._get_spawn_element_for_level()
            self.snake = Snake(head)
            self.food = self._generate_food()
            self.is_level_completed = False
        else:
            total_time = int(time.time() - self.game_start_time)
            self._save_highscore(total_time)
            print(f"Поздравляем! Вы прошли все уровни за {total_time} секунд!")

            self.is_running = False
            self.is_level_completed = True

    def _save_highscore(self, time_sec: int):
        try:
            with open("highscores.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"Уровень 3 | Время: {time_sec} сек | "
                    f"{time.strftime('%Y-%m-%d %H:%M')}\n")
        except:
            pass

    def _get_spawn_element_for_level(self):
        # Для 3 уровня: сверху по центру
        if self.current_level_num == 3:
            return Element(WIDTH // 2, 1)
        # Для остальных уровней - дефолт
        return get_center_element()

    def loop(self):
        """
        Главный цикл игры
        В каждом цикле происходит:
            1. Обработка ввода (process_events)
            2. Обновление состояния игры (update_state)
            3. Отрисовка кадра (render)
        """
        while self.is_running:
            self.infrastructure.pump_events()

            self.process_events()
            self.update_state()
            self.render()
