import pygame
import sys
import requests
from PIL import Image

# Download the image
url = 'https://t4.ftcdn.net/jpg/02/35/01/83/360_F_235018350_NwKA1B9koCLcptK9P1B4WznO19dIQPhe.jpg'
response = requests.get(url)
image_file = 'background_layer1.jpg'

with open(image_file, 'wb') as file:
    file.write(response.content)

# Resize the image to fit the screen
image = Image.open(image_file)
image = image.resize((800, 600), Image.Resampling.LANCZOS)
image.save(image_file)

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tap to Bounce")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and optimize the background image
background_image = pygame.image.load(image_file).convert()

# Game variables
ball_pos = [100, 300]
ball_radius = 20
ball_speed = [5, 0]
gravity = 0.5
jump_strength = -10
is_jumping = False
camera_offset = 0

# Clock for controlling frame rate
clock = pygame.time.Clock()

def draw_ball(screen, ball_pos, camera_offset):
    pygame.draw.circle(screen, BLACK, (ball_pos[0] - camera_offset, ball_pos[1]), ball_radius)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK
        self.speed = 5

    def move(self):
        self.rect.x -= self.speed

    def draw(self, screen, camera_offset):
        pygame.draw.rect(screen, self.color, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

def draw_background(screen, camera_offset):
    offset = camera_offset % SCREEN_WIDTH
    screen.blit(background_image, (-offset, 0))
    screen.blit(background_image, (SCREEN_WIDTH - offset, 0))

def main():
    global is_jumping, ball_speed, camera_offset

    obstacles = [Obstacle(800, SCREEN_HEIGHT - 40, 30, 40)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    ball_speed[1] = jump_strength
                    is_jumping = True

        # Apply gravity
        ball_speed[1] += gravity
        ball_pos[1] += int(ball_speed[1])
        ball_pos[0] += ball_speed[0]

        # Move the camera
        camera_offset = ball_pos[0] - 100

        # Check if the ball is on the ground
        if ball_pos[1] >= SCREEN_HEIGHT - ball_radius:
            ball_pos[1] = SCREEN_HEIGHT - ball_radius
            ball_speed[1] = 0
            is_jumping = False

        # Move and add obstacles
        for obstacle in obstacles:
            obstacle.move()
            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)
                obstacles.append(Obstacle(800 + camera_offset, SCREEN_HEIGHT - 40, 30, 40))

        # Increase obstacle speed over time
        for obstacle in obstacles:
            obstacle.speed += 0.001

        # Check for collisions
        for obstacle in obstacles:
            if pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2).colliderect(obstacle.rect):
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(WHITE)

        # Draw the background
        draw_background(screen, camera_offset)

        # Draw the ball and obstacles
        draw_ball(screen, ball_pos, camera_offset)
        for obstacle in obstacles:
            obstacle.draw(screen, camera_offset)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
