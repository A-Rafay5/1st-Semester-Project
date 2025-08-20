import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = BLACK
FONT_COLOR = BLACK
BUTTON_COLOR = BLACK
BUTTON_TEXT_COLOR = WHITE

# Load background image
background_image_path = r"C:\Users\User\Desktop\1.jpg"
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Ball")

# Clock for controlling game speed
clock = pygame.time.Clock()

def start_new_game():
    # Initial paddle position
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    paddle_y = HEIGHT - 2 * PADDLE_HEIGHT
    # Ball properties
    ball_x = random.randint(0, WIDTH - 2 * BALL_RADIUS)
    ball_y = 10
    ball_speed_x = 5
    ball_speed_y = 5
    # Score
    score = 0
    return paddle_x, paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score

def draw_start_button():
    start_button = pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50))
    font = pygame.font.Font(None, 36)
    start_text = font.render("Start Game", True, BUTTON_TEXT_COLOR)
    screen.blit(start_text, (WIDTH // 2 - 70, HEIGHT // 2 + 35))
    return start_button

# Game state
game_running = False
game_over = False

while not game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_button = draw_start_button()
            if start_button.collidepoint(mouse_x, mouse_y):
                game_running = True

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw the paddle
    pygame.draw.rect(screen, RED, ((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 2 * PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw the ball
    pygame.draw.circle(screen, BLUE, (WIDTH // 2, HEIGHT // 2), BALL_RADIUS)

    # Display the "Start Game" button
    draw_start_button()

    pygame.display.flip()
    clock.tick(60)

# Start a new game
paddle_x, paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score = start_new_game()

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 5
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += 5

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with walls
        if ball_x <= 0 or ball_x >= WIDTH - 2 * BALL_RADIUS:
            ball_speed_x = -ball_speed_x

        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddle
        if (
            ball_y + BALL_RADIUS >= paddle_y
            and paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH
        ):
            ball_speed_y = -ball_speed_y
            score += 1

        # Ball missed
        if ball_y >= HEIGHT:
            game_over = True

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Draw the paddle
        pygame.draw.rect(screen, RED, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        # Draw the ball
        pygame.draw.circle(screen, BLUE, (ball_x + BALL_RADIUS, ball_y + BALL_RADIUS), BALL_RADIUS)

        # Display the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, FONT_COLOR)
        screen.blit(score_text, (10, 10))

    else:  # Game over state
        # Draw background image
        screen.blit(background_image, (0, 0))

        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over", True, FONT_COLOR)  # Change to black color
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        new_game_button = pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50))
        font = pygame.font.Font(None, 36)
        new_game_text = font.render("New Game", True, BUTTON_TEXT_COLOR)
        screen.blit(new_game_text, (WIDTH // 2 - 70, HEIGHT // 2 + 35))

        # Check for mouse click on the button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if new_game_button.collidepoint(mouse_x, mouse_y):
            click, _, _ = pygame.mouse.get_pressed()
            if click:
                game_over = False
                paddle_x, paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score = start_new_game()

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
