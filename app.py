import pygame
from pygame import Rect
from graphics import init_graphics, gameloop
from ParentComponent import ParentComponent

def main(): 
    init_graphics()
    gameloop(ParentComponent())


if __name__ == "__main__":
    main()
