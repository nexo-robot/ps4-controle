import pygame
import os

MAP_BUTTONS = {
    0: "CROSS",
    1: "CIRCLE",
    2: "SQUARE",
    3: "TRIANGLE",
    4: "SHARE",
    5: "PS",
    6: "OPTIONS",
    7: "L3",
    8: "R3",
    9: "L1",
    10: "R1",
    11: "UP",
    12: "DOWN",
    13: "LEFT",
    14: "RIGHT",
    15: "TOUCHPAD"
}

MAP_AXES = {
    0: "LEFT_X",
    1: "LEFT_Y",
    2: "RIGHT_X",
    3: "RIGHT_Y",
    4: "L2",
    5: "R2"
}

class ps4_controle:
    def __init__(self, joystick_id=0, deadzone=0.1):
        if "SDL_VIDEODRIVER" not in os.environ:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        # 2. Initialisation de Pygame
        if not pygame.get_init():
            pygame.init()

        if not pygame.joystick.get_init():
            pygame.joystick.init()

        self.__joystick = None
        self.__id = joystick_id
        self.__deadzone = deadzone

        # États actuels (C'est ici qu'on lit les valeurs pour le robot)
        self.__buttons = {name: False for name in MAP_BUTTONS.values()}
        self.__axes = {name: 0.0 for name in MAP_AXES.values()}
        self.__hats = (0, 0)

        self.__events = []

        self.__initialize_joystick()

    def __initialize_joystick(self):
        pygame.event.pump() # Rafraîchir l'état interne de pygame
        if pygame.joystick.get_count() > self.__id:
            self.__joystick = pygame.joystick.Joystick(self.__id)
        else:
            pass

    def __handle_event(self, event):
        # Gestion de la connexion à chaud
        if event.type == pygame.JOYDEVICEADDED:
            if self.__joystick is None:
                self.__initialize_joystick()
            return

        # Vérifie si l'événement appartient à cette manette
        if not self.__joystick or (hasattr(event, 'joy') and event.joy != self.__joystick.get_id()):
            return

        # --- Boutons ---
        if event.type == pygame.JOYBUTTONDOWN:
            name = MAP_BUTTONS.get(event.button, f"BTN_{event.button}")
            self.__buttons[name] = True
            self.__events.append(name)

        elif event.type == pygame.JOYBUTTONUP:
            name = MAP_BUTTONS.get(event.button, f"BTN_{event.button}")
            self.__buttons[name] = False

        # --- Axes ---
        elif event.type == pygame.JOYAXISMOTION:
            name = MAP_AXES.get(event.axis)
            if name:
                val = event.value
                # Zone morte pour les sticks
                if "LEFT" in name or "RIGHT" in name:
                    if abs(val) < self.__deadzone:
                        val = 0.0
                self.__axes[name] = val

        # --- Croix directionnelle ---
        elif event.type == pygame.JOYHATMOTION:
            self.__hats = event.value
            self.__on_hat_motion(event.value)

        # --- Déconnexion ---
        elif event.type == pygame.JOYDEVICEREMOVED:
            if self.__joystick and event.instance_id == self.__joystick.get_instance_id():
                self.__joystick = None

    def __on_hat_motion(self, value):
        self.__events.append(("HAT", value))

    def update(self):

        for event in pygame.event.get():
            self.__handle_event(event)

    def getEvent(self):
        return self.__events

    def clearEvent(self):
        self.__events.clear()

    def getAxes(self):
        return self.__axes

    def getButtons(self):
        return self.__buttons

    def getHats(self):
        return self.__hats
