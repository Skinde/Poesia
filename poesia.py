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
        self.mapped_events[PygameEvent] = Function

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
    accumulated_time = 0
    frame_updates = 0
    frame_time_over_one_second = 0 
    
    
    def __init__(self, ref_to_conf):
        self.reference_to_conf = ref_to_conf


    def update_fps(self):
        self.current_time = time.time()
        self.frame_time = self.current_time - self.previous_time
        self.accumulated_time = self.accumulated_time + self.frame_time
        self.frame_updates = self.frame_updates + 1
        self.previous_time = self.current_time

        if self.accumulated_time > 1:
            self.frame_time_over_one_second = self.accumulated_time/self.frame_updates
            self.accumulated_time = 0
            self.frame_updates = 0
        

    def update_graphics(self):
        for actor in self.actors:
            actor.update_graphics(self.frame_time_over_one_second)


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
            self.reference_to_conf.window.blit(actor.current_surface,(actor.x_position, actor.y_position))
            #self.reference_to_conf.window.blit(self.update_fps(), (10,0))
    def add_actor(self, *args):
        new_actor = actor(*args)
        self.actors.append(new_actor)
        return new_actor
    
    


class actor:

    #Game Values
    x_position = 0
    y_position = 0
    speed_x = 0
    speed_y = 0

    #Image Values
    width = 1
    height = 1

    #Animation Values
    animation_play = False
    animation_speed = 1 #fps the animation should play
    animation_stack = []
    speed_stack_x = []
    speed_stack_y = []
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
        self.inverted_animation_speed = 1/self.animation_speed 
        self.cumulated_time_since_last_update = 0
    
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
        else:
            self.current_animation = self.default_animation_name
        
    def animation_stack_remove(self, animation_name):
        self.animation_stack.remove(animation_name)
        if self.animation_stack:
            self.current_animation = self.animation_stack[-1]
        else:
            self.current_animation = self.default_animation_name

    def speed_stack_x_append(self, speed):
        self.speed_stack_x.append(speed)
        self.speed_x = speed

    def speed_stack_x_remove(self, speed):
        self.speed_stack_x.remove(speed)
        if self.speed_stack_x:
            self.speed_x = self.speed_stack_x[-1]
        else:
            self.speed_x = 0

    def speed_stack_y_append(self, speed):
        self.speed_stack_y.append(speed)
        self.speed_y = speed

    def speed_stack_y_remove(self, speed):
        self.speed_stack_y.remove(speed)
        if self.speed_stack_y:
            self.speed_y = self.speed_stack_y[-1]
        else:
            self.speed_y = 0

    def update_maths(self, frame_duration_seconds): 
        self.x_position = self.x_position + self.speed_x*frame_duration_seconds
        self.y_position = self.y_position + self.speed_y*frame_duration_seconds

    def update_graphics(self, frame_duration_seconds):
        
    
        if self.animation_play and self.inverted_animation_speed <= self.cumulated_time_since_last_update:
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
            self.cumulated_time_since_last_update = 0
        else:
            self.cumulated_time_since_last_update += frame_duration_seconds





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
    print("Poesia 0.2.5 started")
    while configuration.is_running:
        for event in pygame.event.get():
            event_handler.handle(event)
        configuration.window.fill((0,0,0))
        game.update()
        game.update_graphics()
        game.update_fps()
        game.draw()
        pygame.display.update()


