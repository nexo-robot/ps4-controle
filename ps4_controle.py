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

class PS4Controller:
    def __init__(self, joystick_id=0, deadzone=0.1):
        if "SDL_VIDEODRIVER" not in os.environ:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        # 2. Initialisation de Pygame
        if not pygame.get_init():
            pygame.init()

        if not pygame.joystick.get_init():
            pygame.joystick.init()

        self.joystick = None
        self.id = joystick_id
        self.deadzone = deadzone

        # États actuels (C'est ici qu'on lit les valeurs pour le robot)
        self.buttons = {name: False for name in MAP_BUTTONS.values()}
        self.axes = {name: 0.0 for name in MAP_AXES.values()}
        self.hats = (0, 0)
        
        # Liste pour stocker les événements de boutons (Commandes ponctuelles)
        self.events = []

        self._initialize_joystick()

    def _initialize_joystick(self):
        pygame.event.pump() # Rafraîchir l'état interne de pygame
        if pygame.joystick.get_count() > self.id:
            self.joystick = pygame.joystick.Joystick(self.id)
        else:
            pass

    def handle_event(self, event):
        # Gestion de la connexion à chaud
        if event.type == pygame.JOYDEVICEADDED:
            if self.joystick is None:
                self._initialize_joystick()
            return

        # Vérifie si l'événement appartient à cette manette
        if not self.joystick or (hasattr(event, 'joy') and event.joy != self.joystick.get_id()):
            return

        # --- Boutons ---
        if event.type == pygame.JOYBUTTONDOWN:
            name = MAP_BUTTONS.get(event.button, f"BTN_{event.button}")
            self.buttons[name] = True
            self._on_button_down(name)

        elif event.type == pygame.JOYBUTTONUP:
            name = MAP_BUTTONS.get(event.button, f"BTN_{event.button}")
            self.buttons[name] = False
            self._on_button_up(name)

        # --- Axes ---
        elif event.type == pygame.JOYAXISMOTION:
            name = MAP_AXES.get(event.axis)
            if name:
                val = event.value
                # Zone morte pour les sticks
                if "LEFT" in name or "RIGHT" in name:
                    if abs(val) < self.deadzone:
                        val = 0.0
                self.axes[name] = val
                self._on_axis_motion(name, val)

        # --- Croix directionnelle ---
        elif event.type == pygame.JOYHATMOTION:
            self.hats = event.value
            self._on_hat_motion(event.value)

        # --- Déconnexion ---
        elif event.type == pygame.JOYDEVICEREMOVED:
            if self.joystick and event.instance_id == self.joystick.get_instance_id():
                self.joystick = None

    def _on_button_down(self, button_name):
        # On ajoute l'événement bouton car c'est une action ponctuelle
        self.events.append(button_name)

    def _on_button_up(self, button_name):
        pass

    def _on_axis_motion(self, axis_name, value):
        # Pour un robot, on ne stocke pas l'historique des mouvements de joystick.
        # On se contente de mettre à jour self.axes (déjà fait plus haut).
        pass

    def _on_hat_motion(self, value):
        self.events.append(("HAT", value))

    def update(self):
        """
        Méthode utilitaire pour traiter tous les événements en attente d'un coup.
        """
        for event in pygame.event.get():
            self.handle_event(event)
