import pygame
from pygame.time import Clock as clock
from pygame.locals import FULLSCREEN
from Component import Component

SPEED = 0.25
WHITE = (255, 255, 255)

heading_font = None
indicator_font = None
screen = None

def init_graphics():
    global screen, heading_font, indicator_font

    pygame.init()
    pygame.display.set_caption("Custom Core")
    screen = pygame.display.set_mode((1366,768))
    heading_font = pygame.font.SysFont(None, 24)
    indicator_font = pygame.font.SysFont(None, 14)


def gameloop(top_component):
    global screen

    screen_position = [0, 0]
    key_state = [False] * 4    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.display.quit()
                exit()
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_state[0] = True
                elif event.key == pygame.K_RIGHT: 
                    key_state[1] = True
                elif event.key == pygame.K_UP: 
                    key_state[2] = True
                elif event.key == pygame.K_DOWN:
                    key_state[3] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_state[0] = False
                elif event.key == pygame.K_RIGHT: 
                    key_state[1] = False
                elif event.key == pygame.K_UP: 
                    key_state[2] = False
                elif event.key == pygame.K_DOWN:
                    key_state[3] = False
       
        dt = clock().tick(60)
        if key_state[0]:
            screen_position[0] -= int(dt * SPEED)
        elif key_state[1]:
            screen_position[0] += int(dt * SPEED)
 
        if key_state[2]:
            screen_position[1] -= int(dt * SPEED)
        elif key_state[3]:
            screen_position[1] += int(dt * SPEED)

        top_component._compute()

        screen.fill(WHITE)
        top_component._render(screen, screen_position)
        pygame.display.update()
        top_component.clear()
