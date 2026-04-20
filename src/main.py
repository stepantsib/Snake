from src.menu import Menu
from src.infrastructure import Infrastructure

if __name__ == "__main__":
    infrastructure = Infrastructure()
    menu = Menu(infrastructure)
    menu.run()
