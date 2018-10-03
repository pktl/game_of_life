import time
import life
import logging
logging.basicConfig(level=logging.WARNING)
width = 50 
height = 50
game = life.Life(width, height)

try:
    while True:
        game.next_generation()
        print("="*(width+2))
        for x in range(width):
            row = ""
            for y in range(height):
                if game.cells[x][y].state:
                    row += "o"
                else:
                    row += " "
            print("|"+row+"|")
        print("="*(width+2))
        time.sleep(0.1)
        print(chr(27) + "[2J")
except KeyboardInterrupt:
    pass

