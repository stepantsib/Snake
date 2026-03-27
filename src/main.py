from game import Game
from infrastructure import Infrastructure

if __name__ == "__main__":
    game = Game(Infrastructure())
    game.loop()