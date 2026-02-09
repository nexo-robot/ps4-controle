import pygame
import os
import time

def main():
    # Configuration de l'environnement pour éviter d'avoir besoin d'un écran
    if "SDL_VIDEODRIVER" not in os.environ:
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    pygame.joystick.init()

    # Vérification de la présence d'une manette
    if pygame.joystick.get_count() == 0:
        print("Aucune manette détectée. Veuillez brancher une manette.")
        try:
            while pygame.joystick.get_count() == 0:
                pygame.joystick.quit()
                pygame.joystick.init()
                time.sleep(1)
        except KeyboardInterrupt:
            return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"\n--- OUTIL DE DÉCOUVERTE DES IDs (Manette: {joystick.get_name()}) ---")
    print("Appuyez sur un bouton ou bougez un joystick pour voir son ID.")
    print("Utilisez ces IDs pour configurer votre fichier mapping.json.")
    print("Appuyez sur Ctrl+C pour quitter.\n")

    try:
        while True:
            # Traitement des événements
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print(f"[BOUTON] ID: {event.button}")
                
                elif event.type == pygame.JOYAXISMOTION:
                    # On filtre le bruit (zone morte) pour ne pas spammer la console
                    # On affiche seulement si la valeur est significative
                    if abs(event.value) > 0.5:
                        print(f"[AXE]    ID: {event.axis}  | Valeur: {event.value:.2f}")
                
                elif event.type == pygame.JOYHATMOTION:
                    print(f"[HAT]    Valeur: {event.value}")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nArrêt du test.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
