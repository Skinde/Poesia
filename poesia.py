import pygame
import time
from PIL import Image
from datetime import datetime

pygame.init()

def foo():
    return 0

class config:
    width = 800
    window = None
    height = 600
    is_running = True
    background = None
    framerate_limit = 0
        

class keyboard_handler:
    reference_to_conf = None
    reference_to_game = None
    

    mapped_key_press = {

    }

    mapped_key_release = {

    }

    def __init__(self,ref_to_conf, ref_to_game):
        self.reference_to_conf = ref_to_conf
        self.reference_to_game = ref_to_game

    def handle_key_press(self, key):
        if self.mapped_key_press.get(key):
            self.mapped_key_press[key]()
    def handle_key_release(self, key):
        if self.mapped_key_release.get(key):
            self.mapped_key_release[key]()
    def map_key_press(self, key, function):
        self.mapped_key_press[key] = function
    def map_key_release(self, key, function):
        self.mapped_key_release[key] = function



class event_handler:

    #References to other part of the code
    reference_to_conf = None
    reference_to_game = None
    keyboard_handler = None
    
    def __init__(self,ref_to_conf, ref_to_game, ref_to_keyboard_handler):
        self.reference_to_conf = ref_to_conf
        self.reference_to_game = ref_to_game
        self.keyboard_handler = ref_to_keyboard_handler

    #Define your functions here

    def shutdown(self, event):
            self.reference_to_conf.is_running = False
    
    def keydown(self, event):
        self.keyboard_handler.handle_key_press(event.key)

    def keyup(self, event):
        self.keyboard_handler.handle_key_release(event.key)

    #Map said functions
    mapped_events = {pygame.QUIT: shutdown,
                     pygame.KEYDOWN: keydown,
                     pygame.KEYUP: keyup
                    }

    def handle(self,event):
        if self.mapped_events.get(event.type):
            self.mapped_events[event.type](self, event)

    def map_function(self, PygameEvent, Function):
        mapped_events[PygameEvent] = Function

class game:


    #Class Reference
    reference_to_conf = None
    back_scenary = None

    #Object Lists
    actors = []
    current_map = []
    functions = []
    
    #Time Variables
    current_time = 0
    frames_per_second = 0
    frame_time = 0
    previous_time = 0

   
    
    
    def __init__(self, ref_to_conf):
        self.reference_to_conf = ref_to_conf


    def update_fps(self):
        self.current_time = time.time()
        self.frame_time = self.current_time - self.previous_time
        self.previous_time = self.current_time
        if self.frame_time != 0:
            self.frames_per_second = 1/self.frame_time
        print(self.frames_per_second)
        

    def update_graphics(self):
        for actor in self.actors:
            actor.update_graphics(self.frame_time)


    #Updates the game based on it's current phase
    def update(self):
        for function in self.functions:
            function()
        for actor in self.actors:
            actor.update_maths(self.frame_time)

    def load(self):
        for actor in self.actors:
            actor.load()
    def draw(self):
        for actor in self.actors:
            #self.reference_to_conf.window.blit(self.back_scenary.current_surface,(0,0))
            self.reference_to_conf.window.blit(actor.current_surface,(actor.relative_x_position, actor.relative_y_position))
            #self.reference_to_conf.window.blit(self.update_fps(), (10,0))
    def add_actor(self, *args):
        new_actor = actor(*args)
        self.actors.append(new_actor)
        return new_actor
    
    


class actor:

    #Camarea dependent values
    relative_x_position = 0
    relative_y_position = 0
    relative_speed_x = 0
    relative_speed_y = 0

    #Game Values
    speed_x = 0
    speed_y = 0

    #Image Values
    width = 1
    height = 1

    #Animation Values
    animation_play = False
    animation_speed = 1 #fps the animation should play
    animation_stack = []
    current_animation = "default"
    current_frame = 0
    current_surface = None
    default_animation_name = "default"
    frames_since_last_animation_update = 1
    frames_to_wait_untill_update = 1
    seconds_to_wait = 0
    
    
    
    
    #Pygame Values
    source = None
    source_surface = None   
    
    
    #Format is line start_x,start_y,frames
    animation_lines = {"default": [0,0,1]}
    def __init__(self, source = None, animation_lines = {"default": [0,0,1]}, width = 1, height = 1, animation_speed = 1):
        self.source = source
        self.animation_lines = animation_lines
        self.width = width
        self.height = height
        self.animation_speed = animation_speed
        self.current_surface = pygame.Surface((self.width, self.height))
    
    def load(self):
        self.source_surface = pygame.image.load(self.source).convert_alpha()
        self.current_surface.blit(self.source_surface, (0,0), (self.animation_lines[self.default_animation_name][0], self.animation_lines[self.default_animation_name][1], self.animation_lines[self.default_animation_name][0]+self.width, self.animation_lines[self.default_animation_name][1]+self.height))

    def animation_stack_append(self, animation_name):
        self.animation_stack.append(animation_name)
        self.current_animation = animation_name
    
    def animation_stack_pop(self):
        self.animation_stack.pop()
        if self.animation_stack:
            self.current_animation = self.animation_stack[-1]
    def animation_stack_remove(self, animation_name):
        self.animation_stack.remove(animation_name)
        if self.animation_stack:
            self.current_animation = self.animation_stack[-1]
        else:
            self.current_animation = self.default_animation_name

    def update_maths(self, frame_duration_seconds): 
        self.relative_x_position = self.relative_x_position + self.speed_x*frame_duration_seconds
        self.relative_y_position = self.relative_y_position + self.speed_y*frame_duration_seconds

    def update_graphics(self, frame_duration_seconds):
        
        if frame_duration_seconds != 0:
            self.frames_to_wait_untill_update = 1/(frame_duration_seconds*self.animation_speed)

        if self.animation_play and self.frames_to_wait_untill_update <= self.frames_since_last_animation_update:
            if self.current_frame >= self.animation_lines[self.current_animation][2]:
                self.current_frame = 0
            self.current_surface.fill((0,0,0,0))
            self.current_surface.blit(self.source_surface, (0, 0), (
                self.animation_lines[self.current_animation][0]+(self.width*self.current_frame),
                self.animation_lines[self.current_animation][1],
                self.animation_lines[self.current_animation][0]+self.width*(self.current_frame+1),
                self.animation_lines[self.current_animation][1]+self.height
            ))
            self.current_frame = self.current_frame + 1
            self.frames_since_last_animation_update = 1
        else:
            if self.frames_to_wait_untill_update > self.frames_since_last_animation_update:
                self.frames_since_last_animation_update = self.frames_since_last_animation_update + 1





configuration = config()
game = game(configuration)
keyboard_handler = keyboard_handler(configuration, game)
event_handler = event_handler(configuration, game, keyboard_handler)




def init():
    pygame.display.set_caption('Poesia')
    configuration.window = pygame.display.set_mode((configuration.width, configuration.height), pygame.RESIZABLE)
    background = pygame.Surface((configuration.width, configuration.height))
    background.fill(pygame.Color('#000000'))    
    game.load()
    print("Poesia 0.2 started")
    while configuration.is_running:
        for event in pygame.event.get():
            event_handler.handle(event)
        configuration.window.fill((0,0,0))
        game.update()
        game.update_graphics()
        game.update_fps()
        game.draw()
        pygame.display.update()


