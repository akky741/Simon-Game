
import pygame
import random
import sys
import time

# Initialize
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simon Game")
clock = pygame.time.Clock()

# Fonts
TITLE_FONT = pygame.font.SysFont("comicsansms", 48)
INFO_FONT = pygame.font.SysFont("comicsansms", 28)

# Buttons
button_size = WIDTH // 2
buttons = {
    "green": pygame.Rect(0, 0, button_size, button_size),
    "red": pygame.Rect(button_size, 0, button_size, button_size),
    "yellow": pygame.Rect(0, button_size, button_size, button_size),
    "blue": pygame.Rect(button_size, button_size, button_size, button_size)
}

# Colors
COLORS = {
    "green": ((0, 255, 0), (0, 155, 0)),
    "red": ((255, 0, 0), (155, 0, 0)),
    "yellow": ((255, 255, 0), (155, 155, 0)),
    "blue": ((0, 0, 255), (0, 0, 155)),
}

# Sounds
sounds = {
    "green": pygame.mixer.Sound("sounds/green.wav"),
    "red": pygame.mixer.Sound("sounds/red.wav"),
    "yellow": pygame.mixer.Sound("sounds/yellow.wav"),
    "blue": pygame.mixer.Sound("sounds/blue.wav"),
    "wrong": pygame.mixer.Sound("sounds/wrong.wav"),
}

# Game variables
sequence = []
user_input = []
level = 0
game_state = "start"  # start, show_sequence, user_turn, game_over
instruction = "Press any key to start"

# Timing
user_turn_start_time = 0
MAX_WAIT_TIME = 5  # seconds per input


def draw_buttons(highlight=None):
    for color, rect in buttons.items():
        color_value = COLORS[color][0] if highlight == color else COLORS[color][1]
        pygame.draw.rect(screen, color_value, rect)
    pygame.display.update()


def flash_button(color):
    draw_buttons(highlight=color)
    sounds[color].play()
    pygame.time.delay(400)
    draw_buttons()
    pygame.time.delay(100)


def play_sequence():
    pygame.time.delay(500)
    for color in sequence:
        flash_button(color)
        pygame.time.delay(200)


def reset_game():
    global sequence, user_input, level, game_state, instruction
    sequence = []
    user_input = []
    level = 0
    instruction = "Press any key to start"
    game_state = "start"


def draw_text(text, font, y, color=(255, 255, 255)):
    render = font.render(text, True, color)
    screen.blit(render, (WIDTH // 2 - render.get_width() // 2, y))


def main():
    global sequence, user_input, level, game_state, instruction, user_turn_start_time

    running = True
    while running:
        screen.fill((20, 20, 20))
        draw_buttons()
        draw_text(f"Level: {level}", TITLE_FONT, 20)
        draw_text(instruction, INFO_FONT, 90)
        pygame.display.update()

        if game_state == "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    reset_game()
                    level += 1
                    sequence.append(random.choice(list(buttons.keys())))
                    game_state = "show_sequence"
                    instruction = "Watch the pattern..."

        elif game_state == "show_sequence":
            play_sequence()
            user_input = []
            game_state = "user_turn"
            instruction = "Your turn! Repeat the pattern"
            user_turn_start_time = time.time()

        elif game_state == "user_turn":
            # Check timeout
            if time.time() - user_turn_start_time > MAX_WAIT_TIME:
                game_state = "game_over"
                instruction = "⏰ Too slow! Press any key to restart"
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for color, rect in buttons.items():
                        if rect.collidepoint(x, y):
                            flash_button(color)
                            user_input.append(color)
                            user_turn_start_time = time.time()  # reset timer

                            # Check correctness
                            if color != sequence[len(user_input)-1]:
                                game_state = "game_over"
                                instruction = "❌ Wrong! Press any key to restart"
                                break

                            if len(user_input) == len(sequence):
                                level += 1
                                sequence.append(random.choice(list(buttons.keys())))
                                game_state = "show_sequence"
                                instruction = f"✔️ Good job! Watch next pattern..."
                                pygame.time.delay(500)

        elif game_state == "game_over":
            sounds["wrong"].play()
            draw_buttons()
            pygame.display.update()
            pygame.time.delay(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    reset_game()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
