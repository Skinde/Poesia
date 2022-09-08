import poesia
import pygame 

poesia.configuration.width = 900
poesia.configuration.height = 800


#Animation Map for the player stores: [X coordinate of first frame, Y coordinate of first frame, Number of frames]
player_animations = {
                "default": [0,64,1],
                "walk_up": [0,512,9],
                "walk_left": [0,576,9],
                "walk_down": [0,640,9],
                "walk_right": [0,704,9],
                "stop_up": [0,512,1],
                "stop_left": [0,576,1],
                "stop_down": [0,640,1],
                "stop_right": [0,704,1]
            }
        
#Create the "Player Actor" Parameters are: (Path to sprite image, Animations Map, Width, Height, Animation speed In frames per second)
Player = poesia.game.add_actor("Sprites/player.png" , player_animations, 64, 64, 10) 
Player.current_animation = "default"
Player.animation_play = True


def move_player_right():
        Player.animation_stack_append("walk_right")
        Player.speed_x = 150

def stop_moving_player_right():
        Player.animation_stack_remove("walk_right")
        if not Player.animation_stack:
            Player.current_animation = "stop_right"
        Player.speed_x = 0

def move_player_left():
            Player.animation_stack_append("walk_left")
            Player.speed_x = -150

def stop_moving_player_left():
    Player.animation_stack_remove("walk_left")
    if not Player.animation_stack:
        Player.current_animation = "stop_left"
    Player.speed_x = 0

def move_player_up():
    Player.animation_stack_append("walk_up")
    Player.speed_y = -150

def stop_moving_player_up():
    Player.animation_stack_remove("walk_up")
    if not Player.animation_stack:
        Player.current_animation = "stop_up"
    Player.speed_y = 0

def move_player_down():
    Player.animation_stack_append("walk_down")
    Player.speed_y = 150

def stop_moving_player_down():
    Player.animation_stack_remove("walk_down")
    if not Player.animation_stack:
        Player.current_animation = "stop_down"
    Player.speed_y = 0

#Mapping of keypress to function, note that the key pressed can be a variable and changed later on with the same function.
poesia.keyboard_handler.map_key_press(pygame.K_d, move_player_right)
poesia.keyboard_handler.map_key_release(pygame.K_d, stop_moving_player_right)
poesia.keyboard_handler.map_key_press(pygame.K_a, move_player_left)
poesia.keyboard_handler.map_key_release(pygame.K_a, stop_moving_player_left)
poesia.keyboard_handler.map_key_press(pygame.K_w, move_player_up)
poesia.keyboard_handler.map_key_release(pygame.K_w, stop_moving_player_up)
poesia.keyboard_handler.map_key_press(pygame.K_s, move_player_down)
poesia.keyboard_handler.map_key_release(pygame.K_s, stop_moving_player_down)


#Call this function to start the game
poesia.init()
