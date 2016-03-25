# Implementation of classic arcade game Pong
"""
Clone of classic game "Pong"
"""

import pygame
import random

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'

PADDLE_SPEED = 5
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PADDLE_SIZE = (10, 50)
BALL_SIZE = (30, 30)
BALL_SPEED = 5.0

class Paddle(pygame.sprite.Sprite):
    """
    Class that represents a paddle
    """
    def __init__(self, input_rect, screen_rect, upkey, downkey):
        """
        creates a rectangle with input_rect size to be a game paddle
        """
        pygame.sprite.Sprite.__init__(self)
        if type(input_rect) is type([]) or type(()):
            self.rect = pygame.Rect(input_rect)
            self.rect = self.rect.clamp(screen_rect)
        else:
            self.rect = input_rect.clamp(screen_rect)
        
        size = self.rect.size
        self.image = pygame.Surface(size)
        self.image.fill((255,255,255))
        self.up = upkey
        self.down = downkey
    
    def update(self):
        """
        updates the position of the paddle
        """
        pressed = pygame.key.get_pressed()
        if pressed[self.up]:
           self.rect.move_ip(0, -PADDLE_SPEED)
        if pressed[self.down]:
           self.rect.move_ip(0, PADDLE_SPEED)
    
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
class Ball(pygame.sprite.Sprite):
    """
    Class that represents a ball
    """
    def __init__(self, input_rect, screen_rect, set_speed):
        """
        creates a ball with input_rect size to be the game ball
        set_speed sets the length of the initial velocity vector
        """
        if type(input_rect) is type([]) or type(()):
            self.rect = pygame.Rect(input_rect)
        else:
            self.rect = input_rect.copy()
        self.screen_rect = screen_rect.copy()
        
        size = self.rect.size
        self.image = pygame.Surface(size)
        self.image.fill((255,255,255))
        pygame.sprite.Sprite.__init__(self)
        
        self.start_speed = set_speed
        self.spawn_ball(random.choice((1,-1)))
    
    def spawn_ball(self, direction):
        """ 
        sets speed's x vector at start of first round
        """
        if direction == 'left':
            side = -1
        elif direction == 'right':
            side = 1
        else:
            side = direction
            
        assert side == 1 or side == -1, "input direction must be 'left', 'right', -1, or 1"
        
        self.rect.center = self.screen_rect.center
        self.x_speed = side * (0.3 + (random.random() * 0.1)) * self.start_speed
        self.set_y_start_speed()
        
    def set_y_start_speed(self):
        """
        sets the speed's y vector so that the total speed is set_speed
        yay physics!
        """
        self.y_speed = random.choice((1,-1)) * (((self.start_speed ** 2) - (self.x_speed ** 2)) ** (0.5))
    
    def bounce(self):
        """
        flips the x-speed and speeds up a random amount
        """
        self.x_speed *= (1.1 + (0.1 * random.random()))
        self.x_speed *= (-1)
        self.y_speed *= (0.7 + (0.6 * random.random()))
    
    def update(self):
        """
        updates the ball's position and checks for collisions and scoring
        """
        self.rect.move_ip(self.x_speed, self.y_speed)
    
        if self.rect.top < self.screen_rect.top or self.rect.bottom > self.screen_rect.bottom:
            self.rect.clamp(self.screen_rect)
            self.y_speed *= -1
        
        if self.rect.left < self.screen_rect.left:
            self.spawn_ball(1)
        if self.rect.right > self.screen_rect.right:
            self.spawn_ball(-1)
            

def run_game():
    """
    main pong-clone game loop
    """
    #initialize
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pong Clone')
    clock = pygame.time.Clock()
    
    #background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((20,20,20))
    
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    #sprite creation
    middle = SCREEN_HEIGHT//2 - PADDLE_SIZE[1]//2
    right = SCREEN_WIDTH - PADDLE_SIZE[0]
    left = 0
    left_paddle = Paddle(((left, middle), PADDLE_SIZE), 
                            screen.get_rect(),
                            pygame.K_a, pygame.K_z)
    right_paddle = Paddle(((right, middle), PADDLE_SIZE), 
                            screen.get_rect(),
                            pygame.K_UP, pygame.K_DOWN)
    ball = Ball(((0,0), BALL_SIZE), screen.get_rect(), BALL_SPEED)
    
    all_sprites = pygame.sprite.Group((left_paddle, right_paddle, ball))
    paddles = pygame.sprite.Group((left_paddle, right_paddle))
    
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        
        #update everything
        all_sprites.update()
        if pygame.sprite.spritecollide(ball, paddles, False):
            ball.bounce()
        
        #Draw everything
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
    return None

def main():
    """
    Placeholder for menu launcher~
    """
    run_game()
    return None
    
#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
