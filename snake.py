import pygame
import sys
import time
import random


"""
Данный код реализует простую игру "Змейка" с использованием библиотеки Pygame 
в стиле объектно-ориентированного программирования. 
Он состоит из трех основных классов: StartScreen управляет начальным экраном, 
где игрок выбирает уровень сложности; 
SnakeGame отвечает за основной игровой процесс, включая движение змейки, 
сбор еды и отображение счета; 
EndScreen отображает экран завершения игры, показывая результат игрока. 
Код также включает комментарии для улучшения понимания его работы и структуры.
"""


class StartScreen:
    def __init__(self, width, height):
        # Инициализация параметров стартового экрана
        self.frame_size_x = width
        self.frame_size_y = height

        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)

        self.fps_controller = pygame.time.Clock()

        self.difficulty = None

    def display_text(self, text, color, font=None, size=30, y_offset=0):
        # Отображение текста на экране
        font = pygame.font.SysFont(font, size)

        text_surface = font.render(text, True, color)

        text_rect = text_surface.get_rect()
        text_rect.center = (self.frame_size_x // 2, self.frame_size_y // 2 + y_offset)

        self.game_window.blit(text_surface, text_rect)

        pygame.display.update()

    def choose_difficulty(self):
        # Метод для выбора сложности игры

        pygame.font.init()  # Инициализация шрифтов

        while not self.difficulty:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        self.difficulty = 10

                    elif event.key == pygame.K_2:
                        self.difficulty = 25

                    elif event.key == pygame.K_3:
                        self.difficulty = 40

            # Отображение экрана выбора сложности
            self.game_window.fill(self.black)

            self.display_text('Choose difficulty:', self.white, font='arial', size=40, y_offset=-50)

            self.display_text('1 - Easy', self.white, font='arial', size=30, y_offset=0)

            self.display_text('2 - Medium', self.white, font='arial', size=30, y_offset=50)

            self.display_text('3 - Hard', self.white, font='arial', size=30, y_offset=100)

            self.fps_controller.tick(10)

        return self.difficulty


class SnakeGame:
    def __init__(self, width, height, difficulty):
        # Инициализация параметров игры
        pygame.init()
        pygame.font.init()

        self.frame_size_x = width
        self.frame_size_y = height

        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        self.fps_controller = pygame.time.Clock()
        self.difficulty = difficulty

        self.snake_pos = [100, 50]

        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                         random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True

        self.direction = 'RIGHT'

        self.change_to = self.direction

        self.score = 0

        self.running = True  # Флаг для проверки, запущена ли игра

    def game_over(self):
        # Завершение игры
        pygame.quit()

        EndScreen(self.frame_size_x, self.frame_size_y, self.score)

    def show_score(self):
        # Отображение счета на экране
        pygame.font.init()

        score_font = pygame.font.SysFont('times', 20)

        score_surface = score_font.render('Score : ' + str(self.score), True, self.white)

        score_rect = score_surface.get_rect()

        score_rect.midtop = (self.frame_size_x // 2, self.frame_size_y // 1.25)

        self.game_window.blit(score_surface, score_rect)

    def run_game(self):
        # Основной игровой цикл
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.running = False

                    self.game_over()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.change_to = 'UP'

                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.change_to = 'DOWN'

                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.change_to = 'LEFT'

                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.change_to = 'RIGHT'

                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'

            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'

            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'

            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            if self.direction == 'UP':
                self.snake_pos[1] -= 10

            if self.direction == 'DOWN':
                self.snake_pos[1] += 10

            if self.direction == 'LEFT':
                self.snake_pos[0] -= 10

            if self.direction == 'RIGHT':
                self.snake_pos[0] += 10

            self.snake_body.insert(0, list(self.snake_pos))

            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
                self.score += 1
                self.food_spawn = False

            else:
                self.snake_body.pop()

            if not self.food_spawn:
                self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                                 random.randrange(1, (self.frame_size_y // 10)) * 10]

            self.food_spawn = True

            self.game_window.fill(self.black)

            for pos in self.snake_body:
                pygame.draw.rect(self.game_window, self.green, pygame.Rect(pos[0], pos[1], 10, 10))

            pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

            if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x - 10:
                self.running = False

                self.game_over()

            if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y - 10:
                self.running = False

                self.game_over()

            for block in self.snake_body[1:]:
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                    self.running = False

                    self.game_over()

            if self.running:  # Проверяем, что игра еще не закрыта
                self.show_score()

                pygame.display.update()
                self.fps_controller.tick(self.difficulty)


class EndScreen:
    def __init__(self, width, height, score):
        # Инициализация параметров экрана завершения игры
        pygame.init()
        pygame.font.init()

        self.frame_size_x = width
        self.frame_size_y = height

        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)

        self.fps_controller = pygame.time.Clock()

        self.score = score

    def display_text(self, text, color, font='times new roman', size=30, y_offset=0):
        # Отображение текста на экране
        font = pygame.font.SysFont(font, size)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.frame_size_x // 2, self.frame_size_y // 2 + y_offset)

        self.game_window.blit(text_surface, text_rect)

        pygame.display.update()

    def run(self):
        # Основной цикл экрана завершения игры
        self.game_window.fill(self.black)

        self.display_text('Game Over', self.red, size=90, y_offset=-50)
        self.display_text('Score: {}'.format(self.score), self.white, size=40, y_offset=0)
        self.display_text('Press any key to exit', self.white, size=30, y_offset=50)

        pygame.display.update()

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    start_screen = StartScreen(720, 480)

    difficulty = start_screen.choose_difficulty()

    game = SnakeGame(720, 480, difficulty)
    game.run_game()

    end_screen = EndScreen(720, 480, game.score)
    end_screen.run()