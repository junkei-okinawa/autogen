import pygame
import sys
from pygame.locals import *
import time

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Game variables
BALL_RADIUS = 10
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20

ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
paddle1 = pygame.Rect(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

clock = pygame.time.Clock()

class Player:
    def __init__(self, color):
        self.color = color
        self.paddle = None

    def update(self):
        if self.paddle is not None:
            keys = pygame.key.get_pressed()
            if keys[K_w] and self.paddle.top > 0:
                self.paddle.y -= 5
            if keys[K_s] and self.paddle.bottom < SCREEN_HEIGHT:
                self.paddle.y += 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.paddle)

# User_proxy
def user_input():
    keys = pygame.key.get_pressed()
    if keys[K_UP] and player1.paddle is not None:
        player1.paddle.y -= 5
    if keys[K_DOWN] and player2.paddle is not None:
        player2.paddle.y += 5
    return keys

# Main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock.tick(10)
    pygame.time.delay(1000)

    player1 = Player(GREEN)
    player2 = Player(RED)

    ball_speed_x = 5
    ball_speed_y = 5

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = user_input()

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            game_over = True
            break

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            game_over = True
            break

        if player1.paddle is not None and player2.paddle is not None:
            if ball.colliderect(player1.paddle) or ball.colliderect(player2.paddle):
                ball_speed_x = -ball_speed_x
                if ball.x > player1.paddle.x + BALL_RADIUS and ball.x < player1.paddle.x + PADDLE_WIDTH - BALL_RADIUS:
                    ball_speed_y = -ball_speed_y
                elif ball.x > player2.paddle.x + BALL_RADIUS and ball.x < player2.paddle.x + PADDLE_WIDTH - BALL_RADIUS:
                    ball_speed_y = -ball_speed_y

        screen.fill(BLACK)

        player1.update()
        player2.update()
        player1.draw(screen)
        player2.draw(screen)
        ball.draw(screen)

        pygame.display.flip()

    # GameOver screen
    game_over_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_over_font = pygame.font.SysFont("Arial", 32)
    text = game_over_font.render("Game Over", True, WHITE)
    game_over_screen.blit(text, (10, 10))

    buttons = []
    button_width = SCREEN_WIDTH // 4
    button_height = 50
    button_y_offset = 120

    for i in range(2):
        if i == 0:
            text = game_over_font.render("Continue", True, GREEN)
        else:
            text = game_over_font.render("End", True, RED)

        button = pygame.Rect(10, SCREEN_HEIGHT // 2 - button_height // 2 + i * button_y_offset, button_width, button_height)
        buttons.append(button)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = user_input()

        screen.fill(BLACK)

        for button in buttons:
            if button.colliderect(pygame.mouse.get_pos()):
                if i == 0:
                    game_over = False
                    break
                else:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Start the main game loop
if __name__ == "__main__":
    main()