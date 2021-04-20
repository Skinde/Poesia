import pygame

#TODO:Make an actual map of key to action

class keys_handler:
    game_reference = None

    map_of_down_keys = {
        pygame.K_w: "walk_up",
        pygame.K_a: "walk_left",
        pygame.K_s: "walk_down",
        pygame.K_d: "walk_right"
    }

    map_of_up_keys = {
        pygame.K_w: "stop_up",
        pygame.K_a: "stop_left",
        pygame.K_s: "stop_down",
        pygame.K_d: "stop_right"
    }

    stack_of_last_pressed = []
    #TODO: Make a map of keys to function

    def __init__(self, game_ref):
        self.game_reference = game_ref
    def key_down_handle(self, key):
        def phase3():
            if key in self.map_of_down_keys:
                player = self.game_reference.actors["player"]
                player.current_animation = self.map_of_down_keys[key]
                if key == pygame.K_d or key == pygame.K_a:
                    player.speed_x = player.max_x_speed*(key == pygame.K_d) - player.max_x_speed*(key == pygame.K_a)
                if key == pygame.K_w or key == pygame.K_s:
                    player.speed_y = player.max_y_speed*(key == pygame.K_s) - player.max_y_speed*(key == pygame.K_w)
                self.stack_of_last_pressed.append(key)
        locals()["phase"+self.game_reference.phase]()

    def key_up_handle(self, key):
        def phase3():
            if key in self.map_of_up_keys:
                player = self.game_reference.actors["player"]
                self.stack_of_last_pressed.remove(key)
                if player.current_animation == self.map_of_down_keys[key]:
                    player.current_animation = self.map_of_up_keys[key]
                if self.stack_of_last_pressed:
                    player.current_animation = self.map_of_down_keys[self.stack_of_last_pressed[-1]]
                player.speed_x = player.speed_x + (player.max_x_speed*(player.speed_x == -1*player.max_x_speed and key == pygame.K_a) -1*(player.max_x_speed*(player.speed_x == player.max_x_speed and key == pygame.K_d)))
                player.speed_y = player.speed_y + (player.max_y_speed*(player.speed_y == -1*player.max_y_speed and key == pygame.K_w) -1*(player.max_y_speed*(player.speed_y == player.max_y_speed and key == pygame.K_s)))
        locals()["phase"+self.game_reference.phase]()
            