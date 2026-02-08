from ps4_controle import *

if __name__ == "__main__":
    controller = PS4Controller()

    clock = pygame.time.Clock()
    print("\n--- Écoute des événements (Ctrl+C pour quitter) ---")

    try:
        while True:
            # On utilise la méthode update qui vide la file d'attente des événements
            controller.update()

            # 1. Gestion des événements ponctuels (Boutons)
            if controller.events:
                print(f"Events boutons : {controller.events}")
                # Ici, on traiterait les actions "one-shot" (ex: changer de mode, tirer, etc.)
                controller.events.clear()
            
            # 2. Gestion des états continus (Joysticks / Gâchettes) pour le pilotage
            # Pour un robot, on lit la valeur INSTANTANÉE des axes à chaque boucle.
            left_y = controller.axes["LEFT_Y"]
            right_x = controller.axes["RIGHT_X"]
            
            # On affiche seulement si les valeurs sont significatives pour éviter le spam
            if abs(left_y) > 0.1 or abs(right_x) > 0.1:
                print(f"Pilotage -> Avance: {left_y:.2f} | Tourne: {right_x:.2f}")

            # On peut aussi lire l'état directement
            if controller.buttons["CROSS"] and controller.buttons["OPTIONS"]:
                print("Sortie demandée via manette.")
                break

            clock.tick(20) # 20Hz est souvent suffisant pour du contrôle robot
    except KeyboardInterrupt:
        print("\nArrêt.")
    finally:
        pygame.quit()
