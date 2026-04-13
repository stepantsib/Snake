from infrastructure import Infrastructure
from utils import *
from food import Food, FoodType
from constants import *
from random import choices, randint
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

        self.normal_food = self._generate_normal_food()
        self.special_food = None
        self.special_food_spawn_tick = 0
        self.special_food_next_spawn_tick = FPS * 5
        self.tick_counter = 0
        self.snake_speed_delay = INITIAL_SPEED_DELAY

        self.speed_boost_end_tick = 0
        self.is_speed_boost_active = False

        self.is_running = True
        self.is_game_over = False
        self.is_level_completed = False

    def _generate_normal_food(self) -> Food:
        while True:
            element = gen_apple(self.snake, self.level)
            # Проверяем, чтобы обычная еда не заспавнилась поверх специальной
            if (not hasattr(self,
                            'special_food') or self.special_food is None or
                    element != self.special_food.element):
                return Food(element, FoodType.NORMAL)

    def _generate_special_food(self) -> Food:
        while True:
            element = gen_apple(self.snake, self.level)
            # Проверяем, чтобы специальная еда не заспавнилась поверх обычной
            if element != self.normal_food.element:
                break

        types = [FoodType.SPEED, FoodType.SHRINK]
        weights = [24, 1]
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
        self.infrastructure.draw_element(self.normal_food.x,
                                         self.normal_food.y,
                                         NORMAL_FOOD_COLOR)
        if self.special_food:
            special_color = SPEED_FOOD_COLOR if (self.special_food.type ==
                                                 FoodType.SPEED) else (
                SHRINK_FOOD_COLOR)
            self.infrastructure.draw_element(self.special_food.x,
                                             self.special_food.y,
                                             special_color)

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

        if self.special_food:
            # Если прошло 10 секунд (10 * FPS) — еда исчезает
            if self.tick_counter >= self.special_food_spawn_tick + (10 * FPS):
                self.special_food = None
                # Следующая появится через случайное время от 1 до 3 секунд
                self.special_food_next_spawn_tick = self.tick_counter + randint(
                    1 * FPS, 3 * FPS)
        else:
            # Спавним специальную еду, если пришло время
            if self.tick_counter >= self.special_food_next_spawn_tick:
                self.special_food = self._generate_special_food()
                self.special_food_spawn_tick = self.tick_counter

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

            # Проверяем, съели ли мы какую-то еду в этом кадре
            will_eat_normal = (new_head == self.normal_food.element)
            will_eat_special = self.special_food is not None and (
                    new_head == self.special_food.element)
            will_eat = will_eat_normal or will_eat_special

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
                    if will_eat_normal:
                        self.normal_food = self._generate_normal_food()

                    if will_eat_special:
                        self._apply_special_food(self.special_food.type)
                        self.special_food = None
                        # Задаем время следующего спавна после того, как съели
                        self.special_food_next_spawn_tick = (self.tick_counter
                                                             + randint(
                            1 * FPS, 5 * FPS))
                else:
                    self.snake.dequeue()

            current_score = len(self.snake.snake)
            if current_score >= self.level.target_score:
                self._complete_level()

    def _apply_special_food(self, food_type):
        if food_type == FoodType.SPEED:
            self.is_speed_boost_active = True
            self.snake_speed_delay = INITIAL_SPEED_DELAY // 2
            self.speed_boost_end_tick = self.tick_counter + (5 * FPS)

        elif food_type == FoodType.SHRINK:
            self._shrink_snake()

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
            self.normal_food = self._generate_normal_food()
            self.special_food = None
            self.special_food_spawn_tick = 0
            self.special_food_next_spawn_tick = self.tick_counter + (5 * FPS)
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
