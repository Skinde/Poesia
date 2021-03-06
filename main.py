import poesia
import pygame 

#Defines the width and height of the window
poesia.configuration.width = 900
poesia.configuration.height = 800


#This dictionaty defines the animation's starting [x,y,number_of_frames] in the Sprites/player.png image
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

#Create the new player
Player = poesia.game.add_actor("Sprites/player.png", player_animations, 64, 64)
Player.current_animation = "default"
Player.animation_play = True


#Define it's movement
def move_player_right():
    if Player.speed_x < 1:
        Player.current_animation = "walk_right"
        Player.speed_x = 1

def stop_moving_player_right():
    if Player.speed_x > 0:
        Player.current_animation = "stop_right"
        Player.speed_x = 0

def move_player_left():
    if Player.speed_x > -1:
            Player.current_animation = "walk_left"
            Player.speed_x = -1

def stop_moving_player_left():
    if Player.speed_x < 0:
        Player.current_animation = "stop_left"
        Player.speed_x = 0

def move_player_up():
    if Player.speed_y > -1:
        Player.current_animation = "walk_up"
        Player.speed_y = -1

def stop_moving_player_up():
    if Player.speed_y < 0:
        Player.current_animation = "stop_up"
        Player.speed_y = 0

def move_player_down():
    if Player.speed_y < 1:
        Player.current_animation = "walk_down"
        Player.speed_y = 1

def stop_moving_player_down():
    if Player.speed_y > 0:
        Player.current_animation = "stop_down"
        Player.speed_y = 0

#Map the key press to the function
poesia.keyboard_handler.map_key_press(pygame.K_d, move_player_right)
poesia.keyboard_handler.map_key_release(pygame.K_d, stop_moving_player_right)
poesia.keyboard_handler.map_key_press(pygame.K_a, move_player_left)
poesia.keyboard_handler.map_key_release(pygame.K_a, stop_moving_player_left)
poesia.keyboard_handler.map_key_press(pygame.K_w, move_player_up)
poesia.keyboard_handler.map_key_release(pygame.K_w, stop_moving_player_up)
poesia.keyboard_handler.map_key_press(pygame.K_s, move_player_down)
poesia.keyboard_handler.map_key_release(pygame.K_s, stop_moving_player_down)


#Ready, start the game!
poesia.init()