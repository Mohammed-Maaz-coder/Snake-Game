author = 'CodeWithHarry'

# Importing The Modules
import pygame
import random
import os

# Initialization
pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
snakegreen = (35, 45, 40)

# Creating The Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snake By CodeWithHarry")
pygame.display.update()

# Load Music (Check if the file exists before loading)
music_files = ['music/wc.mp3', 'music/bgm.mp3', 'music/bgm1.mp3', 'music/bgm2.mp3']
if os.path.exists(music_files[0]):
    pygame.mixer.music.load(music_files[0])
    pygame.mixer.music.play(-1)  # Loop indefinitely
    pygame.mixer.music.set_volume(0.6)

# Load Images (Check if files exist)
bg2 = pygame.image.load("Screen/bg2.jpg") if os.path.exists("Screen/bg2.jpg") else None
intro = pygame.image.load("Screen/intro1.jpg") if os.path.exists("Screen/intro1.jpg") else None
outro = pygame.image.load("Screen/outro.png") if os.path.exists("Screen/outro.png") else None

# Variables For The Game
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 35)

# Function to Display Text on Screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Function to Draw Snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Welcome Screen
def welcome():
    exit_game = False
    while not exit_game:
        if intro:
            gameWindow.blit(intro, (0, 0))
        else:
            gameWindow.fill(white)
            text_screen("Press ENTER to Start", black, 300, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.fadeout(200)
                    if os.path.exists(music_files[1]):
                        pygame.mixer.music.load(music_files[1])
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.6)
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # Highscore Handling
    highscore = 0
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        try:
            highscore = int(f.read().strip())
        except ValueError:
            highscore = 0  # Default highscore if file is empty

    # Food Position
    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)

    # Game Variables
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    paused = False  # Added pause feature

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            # Game Over Screen
            if outro:
                gameWindow.blit(outro, (0, 0))
            else:
                gameWindow.fill(white)
                text_screen("Game Over! Press ENTER to Restart", red, 200, 250)

            text_screen(f"Score: {score}", snakegreen, 385, 350)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()  # Go back to the welcome screen
            pygame.display.update()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_p:  # Pause game
                        paused = not paused
                    if event.key == pygame.K_q:  # Cheat code for testing
                        score += 10

            if paused:
                text_screen("Game Paused. Press P to Resume", red, 250, 250)
                pygame.display.update()
                continue  # Skip movement when paused

            snake_x += velocity_x
            snake_y += velocity_y

            # Food Collision
            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 10
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snk_length += 5
                if score > highscore:
                    highscore = score

            # Draw Background
            if bg2:
                gameWindow.blit(bg2, (0, 0))
            else:
                gameWindow.fill(white)

            # Display Score
            text_screen(f"Score: {score}  Highscore: {highscore}", snakegreen, 5, 5)

            # Draw Food
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            # Snake Mechanics
            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Check Collision with Itself
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.stop()
                if os.path.exists(music_files[2]):
                    pygame.mixer.music.load(music_files[2])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.6)

            # Check Wall Collision
            if snake_x < 0 or snake_x + snake_size > screen_width or snake_y < 0 or snake_y + snake_size > screen_height:
                game_over = True
                if os.path.exists(music_files[3]):
                    pygame.mixer.music.load(music_files[3])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.6)

            # Draw Snake
            plot_snake(gameWindow, black, snk_list, snake_size)

            pygame.display.update()
            clock.tick(fps)

    pygame.quit()
    exit()

# Start the Game
welcome()
