from ps4_controle import ps4_controle
import time

def main():
    if __name__ == "__main__":
        # Exemple d'utilisation
        ps4 = ps4_controle()

        if ps4.initialized:
            print("Lecture de la manette démarrée (Ctrl+C pour arrêter)...")
            try:
                while True:
                    etat = ps4.update()
                    ps4.debug_print(etat)
                    time.sleep(0.05) # Petite pause pour ne pas saturer le CPU
            except KeyboardInterrupt:
                print("\nArrêt du programme.")
        else:
            print("Veuillez brancher une manette et relancer le script.")

if __name__ == "__main__":
    main()
