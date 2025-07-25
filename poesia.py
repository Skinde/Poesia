import pygame
import time
import math
from PIL import Image
from datetime import datetime

pygame.init()

SQUARE_ROOT_OF_TWO = 2**0.5


class config:
    width = 800
    height = 600
    window = None
    is_running = True
    framerate_limit = 0


class camera:
    # This is to make it easier on the user to
    sorting_coordinate = "z-ordered"


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

    # Object Lists
    scene_sprites = []
    functions = []

    # Time Variables
    current_time = 0
    frame_time = 0
    previous_time = 0
    clock = pygame.time.Clock()

    def __init__(self, ref_to_conf, ref_to_camera):
        self.reference_to_conf = ref_to_conf
        self.reference_to_camera = ref_to_camera

    def update_frame_time(self):
        self.current_time = time.time()
        self.frame_time = self.current_time - self.previous_time
        self.previous_time = self.current_time

    def update_graphics(self):
        for sprite in self.scene_sprites:
            sprite.update_graphics(self.frame_time)

    # Updates the game based on it's current phase
    def update(self):
        if self.reference_to_conf.framerate_limit != 0:
            self.clock.tick(self.reference_to_conf.framerate_limit)
        for function in self.functions:
            function()
        for sprite in self.scene_sprites:
                sprite.update_physics(self.frame_time)

    def load(self):
        for sprite in self.scene_sprites:
            sprite.load()

    def draw(self):
        for sprite in self.scene_sprites:
            self.reference_to_conf.window.blit(
                sprite.current_surface,
                (sprite.position_vector[0], sprite.position_vector[1]),
            )

    def add_sprite(self, *args):
        new_sprite = sprite(*args)
        self.scene_sprites.append(new_sprite)
        return new_sprite


# General game sprite class for animations
class sprite:   

    def __init__(
        self,
        image_path=None,
        animation_lines={"default": [0, 0, 1]},
        width=1,
        height=1,
        animation_frame_rate=30,
    ):
        
        # Game Values
        self.position_vector = [0, 0, 0]
        self.speed_vector = [0, 0, 0]
        self.acceleration_vector = [0, 0, 0]

        # Image Values
        self.width = width
        self.height = height
        self.image_path = image_path
        self.source_surface = None

        # Animation Values
        self.animation_play = False
        self.animation_frame_rate = animation_frame_rate
        self.default_animation_name = "default"
        self.current_animation = "default"
        self.current_frame = 0
        self.current_surface = pygame.Surface((self.width, self.height))
        self.animation_lines = animation_lines
        self.inverted_animation_frame_rate = 1.0 / self.animation_frame_rate
        self.cumulated_time_since_last_update = 0

    def load(self):
        self.source_surface = pygame.image.load(self.image_path).convert_alpha()
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

    def update_physics(self, frame_duration_seconds):
        for dimension in range(len(self.speed_vector)):
            self.speed_vector[dimension] += self.acceleration_vector[dimension]*frame_duration_seconds

        for dimension in range(len(self.position_vector)):
            self.position_vector[dimension] += self.speed_vector[dimension]*frame_duration_seconds

    def update_graphics(self, frame_duration_seconds):
        if (
            self.animation_play
            and self.inverted_animation_frame_rate
            <= self.cumulated_time_since_last_update
        ):
            if self.current_frame >= self.animation_lines[self.current_animation][2]:
                self.current_frame = 0
            self.current_surface = pygame.Surface(
                [self.width, self.height], pygame.SRCALPHA, 32
            ).convert_alpha()
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