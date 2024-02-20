import pygame
import time
import math
from PIL import Image
from datetime import datetime

pygame.init()

SQUARE_ROOT_OF_TWO = 2**0.5
SQUARE_ROOT_OF_THREE = 3**0.5

class config:
    width = 800
    height = 600
    window = None
    is_running = True
    background = None
    framerate_limit = 0


class camera:
    #This is to make it easier on the user to
    sorting_coordinate = "z-ordered"
    coordinate_map = {
        "x-ordered": 0,
        "y-ordered": 1,
        "z-ordered": 2
    }

    priority_dimension = 0
    def get_coordinate_priority(self):
        return self.coordinate_priority_map[self.order]


class keyboard_handler:

    # References to other part of the code
    reference_to_conf = None
    reference_to_game = None

    mapped_key_press = {}
    mapped_key_release = {}

    def __init__(self, ref_to_conf, ref_to_game):
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

    # References to other part of the code
    reference_to_conf = None
    reference_to_game = None
    keyboard_handler = None

    def __init__(self, ref_to_conf, ref_to_game, ref_to_keyboard_handler):
        self.reference_to_conf = ref_to_conf
        self.reference_to_game = ref_to_game
        self.keyboard_handler = ref_to_keyboard_handler

    # Define your functions here
    def shutdown(self, event):
        self.reference_to_conf.is_running = False

    def keydown(self, event):
        self.keyboard_handler.handle_key_press(event.key)

    def keyup(self, event):
        self.keyboard_handler.handle_key_release(event.key)

    # Map said functions
    mapped_events = {
        pygame.QUIT: shutdown,
        pygame.KEYDOWN: keydown,
        pygame.KEYUP: keyup,
    }

    def handle(self, event):
        if self.mapped_events.get(event.type):
            self.mapped_events[event.type](self, event)

    def map_function(self, PygameEvent, Function):
        self.mapped_events[PygameEvent] = Function


class game:

    # Class Reference
    reference_to_conf = None
    reference_to_camera = None
    back_scenary = None

    # Object Lists
    background_objects = []
    actors = []
    functions = []

    # Time Variables
    current_time = 0
    frame_time = 0
    previous_time = 0

    def __init__(self, ref_to_conf, ref_to_camera):
        self.reference_to_conf = ref_to_conf
        self.reference_to_camera = ref_to_camera

    def update_frame_time(self):
        self.current_time = time.time()
        self.frame_time = self.current_time - self.previous_time
        self.previous_time = self.current_time

    def update_graphics(self):
        for actor in self.actors:
            actor.update_graphics(self.frame_time)

    # Updates the game based on it's current phase
    def update(self):
        for function in self.functions:
            function()
        for actor in self.actors:
            actor.update_values(self.frame_time)

    def load(self):
        for actor in self.actors:
            actor.load()


    def draw(self):
        for background in self.background_objects:
            self.reference_to_conf.window.blit(
                background.current_surface, (background.position_vector[0], background.position_vector[1])
            )
        sorted_actors = self.actors
        for actor in sorted_actors:
            self.reference_to_conf.window.blit(
                actor.current_surface, (actor.position_vector[0], actor.position_vector[1])
            )

    def add_actor(self, *args):
        new_actor = actor(*args)
        self.actors.append(new_actor)
        return new_actor

    def add_background_object(self, *args):
        new_background_object = background_object(*args)
        self.background_objects.append(new_background_object)
        return new_background_object

#Background objects can't interact, can't move, can't be controlled
class background_object:
    # Game Values
    position_vector = [0,0,0]

    # Image Values
    width = 1
    height = 1
    source = None
    source_surface = None
    current_surface = None

    def __init__(
            self,
            source=None,
            width=1,
            height=1,
        ):
            self.source = source
            self.width = width
            self.height = height
            self.current_surface = pygame.image.load(self.source)
        

#Stationary objects can interact, can't move, can't be controlled
class stationary_object:
    position_vector = [0,0,0]

#Props can move interact, can move, can't be controlled
class prop:
    # Game Values
    position_vector = [0,0,0]
    speed_vector = [0,0,0]
    
    # Image Values
    width = 1
    height = 1

#Actors can interact, can move, can be controlled
class actor:

    # Game Values
    position_vector = [0,0,0]
    speed_vector = [0,0,0]
    direction_vector = [0,0,0]
    speed = 100

    # Image Values
    width = 1
    height = 1
    source = None
    source_surface = None

    # Animation Values
    animation_play = False
    animation_frame_rate = 1
    default_animation_name = "default"
    current_animation = "default"
    current_frame = 0
    current_surface = None
    animation_lines = {"default": [0, 0, 1]}

    def __init__(
        self,
        source=None,
        animation_lines={"default": [0, 0, 1]},
        width=1,
        height=1,
        animation_frame_rate=1,
    ):
        self.source = source
        self.animation_lines = animation_lines
        self.width = width
        self.height = height
        self.animation_frame_rate = animation_frame_rate
        self.current_surface = pygame.Surface((self.width, self.height))
        self.inverted_animation_frame_rate = 1 / self.animation_frame_rate
        self.cumulated_time_since_last_update = 0

    def load(self):
        self.source_surface = pygame.image.load(self.source).convert_alpha()
        self.current_surface.blit(
            self.source_surface,
            (0, 0),
            (
                self.animation_lines[self.default_animation_name][0],
                self.animation_lines[self.default_animation_name][1],
                self.animation_lines[self.default_animation_name][0] + self.width,
                self.animation_lines[self.default_animation_name][1] + self.height,
            ),
        )


    def update_values(self, frame_duration_seconds):
        n = self.direction_vector.count(0)
        n = 3 - n
        v = (n == 0) * 0 + (n == 1) * self.speed + (n == 2) * (self.speed / SQUARE_ROOT_OF_TWO)
        for dimension in range(len(self.speed_vector)):
            self.speed_vector[dimension] = v * self.direction_vector[dimension]
        self.position_vector[0] = self.position_vector[0] + self.speed_vector[0] * frame_duration_seconds
        self.position_vector[1] = self.position_vector[1] + self.speed_vector[1] * frame_duration_seconds

    def update_graphics(self, frame_duration_seconds):

        if (
            self.animation_play
            and self.inverted_animation_frame_rate
            <= self.cumulated_time_since_last_update
        ):
            if self.current_frame >= self.animation_lines[self.current_animation][2]:
                self.current_frame = 0
            self.current_surface = pygame.Surface([self.width,self.height], pygame.SRCALPHA, 32).convert_alpha()
            self.current_surface.blit(
                self.source_surface,
                (0, 0),
                (
                    self.animation_lines[self.current_animation][0]
                    + (self.width * self.current_frame),
                    self.animation_lines[self.current_animation][1],
                    self.animation_lines[self.current_animation][0]
                    + self.width * (self.current_frame + 1),
                    self.animation_lines[self.current_animation][1] + self.height,
                ),
            )
            self.current_frame = self.current_frame + 1
            self.cumulated_time_since_last_update = 0
        else:
            self.cumulated_time_since_last_update += frame_duration_seconds


configuration = config()
camera = camera()
game = game(configuration, camera)
keyboard_handler = keyboard_handler(configuration, game)
event_handler = event_handler(configuration, game, keyboard_handler)


def init():
    pygame.display.set_caption("Poesia")
    configuration.window = pygame.display.set_mode(
        (configuration.width, configuration.height), pygame.RESIZABLE
    )
    background = pygame.Surface((configuration.width, configuration.height))
    background.fill(pygame.Color("#000000"))
    game.load()
    print("Poesia 0.2.5 started")
    while configuration.is_running:
        for event in pygame.event.get():
            event_handler.handle(event)
        configuration.window.fill((0, 0, 0))
        game.update()
        game.update_graphics()
        game.update_frame_time()
        game.draw()
        pygame.display.update()
