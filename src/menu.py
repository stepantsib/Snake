import pygame
from constants import WIDTH, HEIGHT, SCALE
from game import Game


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def draw(self, screen, font):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, pygame.Color(color), self.rect, border_radius=12)
        pygame.draw.rect(screen, pygame.Color("white"), self.rect, 3, border_radius=12)

        text_surf = font.render(self.text, True, pygame.Color("white"))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Menu:
    def __init__(self, infrastructure):
        self.infrastructure = infrastructure
        self.screen = infrastructure.screen
        self.font = infrastructure.font
        self.big_font = pygame.font.Font(None, SCALE * 2)

        self.music_enabled = True

        center_x = WIDTH * SCALE // 2 - 150

        self.main_buttons = [
            Button(center_x, 180, 300, 60, "Начать игру", "#4CAF50", "#45a049", "start"),
            Button(center_x, 260, 300, 60, "Таблица рекордов", "#2196F3", "#1976D2", "highscores"),
            Button(center_x, 340, 300, 60, "Музыка: ВКЛ", "#FF9800", "#F57C00", "music"),
            Button(center_x, 420, 300, 60, "Выйти", "#f44336", "#d32f2f", "quit"),
        ]

        self.music_button = self.main_buttons[2]

        try:
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except:
            self.music_enabled = False
            self.music_button.text = "Музыка: недоступна"

    def toggle_music(self):
        if "недоступна" in self.music_button.text:
            return
        self.music_enabled = not self.music_enabled
        self.music_button.text = "Музыка: ВКЛ" if self.music_enabled else "Музыка: ВЫКЛ"
        try:
            if self.music_enabled:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        except:
            pass

    def _process_events(self, buttons=None, exit_on_input=False):
        if buttons is not None:
            pos = self.infrastructure.get_mouse_position()
            for btn in buttons:
                btn.check_hover(pos)

            if self.infrastructure.was_mouse_clicked():
                for btn in buttons:
                    if btn.is_clicked(pos):
                        return btn.action

        if exit_on_input and self.infrastructure.any_input_event():
            return "exit"

        if self.infrastructure.is_quit_event():
            return "quit"

        return None

    def show_highscores(self):
        try:
            with open("highscores.txt", "r", encoding="utf-8") as f:
                records = f.readlines()[-10:]
        except:
            records = ["Нет сохранённых рекордов."]

        while True:
            self.infrastructure.pump_events()

            action = self._process_events(exit_on_input=True)
            if action == "quit":
                self.infrastructure.quit()
                return
            elif action == "exit":
                return

            self.infrastructure.fill_screen()

            self.infrastructure.draw_centered_text(
                "ТАБЛИЦА РЕКОРДОВ", "gold", y=80, font=self.big_font
            )

            y = 160
            for line in records:
                text = self.font.render(line.strip(), True, pygame.Color("white"))
                self.screen.blit(text, (80, y))
                y += 35

            self.infrastructure.draw_centered_text(
                "Кликните или нажмите клавишу для возврата",
                "gray",
                y=HEIGHT * SCALE - 60
            )

            pygame.display.update()

    def draw_main_menu(self):
        self.infrastructure.fill_screen()

        self.infrastructure.draw_centered_text(
            "SNAKE", "yellow", y=80, font=self.big_font
        )
        self.infrastructure.draw_centered_text(
            "Классическая змейка с уровнями", "gray", y=130
        )

        for btn in self.main_buttons:
            btn.draw(self.screen, self.font)

        pygame.display.update()

    def show_end_screen(self, is_win: bool):
        """Экран выбора после окончания игры"""
        center_x = WIDTH * SCALE // 2 - 150
        end_buttons = [
            Button(center_x, 240, 300, 60, "Начать новую игру", "#4CAF50", "#45a049", "restart"),
            Button(center_x, 320, 300, 60, "Выйти из приложения", "#f44336", "#d32f2f", "quit")
        ]

        while True:
            self.infrastructure.pump_events()

            action = self._process_events(end_buttons)
            if action is not None:
                return action

            self.infrastructure.fill_screen()

            title_text = "ИГРА ПРОЙДЕНА!" if is_win else "GAME OVER"
            title_color = "lime" if is_win else "red"
            self.infrastructure.draw_centered_text(
                title_text, title_color, y=120, font=self.big_font
            )

            for btn in end_buttons:
                btn.draw(self.screen, self.font)

            pygame.display.update()

    def run(self):
        while True:
            self.infrastructure.pump_events()

            action = self._process_events(self.main_buttons)

            if action == "quit":
                self.infrastructure.quit()
                return

            elif action == "start":
                game = Game(self.infrastructure)
                game.loop()

                is_win = game.is_level_completed and game.current_level_num == 3
                result = self.show_end_screen(is_win)

                if result == "quit":
                    self.infrastructure.quit()
                    return

            elif action == "highscores":
                self.show_highscores()

            elif action == "music":
                self.toggle_music()

            self.draw_main_menu()
            self.infrastructure.clock.tick(60)
