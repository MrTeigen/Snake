import sqlite3
import pygame
import random

# Initialize Pygame
pygame.init()

# SQLite Database Configuration
db_path = 'snake_game.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS highscores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        score INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Window dimensions
window_width = 640
window_height = 480
header_height = 50
game_area_height = window_height - header_height

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

# Function to display the snake and food
def show_snake(snake_size, snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

def show_food(food_pos, snake_size):
    pygame.draw.rect(window, RED, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

def show_score_and_speed(score, speed):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f'Score: {score}', True, WHITE)
    speed_text = font.render(f'Speed: {speed}', True, WHITE)
    window.blit(score_text, (window_width - score_text.get_width() - 10, 10))
    window.blit(speed_text, (10, 10))

def get_highscores():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, score FROM highscores ORDER BY score DESC LIMIT 10")
        highscores = cursor.fetchall()
        cursor.close()
        conn.close()
        return highscores
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return []

def save_highscore(name, score):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", (name, score))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print(f"Error: {err}")

def show_highscores(highscores):
    font = pygame.font.SysFont(None, 35)
    y_offset = 100
    for i, (name, score) in enumerate(highscores):
        score_text = font.render(f'{i + 1}. {name}: {score}', True, WHITE)
        window.blit(score_text, (window_width // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 30

def game_over(score):
    highscores = get_highscores()
    if len(highscores) < 10 or score > highscores[-1][1]:
        name = get_player_name()
        save_highscore(name, score)

def get_player_name():
    name = ""
    font = pygame.font.SysFont(None, 35)
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        window.fill(BLACK)
        prompt_text = font.render('Enter your name:', True, WHITE)
        name_text = font.render(name, True, WHITE)
        window.blit(prompt_text, (window_width // 2 - prompt_text.get_width() // 2, window_height // 2 - 50))
        window.blit(name_text, (window_width // 2 - name_text.get_width() // 2, window_height // 2))
        pygame.display.update()
    return name

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                if event.key == pygame.K_h:
                    highscore_screen()
        window.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        title_text = font.render('Snake Game', True, WHITE)
        start_text = font.render('Press Enter to Start', True, WHITE)
        highscore_text = font.render('Press H for High Scores', True, WHITE)
        window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, window_height // 2 - 100))
        window.blit(start_text, (window_width // 2 - start_text.get_width() // 2, window_height // 2))
        window.blit(highscore_text, (window_width // 2 - highscore_text.get_width() // 2, window_height // 2 + 100))
        pygame.display.update()

def highscore_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    main_menu()
        window.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        title_text = font.render('High Scores', True, WHITE)
        window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 50))
        highscores = get_highscores()
        show_highscores(highscores)
        back_text = font.render('Press Backspace to Return', True, WHITE)
        window.blit(back_text, (window_width // 2 - back_text.get_width() // 2, window_height - 60))
        pygame.display.update()

def main():
    # Game variables
    snake_pos = [[100, header_height + 50], [90, header_height + 50], [80, header_height + 50]]
    snake_size = 10
    speed = 15
    food_pos = [random.randrange(1, (window_width // 10)) * 10, random.randrange(1, (game_area_height // 10)) * 10 + header_height]
    food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0
    
    clock = pygame.time.Clock()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_RIGHT, ord('d')}:
                    change_to = 'RIGHT'
                if event.key in {pygame.K_LEFT, ord('a')}:
                    change_to = 'LEFT'
                if event.key in {pygame.K_UP, ord('w')}:
                    change_to = 'UP'
                if event.key in {pygame.K_DOWN, ord('s')}:
                    change_to = 'DOWN'

        # Validate the direction
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'

        # Update snake position
        if direction == 'RIGHT':
            new_head = [snake_pos[0][0] + snake_size, snake_pos[0][1]]
        if direction == 'LEFT':
            new_head = [snake_pos[0][0] - snake_size, snake_pos[0][1]]
        if direction == 'UP':
            new_head = [snake_pos[0][0], snake_pos[0][1] - snake_size]
        if direction == 'DOWN':
            new_head = [snake_pos[0][0], snake_pos[0][1] + snake_size]

        snake_pos.insert(0, new_head)

        # Check if snake eats the food
        if snake_pos[0] == food_pos:
            score += 1
            food_spawn = False
            if score % 5 == 0:
                speed += 1
        else:
            snake_pos.pop()

        # Spawn new food
        if not food_spawn:
            food_pos = [random.randrange(1, (window_width // 10)) * 10, random.randrange(1, (game_area_height // 10)) * 10 + header_height]
            food_spawn = True

        # Display background and snake
        window.fill(BLACK)
        show_snake(snake_size, snake_pos)
        show_food(food_pos, snake_size)
        show_score_and_speed(score, speed)

        # Draw the game area border
        pygame.draw.line(window, WHITE, (0, header_height), (window_width, header_height), 2)

        # Check if snake hits the boundaries or itself
        if (snake_pos[0][0] < 0 or snake_pos[0][0] >= window_width or
                snake_pos[0][1] < header_height or snake_pos[0][1] >= window_height):
            game_over(score)
            main_menu()
            return
        for block in snake_pos[1:]:
            if block == snake_pos[0]:
                game_over(score)
                main_menu()
                return

        pygame.display.update()
        clock.tick(speed)

if __name__ == '__main__':
    init_db()
    main_menu()
