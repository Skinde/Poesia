import pygame
from config import config
from event_handler import event_handler
from game import game

pygame.init()

conf = config()
game = game(conf)
background = pygame.Surface((conf.width, conf.height))
background.fill(pygame.Color('#000000'))
e_handler = event_handler(conf, game)




while conf.is_running:
    for event in pygame.event.get():
        e_handler.handle(event)
    conf.window.fill((0,0,0))
    game.update()
    game.draw()
    pygame.display.update()