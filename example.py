import blockability
from blockability import *

import pygame
from pygame import *

data_path = os.path.join(".","data")

#change super class to BAGame to allow multiple BAWorlds??
class TheMissingString(BAGame):

    def run():
        pass

def main():
    global game
    game = TheMissingString("TheMissingString")
    game.run()


if __name__ == "__main__":
    main()

