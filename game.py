import pygame
from drawable import actor, player

pygame.init()
class game:
    reference_to_conf = None
    
    phase = "1"
    actors = {

    }
    n = 0
    current_map = []
    clock = pygame.time.Clock()
    framerate_font = pygame.font.SysFont("Arial", 18)
    
    def __init__(self, ref_to_conf):
        self.reference_to_conf = ref_to_conf
    def update_fps(self):
	    fps = str(int(self.clock.get_fps()))
	    fps_text = self.framerate_font.render(fps, 1, pygame.Color("coral"))
	    return fps_text
    #Updates the game based on it's current phase
    def update(self):
        def phase1():
            #Loads where the player animations (x,y) start from it's source and the number of frames
            player_animations = {
                #default animation is at x:0 y:64 and the number of frames is 1
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
            #Creates a new player with the source image being Sprites/player.png
            #TODO: Replace with os.join
            self.actors["player"] = player(64, 64, player_animations, "Sprites/player", "png", "default")
            #Changes Game Phase from Loading to game loop
            self.phase = "2"
        def phase2():
            self.n = self.n + 1
            #I don't know why but this makes animation framerate stable
            delta_t = self.clock.get_fps()/20
            if self.n >= delta_t or delta_t < 1:
                #Update Graphics for all actors
                for actor in self.actors:
                    real_actor = self.actors[actor]
                    real_actor.update_maths()
                    real_actor.update_graphics()
                self.n = 0
            x = 1
            #Put framerate inside the window
            self.reference_to_conf.window.blit(self.update_fps(), (10,0))
            self.clock.tick(self.reference_to_conf.framerate_limit)
        locals()["phase" + self.phase]()

    def draw(self):
        for actor in self.actors:
            real_actor = self.actors[actor]
            self.reference_to_conf.window.blit(real_actor.current_surface,(real_actor.relative_x_position, real_actor.relative_y_position))

