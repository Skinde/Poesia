import pygame

class config:
    width = 800
    window = None
    height = 600
    is_running = True
    background = None
    framerate_limit = 0
    #TODO: Read from a file the correct width and height save user preference
    def __init__(self):
        pygame.display.set_caption('Poesia')
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
