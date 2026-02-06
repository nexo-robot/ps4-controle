import pygame
import dataclasses
import platform

@dataclasses.dataclass
class mapping_linux:
    buttons: dict = dataclasses.field(default_factory=lambda: {
        0: "Croix",
        1: "Rond",
        2: "Carré",
        3: "Triangle",
        4: "L1",          # Changement ici
        5: "R1",          # Changement ici
        6: "L2_Bouton",   # Note: L2 est souvent un axe ET un bouton sous Linux
        7: "R2_Bouton",
        8: "Partager",    # Share
        9: "Options",
        10: "PS",
        11: "L3",         # Clic joystick gauche
        12: "R3",         # Clic joystick droit
        13: "Touchpad_Clic"
    })
    axes: dict = dataclasses.field(default_factory=lambda: {
        0: "Joystick_G_Horizontal",
        1: "Joystick_G_Vertical",
        2: "L2_Analogique", # Valeur de -32768 à 32767 ou 0 à 1
        3: "Joystick_D_Horizontal",
        4: "Joystick_D_Vertical",
        5: "R2_Analogique"
    })
    hats: dict = dataclasses.field(default_factory=lambda: {
        (0, 1): "Haut",
        (0, -1): "Bas",
        (-1, 0): "Gauche",
        (1, 0): "Droite"
    })


class ps4_controle:
    def __init__(self):
        # Init de pygame
        pygame.init()
        pygame.joystick.init()

        # Init des variable
        self.controller = None
        self.initialized = False

        if platform.system() == "Linux":
            self.__mapping = mapping_linux()

        self.__find_controller()

    def __find_controller(self):
        """Cherche et initialise la première manette disponible."""
        count = pygame.joystick.get_count()
        if count > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            print(f"Manette connectée : {self.controller.get_name()}")
            self.initialized = True
        else:
            print("Aucune manette détectée.")
            self.initialized = False

    def update(self):
        """Récupère les derniers événements de la manette."""
        if not self.initialized:
            return None

        # On vide la file d'attente des événements pygame
        pygame.event.pump()

        data = {
            "buttons": {},
            "axes": {},
            "hats": {}
        }

        # Lecture des boutons
        for i in range(self.controller.get_numbuttons()):
            name = self.__mapping.buttons.get(i, f"Bouton_{i}")
            data["buttons"][name] = self.controller.get_button(i)

        # Lecture des axes (Joysticks et Gâchettes)
        for i in range(self.controller.get_numaxes()):
            name = self.__mapping.axes.get(i, f"Axe_{i}")
            val = self.controller.get_axis(i)
            # On arrondit pour éviter le bruit des capteurs
            data["axes"][name] = round(val, 2)

        # Lecture de la croix directionnelle (Hat)
        for i in range(self.controller.get_numhats()):
            data["hats"][f"Dpad_{i}"] = self.controller.get_hat(i)

        return data

    def debug_print(self, data):
        """Affiche les entrées actives pour le débogage."""
        if not data:
            return

        active_buttons = [name for name, val in data["buttons"].items() if val]

        # On n'affiche que si un joystick bouge de façon significative (> 0.1)
        active_axes = {name: val for name, val in data["axes"].items() if abs(val) > 0.1}

        if active_buttons or active_axes or any(h != (0,0) for h in data["hats"].values()):
            print("-" * 30)
            if active_buttons: print(f"Boutons: {active_buttons}")
            if active_axes: print(f"Axes: {active_axes}")
            for h_name, h_val in data["hats"].items():
                if h_val != (0,0): print(f"{h_name}: {h_val}")
