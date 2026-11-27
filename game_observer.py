from observer import Observer


class GameObserver(Observer):

    def update(self, event, data=None):
        if event == "score_changed":
            print(f"Score mis à jour : {data}")

        elif event == "player_damaged":
            print(f"Le joueur a perdu une vie. Vie restante : {data}")

        elif event == "game_reset":
            print("Nouvelle partie commencée !")