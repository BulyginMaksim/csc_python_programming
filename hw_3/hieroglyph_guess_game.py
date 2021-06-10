from graphical_user_interface import GameGUI
from tkinter import Tk


class GuessGame(object):

    def start_game(self):
        """Этот метод отвечает за открытие приложения и начало игры."""
        root = Tk()
        GameGUI(root)
        root.mainloop()

if __name__ == "__main__":
    game = GuessGame()
    game.start_game()
