'''
Created on 30.09.2018

@author: PB
'''

import logging
import random

class Cell:
    def __init__(self, x=0, y=0, state=False):
        self.x = x
        self.y = y
        self.state = state
        self.neighbors = {
                "N":  None,
                "NW": None,
                "W":  None,
                "SW": None,
                "S":  None,
                "SE": None,
                "E":  None,
                "NE": None,
                }
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Cell {} initialized: {}".format(id(self), self))

    def __repr__(self):
        return("x={}, y={}, state={}".format(self.x, self.y, self.state))

    def switch_state(self):
        self.state = not self.state
        self.logger.debug("Cell {} switched state to {}".format(id(self), self.state))

    def set_state(self, state):
        self.state = state
        self.logger.debug("Cell {} state set to {}".format(id(self), self.state))

    def set_neighbor(self, direction, cell):
        """Set a neighbor in position relative to this cell.
        Direction is either N, NW, W, SW, S, SE, E, NE.
        """
        self.neighbors[direction] = cell
        self.logger.debug("[{}, {}] located {} of [{}, {}]".format(cell.x, cell.y, direction, self.x, self.y))

    def count_live_neighbors(self):
        n_live_neighbors = sum(1 for x in self.neighbors.values() if x is not None and x.state)
        self.logger.debug("[{}, {}] has {} neighbors".format(self.x, self.y, n_live_neighbors))
        return(n_live_neighbors)

    def set_new_state(self, new_state):
        self.new_state = new_state
        self.logger.debug("[{}, {}] new state {}".format(self.x, self.y, self.new_state))

    def apply_new_state(self):
        self.state = self.new_state
        self.logger.debug("[{}, {}] new state {} applied".format(self.x, self.y, self.state))


class Life:
    directions = {
        "N" : [ 0, +1],
        "NW": [-1, +1],
        "W" : [-1,  0],
        "SW": [-1, -1],
        "S" : [ 0, -1],
        "SE": [+1, -1],
        "E" : [+1,  0],
        "NE": [+1, +1],
        }
    
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Life {} initialized: {}".format(id(self), self))
        self.create_cells()
        self.randomize_cells()
        self.invert_cells()
        self.set_neighbors()

    def __repr__(self):
        return("width={}, height={}".format(self.width, self.height))

    def create_cells(self):
        self.cells = [ [Cell(x, y, False) for y in range(self.height)] for x in range(self.width)]
        self.logger.debug(self.cells)
        self.logger.debug("All cells created")
        
    def randomize_cells(self):
        [ [self.cells[x][y].set_state(bool(random.randint(0, 1))) for x in range(self.width)] for y in range(self.height)]
        self.logger.debug("All cells randomized")

    def invert_cells(self):
        [ [self.cells[x][y].switch_state() for x in range(self.width)] for y in range(self.height)]
        self.logger.debug("All cells inverted")

    def set_neighbors(self):
        for y in range(self.height):
            for x in range(self.width):
                for direction, dxy in self.directions.items():
                    dx = dxy[0]
                    dy = dxy[1]
                    try:
                        if((x+dx)<0 or (y+dy)<0):
                            raise IndexError("Negative index not allowed!")
                        else:
                            self.cells[x+dx][y+dy]
                            self.cells[x][y].set_neighbor(direction, self.cells[x+dx][y+dy])
                    except IndexError:
                        self.logger.debug("No neighbor {} of [{}, {}]".format(direction, x, y))
                        pass

    def next_generation(self):
        for y in range(self.height):
            for x in range(self.width):
                n_live_neighbors = self.cells[x][y].count_live_neighbors()
                if self.cells[x][y].state:
                    # Cell is alive
                    if n_live_neighbors < 2 or n_live_neighbors > 3:
                        self.cells[x][y].set_new_state(False)
                    else:
                        self.cells[x][y].set_new_state(self.cells[x][y].state)
                else:
                    # Cell is dead
                    if n_live_neighbors == 3:
                        self.cells[x][y].set_new_state(True)
                    else:
                        self.cells[x][y].set_new_state(self.cells[x][y].state)
        for y in range(self.height):
            for x in range(self.width):
                self.cells[x][y].apply_new_state()

        
# Not sure how to use this yet...
def mylist(list):
    """Custom list which disallows negative indices.

    Source: https://stackoverflow.com/questions/30649912/how-to-make-python-refuse-negative-index-values
    """
    def __getitem__(self, n):
        if n < 0:
            raise IndexError("Negative index not allowed!")
        return(list.__getitem__(self, n))


def test():
    game = Life(width=2, height=2)
    

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    #c1 = Cell()
    #c2 = Cell()
    #c1.set_neighbor("N", c2)

    game = Life(width=2, height=2)
