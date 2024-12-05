import tkinter as tk
import numpy as np

# Constants
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 20
JUMP_HEIGHT = 150
GRAVITY = 1
SPEED = 5
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 20

# Global variables (initialized later)
x = None
y = None
y_velocity = None
obstacles = []
game_over = False
GROUND_LEVEL = None
CANVAS_WIDTH = None   
CANVAS_HEIGHT = None

# Create window and canvas (deferring dimension calculations)
window = tk.Tk()
window.title("Tap to Jump")
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

# Function to initialize game variables AFTER window is ready
def init_game():
    global x, y, y_velocity, GROUND_LEVEL, CANVAS_WIDTH, CANVAS_HEIGHT

    # Get accurate dimensions
    CANVAS_WIDTH = canvas.winfo_width()
    CANVAS_HEIGHT = canvas.winfo_height()
    GROUND_LEVEL = CANVAS_HEIGHT - BALL_RADIUS 

    # Initialize ball position and velocity
    x = 50
    y = GROUND_LEVEL
    y_velocity = 0

    # Create ball
    canvas.coords(ball, x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS)

    # Start spawning obstacles
    spawn_obstacle()
    update()

# Create ball (initially out of view)
ball = canvas.create_oval(0, 0, 0, 0, fill="red")

# Function to spawn obstacles
def spawn_obstacle():
    global obstacles, game_over, GROUND_LEVEL
    x = CANVAS_WIDTH
    y = GROUND_LEVEL - OBSTACLE_HEIGHT // 2 
    obstacles.append(canvas.create_rectangle(x, y, x + OBSTACLE_WIDTH, y + OBSTACLE_HEIGHT, fill="black"))
    if not game_over:
        window.after(2000, spawn_obstacle)

# Function to check for collisions
def check_collision():
    global x, y, obstacles
    for obstacle in obstacles:
        x1, y1, x2, y2 = canvas.coords(obstacle)
        if x1 < x < x2 and y1 < y < y2:
            return True
    return False

# Function to update game state
def update():
    global y, y_velocity, game_over, GROUND_LEVEL
    y_velocity += GRAVITY
    y += y_velocity
    canvas.move(ball, SPEED, y_velocity)

    # Move obstacles and remove off-screen ones
    for obstacle in obstacles:
        canvas.move(obstacle, -SPEED, 0)
        if canvas.coords(obstacle)[0] < -OBSTACLE_WIDTH:
            canvas.delete(obstacle)
            obstacles.remove(obstacle)

    # Check if the ball is below ground level
    if y > GROUND_LEVEL:
        y = GROUND_LEVEL
        y_velocity = 0  

    if check_collision():
        game_over = True

    if not game_over:
        window.after(20, update)

# Function to handle tap/click event
def jump(event):
    global y_velocity, game_over, GROUND_LEVEL
    if not game_over and y == GROUND_LEVEL:
        y_velocity = -JUMP_HEIGHT

# Bind tap/click event to jump function
canvas.bind("<Button-1>", jump)

# Start game AFTER window is fully realized
window.after(100, init_game)  
window.mainloop()
