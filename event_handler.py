from keyboard_event_handler import keys_handler

class event_handler:
    reference_to_conf = None
    reference_to_game = None
    keyboard_handler = None
    def __init__(self,ref_to_conf, ref_to_game):
        self.reference_to_conf = ref_to_conf
        self.reference_to_game = ref_to_game
        self.keyboard_handler = keys_handler(ref_to_game)
    def handle(self,event):
        mapped_events = {256: True, 768: True, 769: True}
        def E256():
            #pygame.QUIT event
            global is_running
            self.reference_to_conf.is_running = False
        def E768():
            #pygame.KEYDOWN event
            self.keyboard_handler.key_down_handle(event.key)
        def E769():
            self.keyboard_handler.key_up_handle(event.key)

        if mapped_events.get(event.type, False):
            locals()['E'+str(event.type)]()