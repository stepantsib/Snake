from infrastructure import Infrastructure
from menu import Menu

if __name__ == "__main__":
    infrastructure = Infrastructure()
    menu = Menu(infrastructure)
    menu.run()
