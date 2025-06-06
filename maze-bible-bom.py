import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (1250, 1000)
CELL_SIZE = 44
MAZE_WIDTH = 21
MAZE_HEIGHT = 15
MAZE_OFFSET_Y = 125
MAZE_OFFSET_X = 63
STARTING_HP = 5

# Effect constants
SHAKE_DURATION = 60
FLASH_DURATION = 80
SHAKE_INTENSITY = 6

# Game states
LOADING = 0
PLAYING = 1
GAME_OVER = 2

# Colors (Plotly-inspired palette)
BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
BLUE = (99, 110, 250)
RED = (239, 85, 59)
GREEN = (0, 204, 150)
YELLOW = (255, 161, 90)
GOLD = (255, 215, 0)
DARK_GREEN = (0, 102, 75)

# Update font sizes (25% larger)
TITLE_FONT_SIZE = 92
NORMAL_FONT_SIZE = 45
HEADER_FONT_SIZE = 60

def generate_maze():
    # Initialize maze with all walls
    maze = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    
    def carve_path(x, y):
        maze[y][x] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT 
                and maze[new_y][new_x] == 1):
                maze[y + dy//2][x + dx//2] = 0
                carve_path(new_x, new_y)
    
    start_x, start_y = 1, 1
    carve_path(start_x, start_y)
    
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                maze[y][x] = random.choice([1, 2])
    
    maze[1][1] = 3  # Start
    maze[MAZE_HEIGHT-2][MAZE_WIDTH-2] = 4  # End
    
    return maze

def can_move(new_pos, maze):
    if (new_pos[0] < 0 or new_pos[0] >= len(maze) or 
        new_pos[1] < 0 or new_pos[1] >= len(maze[0])):
        return False
    
    cell = maze[new_pos[0]][new_pos[1]]
    return cell != 1 and cell != 2

class GameState:
    def __init__(self):
        self.shake_frames = 0
        self.flash_frames = 0
        self.hit_points = STARTING_HP
        self.game_state = LOADING
        self.bible_active = False
        self.bom_active = False
        self.won = False
        self.maze = generate_maze()
        self.player_pos = [1, 1]

    def handle_collision(self):
        self.hit_points -= 1
        self.shake_frames = SHAKE_DURATION
        self.flash_frames = FLASH_DURATION
        if self.hit_points <= 0:
            self.game_state = GAME_OVER

    def reset(self):
        self.__init__()

def apply_screen_shake(surface, game_state):
    if game_state.shake_frames > 0:
        offset_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        offset_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        return surface.copy(), (offset_x, offset_y)
    return surface.copy(), (0, 0)

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("The Strait and Narrow Way")

# Initialize game state
game = GameState()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game.game_state == LOADING:
                game.game_state = PLAYING
                continue
                
            if event.key == pygame.K_r:
                game.reset()
                game.game_state = PLAYING
                continue

            if game.game_state == PLAYING and not game.won:
                if event.key == pygame.K_b:
                    game.bible_active = not game.bible_active
                if event.key == pygame.K_m:
                    game.bom_active = not game.bom_active
                
                new_pos = game.player_pos.copy()
                
                if event.key == pygame.K_LEFT:
                    new_pos[1] -= 1
                if event.key == pygame.K_RIGHT:
                    new_pos[1] += 1
                if event.key == pygame.K_UP:
                    new_pos[0] -= 1
                if event.key == pygame.K_DOWN:
                    new_pos[0] += 1
                    
                if not can_move(new_pos, game.maze):
                    game.handle_collision()
                else:
                    game.player_pos = new_pos
                    if game.maze[game.player_pos[0]][game.player_pos[1]] == 4:
                        game.won = True

    # Clear screen
    screen.fill(BLACK)

    if game.game_state == LOADING:
        # Draw loading screen
        title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        subtitle_font = pygame.font.Font(None, NORMAL_FONT_SIZE)
        
        title_text = title_font.render("The Strait and Narrow Way", True, WHITE)
        subtitle_text = subtitle_font.render("Press any key to start", True, WHITE)
        
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 - 50))
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 + 50))
        
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)

    elif game.game_state == PLAYING:
        # Create temporary surface for shake effect
        temp_surface = pygame.Surface(WINDOW_SIZE)
        temp_surface.fill(BLACK)

        # Draw maze and player on temp_surface
        for row in range(len(game.maze)):
            for col in range(len(game.maze[0])):
                x = col * CELL_SIZE + MAZE_OFFSET_X
                y = row * CELL_SIZE + MAZE_OFFSET_Y
                cell = game.maze[row][col]
                
                if cell == 0:
                    pygame.draw.rect(temp_surface, GREY, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 3:
                    pygame.draw.rect(temp_surface, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 4:
                    pygame.draw.rect(temp_surface, GOLD, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 1 and game.bible_active:
                    pygame.draw.rect(temp_surface, RED, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 2 and game.bom_active:
                    pygame.draw.rect(temp_surface, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(temp_surface, GREY, (x, y, CELL_SIZE, CELL_SIZE))

        # Draw player
        player_x = game.player_pos[1] * CELL_SIZE + MAZE_OFFSET_X
        player_y = game.player_pos[0] * CELL_SIZE + MAZE_OFFSET_Y
        pygame.draw.circle(temp_surface, WHITE, (player_x + CELL_SIZE//2, player_y + CELL_SIZE//2), CELL_SIZE//3)

        # Apply screen shake to maze and player
        final_surface, offset = apply_screen_shake(temp_surface, game)
        screen.blit(final_surface, offset)

        # Draw UI elements directly on screen (not affected by shake)
        font = pygame.font.Font(None, NORMAL_FONT_SIZE)
        title_font = pygame.font.Font(None, HEADER_FONT_SIZE)
        
        # Draw title
        title_text = title_font.render("The Strait and Narrow Way", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0]/2, 30))
        screen.blit(title_text, title_rect)
        
        # Draw status indicators with better visibility
        bible_status = "ON" if game.bible_active else "OFF"
        bom_status = "ON" if game.bom_active else "OFF"
        
        bible_text = font.render(f"Bible (B): {bible_status}", True, 
                               RED if game.bible_active else WHITE)
        bom_text = font.render(f"Book of Mormon (M): {bom_status}", True, 
                             BLUE if game.bom_active else WHITE)
        hp_text = font.render(f"Hit Points: {game.hit_points}", True, GREEN)
        
        # Position the text with specific offsets
        screen.blit(bible_text, (MAZE_OFFSET_X, 60))
        screen.blit(bom_text, (WINDOW_SIZE[0] - 300, 60))
        screen.blit(hp_text, (WINDOW_SIZE[0]//2 - 50, 60))

        # Draw "BAD CHOICE" if flash frames active
        if game.flash_frames > 0:
            flash_font = pygame.font.Font(None, TITLE_FONT_SIZE)
            
            # Create the text with a grey shadow
            shadow_text = flash_font.render("BAD CHOICE", True, GREY)
            main_text = flash_font.render("BAD CHOICE", True, WHITE)
            
            # Calculate scale for pulsing effect
            scale = 1 + 0.2 * math.sin(game.flash_frames * 0.5)
            
            # Scale both shadow and main text
            shadow_rect = shadow_text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
            scaled_shadow = pygame.transform.scale(shadow_text, 
                (int(shadow_rect.width * scale), int(shadow_rect.height * scale)))
            scaled_main = pygame.transform.scale(main_text, 
                (int(shadow_rect.width * scale), int(shadow_rect.height * scale)))
            
            # Position both layers
            shadow_rect = scaled_shadow.get_rect(center=(WINDOW_SIZE[0]/2 + 2, WINDOW_SIZE[1]/2 + 2))
            main_rect = scaled_main.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
            
            # Draw directly to screen
            screen.blit(scaled_shadow, shadow_rect)
            screen.blit(scaled_main, main_rect)
            
            game.flash_frames -= 1

        if game.shake_frames > 0:
            game.shake_frames -= 1

        if game.won:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]))
            overlay.fill(BLACK)
            overlay.set_alpha(128)
            screen.blit(overlay, (0, 0))
            
            win_font = pygame.font.Font(None, TITLE_FONT_SIZE)
            small_font = pygame.font.Font(None, NORMAL_FONT_SIZE)
            
            win_text = win_font.render("You Found Christ!", True, YELLOW)
            restart_text = small_font.render("Press R to restart", True, WHITE)
            
            text_rect = win_text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 + 100))
            
            screen.blit(win_text, text_rect)
            screen.blit(restart_text, restart_rect)

    elif game.game_state == GAME_OVER:
        # Draw the maze first
        temp_surface = pygame.Surface(WINDOW_SIZE)
        temp_surface.fill(BLACK)

        # Draw maze and player
        for row in range(len(game.maze)):
            for col in range(len(game.maze[0])):
                x = col * CELL_SIZE + MAZE_OFFSET_X
                y = row * CELL_SIZE + MAZE_OFFSET_Y
                cell = game.maze[row][col]
                
                if cell == 0:
                    pygame.draw.rect(temp_surface, GREY, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 3:
                    pygame.draw.rect(temp_surface, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 4:
                    pygame.draw.rect(temp_surface, GOLD, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 1 and game.bible_active:
                    pygame.draw.rect(temp_surface, RED, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 2 and game.bom_active:
                    pygame.draw.rect(temp_surface, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(temp_surface, GREY, (x, y, CELL_SIZE, CELL_SIZE))

        # Draw player
        player_x = game.player_pos[1] * CELL_SIZE + MAZE_OFFSET_X
        player_y = game.player_pos[0] * CELL_SIZE + MAZE_OFFSET_Y
        pygame.draw.circle(temp_surface, WHITE, (player_x + CELL_SIZE//2, player_y + CELL_SIZE//2), CELL_SIZE//3)

        screen.blit(temp_surface, (0, 0))

        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]))
        overlay.fill(BLACK)
        overlay.set_alpha(128)  # Semi-transparent
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        font = pygame.font.Font(None, TITLE_FONT_SIZE)
        small_font = pygame.font.Font(None, NORMAL_FONT_SIZE)
        
        text1 = font.render("Search, Ponder and Pray", True, WHITE)
        text2 = font.render("and you will find the way", True, WHITE)
        restart_text = small_font.render("Press R to restart", True, WHITE)
        
        text1_rect = text1.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 - 50))
        text2_rect = text2.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 + 50))
        restart_rect = restart_text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 + 150))
        
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
