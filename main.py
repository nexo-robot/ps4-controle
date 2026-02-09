from ps4_controle import *

if __name__ == "__main__":
    controller = ps4_controle(mapping_file="mapping/mapping_raspi.json")

    clock = pygame.time.Clock()
    print("\n--- Écoute des événements (Ctrl+C pour quitter) ---")

    try:
        while True:
            controller.update()

            if controller.getEvent():
                print(f"Events boutons : {controller.getEvent()}")

                controller.clearEvent()

            left_y = controller.getAxes()["LEFT_Y"]
            right_x = controller.getAxes()["RIGHT_X"]

            l2 = controller.getAxes()["L2"]
            r2 = controller.getAxes()["R2"]



            if abs(left_y) > 0.1 or abs(right_x) > 0.1:
                print(f"Pilotage -> Avance: {left_y:.2f} | Tourne: {right_x:.2f}")

            if controller.getButtons()["CROSS"] and controller.getButtons()["OPTIONS"]:
                print("Sortie demandée via manette.")
                break

            clock.tick(20)
    except KeyboardInterrupt:
        print("\nArrêt.")
    finally:
        pygame.quit()
