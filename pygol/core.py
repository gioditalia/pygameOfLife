""" core.py
    Copyright (C) 2016  Giovanni D'Italia

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np

class gameOfLife(object):
    """
    gof implements the evolution's rules of "game of life"
    The __init__ method create an empty grid where place all cells

    Args:
        X (int): X size of array
        Y (int): Y size of array
    """

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.grid = np.zeros((self.Y, self.X), int)


    def evolve(self, generation=1):
        """
        evolve iterate the _evolve method for precise number of generation

        Args:
            generation (int): generation's number who have to elapse
        """
        for i in xrange(0, generation):
            self.setGrid(self.__evolve())

    def __evolve(self):
        """
        _evolve change the grid state from current to next generation
        """
        nbrs_count = sum(np.roll(np.roll(self.grid, i, 0), j, 1)
                         for i in (-1, 0, 1) for j in (-1, 0, 1)
                         if i != 0 or j != 0)
        return (nbrs_count == 3) | (self.grid & (nbrs_count == 2))

    def getGrid(self):
        """
        getGrid return current value of grid
        """
        return self.grid

    def setGrid(self, grid):
        """
        setGrid set a numpy grid passed by arguments

        Args:
            grid (numpy array): numpy grid to set as current grid
        """
        self.grid = grid

    def setCell(self, X, Y, state):
        """
        setCell set the state of one cell

        Args:
            X (int): X index of cell
            Y (int): Y index of cell
            state (int): state of cell (alive/die)-(1/0)
        """

        if X < self.X and Y < self.Y and (state == 0 or state == 1):
            self.grid[Y][X] = state

    def clearGrid(self):
        self.grid = np.zeros((self.Y, self.X), int)
