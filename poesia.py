import pygame
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


    reference_to_conf = None
    actors = []
    current_map = []
    functions = []
    clock = pygame.time.Clock()
    framerate_font = pygame.font.SysFont("Arial", 18)
    back_scenary = None
    
    def __init__(self, ref_to_conf):
        self.reference_to_conf = ref_to_conf


    def update_fps(self):
	    fps = str(int(self.clock.get_fps()))
	    fps_text = self.framerate_font.render(fps, 1, pygame.Color("coral"))
	    return fps_text
    def update_graphics(self):
        for actor in self.actors:
            actor.update_graphics()


    #Updates the game based on it's current phase
    def update(self):
        for function in self.functions:
            function()
        for actor in self.actors:
            actor.update_maths()

    def load(self):
        for actor in self.actors:
            actor.load()
    def draw(self):
        for actor in self.actors:
            #self.reference_to_conf.window.blit(self.back_scenary.current_surface,(0,0))
            self.reference_to_conf.window.blit(actor.current_surface,(actor.relative_x_position, actor.relative_y_position))
            #self.reference_to_conf.window.blit(self.update_fps(), (10,0))
    def add_actor1(self, args):
        new_actor = actor(args[0])
        self.actors.append(new_actor)
        return new_actor
    def add_actor2(self, args):
        new_actor = actor(args[0], args[1])
        self.actors.append(new_actor)
        return new_actor
    def add_actor4(self, args):
        new_actor = actor(args[0], args[1], args[2], args[3])
        self.actors.append(new_actor)
        return new_actor
    def add_actor(self, *args):
        n_of_arguments = len(args)
        map_of_args = {1: self.add_actor1, 2:self.add_actor2, 4:self.add_actor4}
        return map_of_args[n_of_arguments](args)
    


class actor:
    relative_x_position = 0
    relative_y_position = 0
    current_frame = 0
    speed_x = 0
    speed_y = 0
    current_animation = "default"
    current_surface = None
    width = 1
    height = 1
    source_surface = None
    source = None
    default_animation_name = "default"
    animation_play = False
    #Format is line start_x,start_y,frames
    animation_lines = {"default": [0,0,1]}
    def __init__(self, *args):
        n_of_arguments = len(args)
        map_of_inits = {1: self.init_one_argument, 2: self.init_two_arguments, 4: self.init_four_arguments}
        map_of_inits[n_of_arguments](args)

    def init_four_arguments(self, args):
        self.source = args[0]
        self.animation_lines = args[1]
        self.width = args[2]
        self.height = args[3]
        self.current_surface = pygame.Surface((self.width, self.height))

    def init_two_arguments(self, args):
        self.source = args[0]
        self.animation_lines = args[1]
        self.width, self.height = Image.open(self.source).size 
        self.current_surface = pygame.Surface((self.width,self.height))
        
    def init_one_argument(self, args):
        self.source = args[0]
        self.width, self.height = Image.open(self.source).size 
        self.current_surface = pygame.Surface((self.width,self.height))
    
    def load(self):
        self.source_surface = pygame.image.load(self.source).convert_alpha()
        self.current_surface.blit(self.source_surface, (0,0), (self.animation_lines[self.default_animation_name][0], self.animation_lines[self.default_animation_name][1], self.animation_lines[self.default_animation_name][0]+self.width, self.animation_lines[self.default_animation_name][1]+self.height))

    def update_maths(self): 
        self.relative_x_position = self.relative_x_position + self.speed_x
        self.relative_y_position = self.relative_y_position + self.speed_y

    def update_graphics(self):
        if self.animation_play:
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
    print("Poesia 0.1 started")
    while configuration.is_running:
        for event in pygame.event.get():
            event_handler.handle(event)
        configuration.window.fill((0,0,0))
        game.update()
        game.update_graphics()
        game.draw()
        pygame.display.update()


