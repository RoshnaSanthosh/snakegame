import pygame
from pygame.locals import *
import time
import random

SIZE = 28
BACKGROUND_COLOR = (18, 6, 2)  

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen        
        self.image = pygame.image.load(r"C:\Users\Roshna Santhosh\OneDrive\Desktop\apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

class Snake:
    def __init__(self, parent_screen, start_x=40, start_y=40, image_path=r"C:\Users\Roshna Santhosh\OneDrive\Desktop\snake.jpg"):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(image_path).convert()
        self.direction = 'down'
        self.length = 1
        self.x = [start_x]
        self.y = [start_y]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        
        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

        
        screen_width = self.parent_screen.get_width()
        screen_height = self.parent_screen.get_height()

        if self.x[0] < 0:
            self.x[0] = screen_width - SIZE
        elif self.x[0] >= screen_width:
            self.x[0] = 0
        if self.y[0] < 0:
            self.y[0] = screen_height - SIZE
        elif self.y[0] >= screen_height:
            self.y[0] = 0

    def draw(self):
        
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Two Player Snake Game")
        self.surface = pygame.display.set_mode((1000, 800))
        
        self.eat_sound = pygame.mixer.Sound(r"C:\Users\Roshna Santhosh\OneDrive\Documents\ding.mp3.mpeg")
        
        self.game_over_sound = pygame.mixer.Sound(r"C:\Users\Roshna Santhosh\OneDrive\Documents\crash.mp3.mpeg")
        
        self.snake = Snake(self.surface, 40, 40,
                           image_path=r"C:\Users\Roshna Santhosh\OneDrive\Desktop\snake.jpg")
        
        self.snake2 = Snake(self.surface, 400, 400,
                            image_path=r"C:\Users\Roshna Santhosh\OneDrive\Desktop\snake2.jpg")
        self.apple = Apple(self.surface)

    def reset(self):
        
        self.snake = Snake(self.surface, 40, 40,
                           image_path=r"C:\Users\Roshna Santhosh\OneDrive\Desktop\snake1.jpg")
        self.snake2 = Snake(self.surface, 400, 400,
                            image_path=r"C:\Users\Roshna Santhosh\OneDrive\Desktop\snake2.jpg")
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        
        self.snake.walk()
        self.snake2.walk()
        self.surface.fill(BACKGROUND_COLOR)
        self.snake.draw()
        self.snake2.draw()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            self.eat_sound.play()
        if self.is_collision(self.snake2.x[0], self.snake2.y[0], self.apple.x, self.apple.y):
            self.snake2.increase_length()
            self.apple.move()
            self.eat_sound.play()

        
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Collision Occurred for Player 1")
        
        for i in range(2, self.snake2.length):
            if self.is_collision(self.snake2.x[0], self.snake2.y[0], self.snake2.x[i], self.snake2.y[i]):
                raise Exception("Collision Occurred for Player 2")

        
        for i in range(self.snake2.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake2.x[i], self.snake2.y[i]):
                raise Exception("Collision Between Players: Player 1 hit Player 2")
        for i in range(self.snake.length):
            if self.is_collision(self.snake2.x[0], self.snake2.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Collision Between Players: Player 2 hit Player 1")

    def display_score(self):
        
        font = pygame.font.SysFont('arial', 30)
        score1 = font.render(f"P1 Score: {self.snake.length}", True, (200, 200, 200))
        score2 = font.render(f"P2 Score: {self.snake2.length}", True, (200, 200, 200))
        self.surface.blit(score1, (850, 10))
        self.surface.blit(score2, (850, 40))

    def show_game_over(self):
    
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render("Game Over!", True, (255, 255, 255))
        line2 = font.render("Closing game in 5 seconds...", True, (255, 255, 255))
        final_score1 = font.render(f"Final Score - Player 1: {self.snake.length}", True, (255, 255, 255))
        final_score2 = font.render(f"Final Score - Player 2: {self.snake2.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 250))
        self.surface.blit(line2, (200, 300))
        self.surface.blit(final_score1, (200, 350))
        self.surface.blit(final_score2, (200, 400))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        # Player 1 controls (arrow keys).
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        # Player 2 controls (WASD keys).
                        if event.key == K_a:
                            self.snake2.move_left()
                        if event.key == K_d:
                            self.snake2.move_right()
                        if event.key == K_w:
                            self.snake2.move_up()
                        if event.key == K_s:
                            self.snake2.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                
                self.game_over_sound.play()
                self.show_game_over()
                print("Game Over!")
                print(f"Final Score - Player 1: {self.snake.length}")
                print(f"Final Score - Player 2: {self.snake2.length}")
                
                time.sleep(5)
                running = False

            time.sleep(0.25)
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
