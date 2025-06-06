from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import random
import math
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scripture-maze-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

# Constants
MAZE_WIDTH = 21
MAZE_HEIGHT = 15
STARTING_HP = 5
SHAKE_DURATION = 60
FLASH_DURATION = 80

# Game states
LOADING = 0
PLAYING = 1
GAME_OVER = 2

class GameState:
    def __init__(self):
        self.shake_frames = 0
        self.flash_frames = 0
        self.hit_points = STARTING_HP
        self.game_state = LOADING
        self.bible_active = False
        self.bom_active = False
        self.won = False
        self.maze = self.generate_maze()
        self.player_pos = [1, 1]

    def generate_maze(self):
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

    def can_move(self, new_pos):
        if (new_pos[0] < 0 or new_pos[0] >= len(self.maze) or 
            new_pos[1] < 0 or new_pos[1] >= len(self.maze[0])):
            return False
        
        cell = self.maze[new_pos[0]][new_pos[1]]
        return cell != 1 and cell != 2

    def handle_collision(self):
        self.hit_points -= 1
        self.shake_frames = SHAKE_DURATION
        self.flash_frames = FLASH_DURATION
        if self.hit_points <= 0:
            self.game_state = GAME_OVER

    def reset(self):
        self.__init__()

    def get_state(self):
        return {
            'maze': self.maze,
            'player_pos': self.player_pos,
            'hit_points': self.hit_points,
            'game_state': self.game_state,
            'bible_active': self.bible_active,
            'bom_active': self.bom_active,
            'won': self.won,
            'shake_frames': self.shake_frames,
            'flash_frames': self.flash_frames
        }

# Global game state
game = GameState()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('game_state', game.get_state())

@socketio.on('start_game')
def handle_start():
    game.game_state = PLAYING
    emit('game_state', game.get_state(), broadcast=True)

@socketio.on('restart_game')
def handle_restart():
    game.reset()
    game.game_state = PLAYING
    emit('game_state', game.get_state(), broadcast=True)

@socketio.on('toggle_bible')
def handle_toggle_bible():
    game.bible_active = not game.bible_active
    emit('game_state', game.get_state(), broadcast=True)

@socketio.on('toggle_bom')
def handle_toggle_bom():
    game.bom_active = not game.bom_active
    emit('game_state', game.get_state(), broadcast=True)

@socketio.on('move_player')
def handle_move(data):
    if game.game_state != PLAYING or game.won:
        return
    
    direction = data['direction']
    new_pos = game.player_pos.copy()
    
    if direction == 'left':
        new_pos[1] -= 1
    elif direction == 'right':
        new_pos[1] += 1
    elif direction == 'up':
        new_pos[0] -= 1
    elif direction == 'down':
        new_pos[0] += 1
    
    if not game.can_move(new_pos):
        game.handle_collision()
    else:
        game.player_pos = new_pos
        if game.maze[game.player_pos[0]][game.player_pos[1]] == 4:
            game.won = True
    
    emit('game_state', game.get_state(), broadcast=True)

@socketio.on('update_effects')
def handle_update_effects():
    # Update effect timers
    if game.shake_frames > 0:
        game.shake_frames -= 1
    if game.flash_frames > 0:
        game.flash_frames -= 1
    
    emit('game_state', game.get_state(), broadcast=True)

if __name__ == '__main__':
    # Production-ready configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('ENVIRONMENT') == 'development'
    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True) 