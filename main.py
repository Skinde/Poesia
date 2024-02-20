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
Player = poesia.game.add_actor("Sprites/player.png" , player_animations, 64, 64, 30) 
Player.current_animation = "default"
Player.animation_play = True
Player.speed = 150

Bradd_pitt = poesia.game.add_background_object("Sprites/bradpitt.jpg", 200,100)

def update_animation(last_direction):
    if Player.direction_vector[0] == 0 and Player.direction_vector[1] == 0:
        Player.current_animation = "default"
        if last_direction[0] == 1:
            Player.current_animation = "stop_right"
        if last_direction[0] == -1:
            Player.current_animation = "stop_left"
        if last_direction[1] == 1:
            Player.current_animation = "stop_down"
        if last_direction[1] == -1:
            Player.current_animation = "stop_up"

    if Player.direction_vector[1] == 1:
        Player.current_animation = "walk_down"
    if Player.direction_vector[1] == -1:
        Player.current_animation = "walk_up"
    if Player.direction_vector[0] == 1:
        Player.current_animation = "walk_right"
    if Player.direction_vector[0] == -1:
        Player.current_animation = "walk_left"

def move_player_right():
    last_direction = Player.direction_vector[:]
    Player.direction_vector[0] = 1
    update_animation(last_direction)

def stop_moving_player_right():
    last_direction = Player.direction_vector[:]
    print(last_direction)
    Player.direction_vector[0] = 0
    print(last_direction)
    update_animation(last_direction)
    

def move_player_left():
    last_direction = Player.direction_vector[:]
    Player.direction_vector[0] = -1
    update_animation(last_direction)

def stop_moving_player_left():
    last_direction = Player.direction_vector[:]
    Player.direction_vector[0] = 0
    update_animation(last_direction)

def move_player_up():
    last_direction = Player.direction_vector[:]
    Player.direction_vector[1] = -1
    update_animation(last_direction)
    
def stop_moving_player_up():
    last_direction = Player.direction_vector[:]
    Player.direction_vector[1] = 0
    update_animation(last_direction)
    
def move_player_down():
    last_direction = Player.direction_vector[:]
    Player.direction_vector[1] = 1
    update_animation(last_direction)

def stop_moving_player_down():
    last_direction = Player.direction_vector[:]
    Player.direction_vector[1] = 0
    update_animation(last_direction)
    

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