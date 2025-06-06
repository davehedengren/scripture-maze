# The Strait and Narrow Way

A maze game about finding the strait and narrow path, built with Python. Available in both desktop (Pygame) and web (Flask) versions!

## How to Play

1. Use the arrow keys to navigate through the maze
2. Toggle the Bible with the 'B' key to reveal red walls
3. Toggle the Book of Mormon with the 'M' key to reveal blue walls
4. Avoid hitting walls or you'll lose hit points
5. Find your way to the gold square to win
6. Press 'R' to restart the game at any time

## Game Elements

- **Green square**: Starting point
- **Gold square**: End goal (Find Christ!)
- **Red walls**: Visible when Bible is active
- **Blue walls**: Visible when Book of Mormon is active  
- **White circle**: Player
- **Hit Points**: Number of times you can hit walls before game over

## Running on Replit (Web Version - Recommended)

### Flask Web Version
1. Create a new Python Repl on [Replit](https://replit.com)
2. Copy the contents of `app.py` into your main.py file
3. Copy the `templates/` folder and its contents
4. Copy the contents of `requirements.txt` into your requirements.txt file
5. Click the **Run** button - Replit will automatically install dependencies and start the web server!
6. Your game will be available at your Repl's web URL

### Desktop Version (Alternative)
1. Copy the contents of `main.py` instead of `app.py`
2. Change deployment type to "Reserved VM (Background Worker)"
3. This version requires a paid Reserved VM plan

## Running Locally

### Web Version (Flask)
1. Make sure you have Python 3.6+ installed
2. Install dependencies:
   ```
   pip install flask flask-socketio python-socketio
   ```
3. Run the web server:
   ```
   python app.py
   ```
4. Open your browser and go to `http://localhost:5000`

### Desktop Version (Pygame)
1. Install pygame:
   ```
   pip install pygame
   ```
2. Run the desktop game:
   ```
   python main.py
   ```

## Game Features

- **Procedurally generated mazes** - each game is different
- **Screen shake effects** when hitting walls
- **Pulsing "BAD CHOICE" flash** for feedback
- **Multiple game states** (loading, playing, game over)
- **Spiritual theme** with Bible and Book of Mormon elements
- **Real-time multiplayer** - multiple people can play the same maze
- **Mobile-friendly** web interface with touch controls

## Controls

### Desktop Version
- **Arrow Keys**: Move player
- **B Key**: Toggle Bible visibility (reveals red walls)
- **M Key**: Toggle Book of Mormon visibility (reveals blue walls)
- **R Key**: Restart game
- **Any Key**: Start game from loading screen

### Web Version
- **Arrow Keys** or **On-screen Buttons**: Move player
- **B Button** or **B Key**: Toggle Bible visibility
- **M Button** or **M Key**: Toggle Book of Mormon visibility
- **Restart Button** or **R Key**: Restart game
- **Start Button** or **Enter/Space**: Start game

## Technical Details

### Web Version (app.py)
- **Flask** web framework
- **Flask-SocketIO** for real-time communication
- **HTML5 Canvas** for game rendering
- **WebSocket** communication between frontend and backend
- **Responsive design** with mobile support

### Desktop Version (main.py)
- **Python 3**
- **Pygame** library
- **Procedural maze generation** algorithm
- **State-based game management**

## File Structure

```
scripture-maze/
├── app.py                 # Flask web version (main file for Replit)
├── main.py               # Pygame desktop version
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── maze-bible-bom.py    # Original game file
```

Perfect for educational purposes, sharing spiritual-themed games, or hosting multiple games on one platform! 