# The engagement period for this game is 90 seconds.
# I added 3 nonaddictive features in this project.

# 1. Positive Disengagement: 
# After 90 seconds of gameplay, a pop-up message appears to celebrate the player’s 
# progress and suggest taking a short break.

# 2. Negative Disengagement: 
# If the player chooses not to take a break after 90 seconds, the game becomes harder:
# one burnt cookie (distractor) is added after each new score, instead of one distractor after getting 5 scores.

# 3. Negative Disengagement: 
# If the player keeps playing without a break, their interaction slows down:
# they must double-click instead of single-click to collect cookies. 
# (and this change happens with no visual indication.)

import pygame
import random
import sys
import math
import time

# Initialize Pygame
pygame.init()

# ========================================
# CONSTANTS - Define once, use everywhere
# ========================================

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB format: Red, Green, Blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
DARK_RED = (139, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (210, 180, 140)
GRAY = (128, 128, 128)
GREEN = (34, 139, 34)

# Frame rate
FPS = 60

# Game balance constants
DISTRACTOR_SPAWN_THRESHOLD = 5   # After every 5 points, a new distractor (burnt cookie) appears.
DISTRACTORS_PER_SPAWN = 1   # Number of distractors added each time the threshold is reached.
BASE_SPEED = 2   # The initial movement speed of distractors.
SPEED_INCREMENT = 0.3   # The speed of distractors move as the player's score increases.
MAX_SPEED = 8   # Distractors move faster as the player’s score rises, up to MAX_SPEED.
ENGAGEMENT_PERIOD = 90   # Define the engagement period.
DOUBLE_CLICK_WINDOW = 0.5   # Maximum time interval (in secs) between two clicks to count as a double-click.

# ========================================
# GAME SETUP - Initialize game components
# ========================================

# Set up the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cookie Clicker Challenge")

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# ========================================
# GAME ASSETS
# ========================================

# Load and scale a cookie image from file.
def load_cookie_image(filepath, size=100):
    # Try to load my custom cookie image from file.
    try:
        img = pygame.image.load(filepath).convert_alpha()
        img = pygame.transform.scale(img, (size, size))
        return img
    # If loading fails, it calls create_cookie_surface() to draw one.
    except pygame.error as e:
        print(f"Error loading image '{filepath}': {e}")
        print("Falling back to generated cookie...")
        return create_cookie_surface(size)

def create_cookie_surface(size=100):
    # Generate a cookie graphic using Pygame drawing functions.
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw a circular cookie base with an outline.
    pygame.draw.circle(surf, LIGHT_BROWN, (center, center), center - 2)
    pygame.draw.circle(surf, BROWN, (center, center), center - 2, 3)
    
    # Place dark “chocolate chip” circles in a few fixed positions.
    chip_positions = [
        (0.3, 0.3), (0.7, 0.3), (0.5, 0.5),
        (0.3, 0.7), (0.7, 0.7), (0.2, 0.5), (0.8, 0.5)
    ]
    for x_ratio, y_ratio in chip_positions:
        chip_x = int(center + (x_ratio - 0.5) * size * 0.6)
        chip_y = int(center + (y_ratio - 0.5) * size * 0.6)
        pygame.draw.circle(surf, DARK_RED, (chip_x, chip_y), size // 15)
    
    return surf

# Draw burnt cookie (distractor).
def create_burnt_cookie_surface(size=100):
    # Generate a burnt cookie (distractor) graphic.
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Make a darker cookie shape (looks burnt).
    pygame.draw.circle(surf, (50, 40, 30), (center, center), center - 2)
    pygame.draw.circle(surf, BLACK, (center, center), center - 2, 3)
    
    # Add random dark burn spots using math.
    for _ in range(8):
        spot_angle = random.uniform(0, 2 * math.pi)
        spot_dist = random.uniform(center * 0.3, center * 0.7)
        spot_x = int(center + math.cos(spot_angle) * spot_dist)
        spot_y = int(center + math.sin(spot_angle) * spot_dist)
        pygame.draw.circle(surf, BLACK, (spot_x, spot_y), size // 20)
    
    return surf

# Load the main cookie image or draw one.
cookie_img = load_cookie_image("cookie.png", 100)
# Create a list with one “burnt cookie” to use as distractors.
distractor_imgs = [create_burnt_cookie_surface(100)]

# ========================================
# GAME VARIABLES - Store game state
# ========================================

score = 0
lives = 3
game_state = "start"
high_score = 0  # Store best score achieved.
cookie_rect = cookie_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Track position of the cookie.
distractors = []  # Hold all moving fake cookies.
last_spawn_score = 0  # Decide when to spawn new distractors.

# Add nonaddictive variables.
session_start_time = None   # Records when the current game session starts. 
time_remaining = ENGAGEMENT_PERIOD   # Tracks the time left in the current session.
difficulty_mode = False
double_click_action = False
last_click_time = 0   # Tracks the time of the last click (for detecting double-click).
last_click_pos = None   # Detects double-clicks in same area.

# ========================================
# ADD NONADDICTIVE FUNCTIONS
# ========================================

# Create a break suggestion message that appears after 90 seconds of play.
# Displays how many cookies the player collected in 90 seconds.
def break_message(score_value):
    return f"Cookie Champion! You've collected {score_value} cookies in 90 seconds!"

# ========================================
# GAME FUNCTIONS - Helper functions
# ========================================

# Draw text with optional centering on screen.
def draw_text(text, size, color, x, y, center=False):
    font = pygame.font.SysFont(None, size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)

# Reset score, lives, and positions so the player can restart.
def reset_game():
    global score, lives, distractors, cookie_rect, game_state, last_spawn_score
    global session_start_time, time_remaining, difficulty_mode, double_click_action
    global last_click_time, last_click_pos

    score = 0
    lives = 3
    distractors.clear()   # Remove all burnt cookies from screen.
    last_spawn_score = 0
    cookie_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    game_state = "playing"

    # Reset nonaddictive design variables.
    session_start_time = time.time()   # Start new session timer.
    time_remaining = ENGAGEMENT_PERIOD
    difficulty_mode = False
    double_click_action = False
    last_click_time = 0
    last_click_pos = None

# Move cookie to a new random spot within screen boundaries.
def spawn_cookie():
    margin = 80
    x = random.randint(margin, SCREEN_WIDTH - margin)
    y = random.randint(margin, SCREEN_HEIGHT - margin)
    cookie_rect.center = (x, y)

# Each time this is called, create a moving burnt cookie.
def spawn_distractor():
    img = random.choice(distractor_imgs)
    margin = 80
    rect = img.get_rect(
        center=(random.randint(margin, SCREEN_WIDTH - margin),
                random.randint(margin, SCREEN_HEIGHT - margin))
    )
    # Speed increases as score goes up, but is capped at MAX_SPEED.
    current_speed = min(BASE_SPEED + (score // 10) * SPEED_INCREMENT, MAX_SPEED)
    dx = random.choice([-1, 1]) * random.uniform(current_speed * 0.8, current_speed)
    dy = random.choice([-1, 1]) * random.uniform(current_speed * 0.8, current_speed)
    distractors.append([rect, dx, dy, img])

# Move all distractors every frame.
def move_distractors():
    for d in distractors:
        rect, dx, dy, img = d
        rect.x += dx
        rect.y += dy
        
        # If they hit an edge, they “bounce” by reversing direction.
        if rect.left <= 0 or rect.right >= SCREEN_WIDTH:
            d[1] *= -1
        if rect.top <= 0 or rect.bottom >= SCREEN_HEIGHT:
            d[2] *= -1

# ========================================
# MAIN GAME LOOP
# ========================================

running = True
while running:
    screen.fill(WHITE)

    # ----------------------------------------
    # 1. EVENT HANDLING
    # ----------------------------------------
    # Captures mouse clicks and key presses.
    for event in pygame.event.get():
        # Check if user wants to quit
        if event.type == pygame.QUIT:
            running = False
        
        # START SCREEN
        if game_state == "start":
            if event.type == pygame.MOUSEBUTTONDOWN:
                reset_game()
        
        # PLAYING STATE
        # "p" for pauses. "esc" for back to menu.
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = "paused"
                elif event.key == pygame.K_ESCAPE:
                    game_state = "start"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check cookie click.
                if cookie_rect.collidepoint(mouse_pos):
                    current_time = time.time()

                    # Check if double-click mode is active (after 90s and choose no break choice).
                    if double_click_action:
                        # Check if player clicks twice quickly and close enough.
                        if (last_click_pos and 
                            abs(mouse_pos[0] - last_click_pos[0]) < 20 and 
                            abs(mouse_pos[1] - last_click_pos[1]) < 20 and
                            current_time - last_click_time < DOUBLE_CLICK_WINDOW):

                            # Valid double-click and count as 1 cookie collected.
                            score += 1
                            spawn_cookie()
                            
                            # Negative Disengagement: add 1 extra distractor after each score.
                            if difficulty_mode:
                                spawn_distractor()
                            
                            # Add regular distractors every 5 scores.
                            if score >= DISTRACTOR_SPAWN_THRESHOLD and \
                               score - last_spawn_score >= DISTRACTOR_SPAWN_THRESHOLD:
                                for _ in range(DISTRACTORS_PER_SPAWN):
                                    spawn_distractor()
                                last_spawn_score = score
                            
                            # Reset click tracking after one double-click.
                            last_click_time = 0
                            last_click_pos = None
                        else:
                            # First click of double-click.
                            last_click_time = current_time
                            last_click_pos = mouse_pos
                    
                    # Normal Single-click Mode.
                    else:
                        # Check cookie click (Normal single-click mode).
                        score += 1
                        spawn_cookie()
                        
                        # Add extra distractor if in difficulty mode.
                        if difficulty_mode:
                            spawn_distractor()
                        
                        if score >= DISTRACTOR_SPAWN_THRESHOLD and \
                           score - last_spawn_score >= DISTRACTOR_SPAWN_THRESHOLD:
                            for _ in range(DISTRACTORS_PER_SPAWN):
                                spawn_distractor()
                            last_spawn_score = score
                
                # Check distractor clicks.
                else:
                    for d in distractors:
                        if d[0].collidepoint(mouse_pos):
                            lives -= 1
                            if lives <= 0:
                                game_state = "gameover"
                                high_score = max(high_score, score)
                            break
        
        # PAUSED STATE
        # Pressing "P" toggles back to play; "ESC" returns to main menu.
        elif game_state == "paused":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    game_state = "start"
    
        # BREAK STATE
        # Break suggestion after 90 seconds.
        elif game_state == "break_suggestion":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Define clickable button areas for "Take a Break" and "Continue".
                take_break_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 140, 50)
                continue_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 80, 140, 50)
                
                # Player chose to take a break, then return to start menu.
                if take_break_rect.collidepoint(mouse_pos):
                    game_state = "start"

                # Player chose to continue, then activate the difficulty mode.
                elif continue_rect.collidepoint(mouse_pos):
                    difficulty_mode = True
                    double_click_action = True
                    # Reset timer for another 90 seconds session.
                    session_start_time = time.time()
                    time_remaining = ENGAGEMENT_PERIOD
                    game_state = "playing"
        
        # GAME OVER STATE
        # Click or press "ESC" to return to main menu; saves high score.
        elif game_state == "gameover":
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "start"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "start"

    # ----------------------------------------
    # 2. GAME LOGIC
    # ----------------------------------------
    # Updates positions of moving elements.
    if game_state == "playing":
        move_distractors()

        # Timer Display: update countdown.
        if session_start_time is not None:
            elapsed = time.time() - session_start_time
            time_remaining = max(0, ENGAGEMENT_PERIOD - elapsed)
        
            # Check if time is up.
            if time_remaining <= 0:
                game_state = "break_suggestion"
    
    # ----------------------------------------
    # 3. DRAWING
    # ----------------------------------------
    # Displays title, instructions, and high score.
    if game_state == "start":
        draw_text("COOKIE CLICKER CHALLENGE", 60, BLACK, 
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120, center=True)
        draw_text("Click the golden cookies, avoid the burnt ones!", 30, GRAY,
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, center=True)
        draw_text("Click anywhere to start", 40, BLACK,
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, center=True)
    
        if high_score > 0:
            draw_text(f"High Score: {high_score}", 36, GOLD,
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120, center=True)
    
    elif game_state == "playing":
        # Draw cookie.
        screen.blit(cookie_img, cookie_rect)
        
        # Draw distractors.
        for d in distractors:
            screen.blit(d[3], d[0])
        
        # Draw HUD (score, lives, controls).
        draw_text(f"Score: {score}", 32, BLACK, 20, 20)
        draw_text(f"Lives: {lives}", 32, RED if lives == 1 else BLACK, 20, 60)
        draw_text("P: Pause | ESC: Menu", 24, GRAY, SCREEN_WIDTH - 240, 20)

        # Timer display and show countdown.
        timer_color = RED if time_remaining <= 10 else BLACK
        draw_text(f"Time: {int(time_remaining)}s", 36, timer_color, 20, 100)
        
        # Draw progress hint.
        if score < DISTRACTOR_SPAWN_THRESHOLD:
            draw_text(f"Score {DISTRACTOR_SPAWN_THRESHOLD} to spawn distractors!", 
                     24, GRAY, SCREEN_WIDTH // 2, 20, center=True)

    # Draw "paused" text.
    elif game_state == "paused":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        draw_text("PAUSED", 80, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, center=True)
        draw_text("P: Continue | ESC: Menu", 40, WHITE,
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, center=True)

    # This state appears after 90 seconds of continuous play.
    elif game_state == "break_suggestion":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Generate the message showing how many cookies the player collected.
        message = break_message(score)
        
        # Display the main break suggestion texts.
        draw_text("TIME'S UP!", 70, GOLD, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, center=True)
        draw_text(message, 26, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70, center=True)
        draw_text("Do you want a break?", 30, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, center=True)
        
        # Define clickable button areas for "Take Break" and "Continue".
        take_break_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 140, 50)
        continue_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 80, 140, 50)
        
        # Draw button text labels on top of invisible clickable rectangles.
        draw_text("Take Break", 28, WHITE, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 95, center=True)
        draw_text("Continue", 28, WHITE, SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT // 2 + 95, center=True) 
    
    # Display the Game Over screen when the player runs out of lives.
    elif game_state == "gameover":
        draw_text("GAME OVER", 80, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, center=True)
        draw_text(f"Final Score: {score}", 50, BLACK,
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10, center=True)
        
        # If the player achieved a new high score, then highlight it.
        if score == high_score and score > 0:
            draw_text("NEW HIGH SCORE!", 36, GOLD,
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)
        # Show the guide for how to return to the main menu.
        draw_text("Click or press ESC to return to menu", 32, GRAY,
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, center=True)
    
    # Update the display
    pygame.display.flip()
    
    # ----------------------------------------
    # 4. FRAME RATE
    # ----------------------------------------
    # Control how fast the game runs
    clock.tick(FPS)

# ========================================
# CLEANUP - End the game properly
# ========================================

pygame.quit()
sys.exit()