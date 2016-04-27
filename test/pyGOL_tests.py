from nose.tools import *
from pygol.core import *

def test_GOL_blink():
    g = gameOfLife(5,5)    
    grid = g.getGrid()
    #set blink(generation = 1)
    grid[1][2:5] = 1
    #evolve to next generation
    g.evolve()
    #get result
    res = g.getGrid()
    #reset the previous set of grid and configure blink(generation = 2)    
    grid[1][2:5] = 0    
    grid[0][3] = 1
    grid[1][3] = 1
    grid[2][3] = 1
    #check if the result is as expected
    assert np.all(grid==res) == 1
