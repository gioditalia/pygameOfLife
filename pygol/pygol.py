""" pyGOL.py
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
import time
import pygame
import numpy as np
import core

class pyGOL:

    def __init__(self, X, Y, size, fullscreen=True):
        self.__X = X
        self.__Y = Y
        self.__size = size
        self.__cells_color = (150, 150, 150) #when active (255, 255, 255)
        self.__bg_color = (0, 0, 0)
        self.__grid_color = (150, 0, 50)
        self.__fullscreen = fullscreen
        self.__run = False  #evolve?
        self.__gen_sleep = 0.5  #T(period) to the next generation
        self.__gen_counter = 0  #Number of generation passed

    def on_init(self):
        pygame.init()
        self.__running = True
        if self.__fullscreen:
            self.__display = pygame.display.set_mode(self.__size,
                                                     pygame.DOUBLEBUF|
                                                     pygame.HWSURFACE|
                                                     pygame.FULLSCREEN, 16)
        else:
            self.__display = pygame.display.set_mode(self.__size,
                                                     pygame.DOUBLEBUF|
                                                     pygame.HWSURFACE, 16)
        self.__gridCalc()
        self.__GOL = core.gameOfLife(self.__X, self.__Y)

        self.__font_info = pygame.font.SysFont("calibri", 22)

    def on_event(self,  event):
        #quit
        if event.type == pygame.QUIT:
            self.__running = False
        #toggle cells by mouse pression
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in xrange(0, len(self.row_pos)):
                if self.row_pos[i] >= event.pos[1]:
                    break
            for j in xrange(0, len(self.col_pos)):
                if self.col_pos[j] >= event.pos[0]:
                    break
            if not self.__matrix[i][j]:
                self.__GOL.setCell(j, i, 1)
            else:
                self.__GOL.setCell(j, i, 0)
            self.on_render()
        #keydown
        elif event.type == pygame.KEYDOWN:
                #start/stop
            if event.key == pygame.K_s:
                if self.__run:
                    self.__stopEvolving()
                else:
                    self.__startEvolving()
            #clear all grid
            elif event.key == pygame.K_c:
                self.__GOL.clearGrid()
            #increase period for next generation
            elif event.key == pygame.K_PLUS:
                self.__gen_sleep = self.__gen_sleep+0.05
            #decrease period for next generation
            elif event.key == pygame.K_MINUS:
                if self.__gen_sleep > 0.06:
                    self.__gen_sleep = self.__gen_sleep-0.05
            #quit
            elif event.key == pygame.K_ESCAPE:
                self.__running = False

    def on_loop(self):
        #evolve to next generation
        if self.__run:
            time.sleep(self.__gen_sleep)
            self.__GOL.evolve()
            #check if all cell was died
            if np.all(self.__matrix == 0):
                self.__stopEvolving()
            else:
                self.__gen_counter = self.__gen_counter+1

    def on_render(self):
        #draw background
        pygame.draw.rect(self.__display,  self.__bg_color,
                         [0, 0, self.__size[0], self.__size[1]])
        #draw matrix
        self.__drawMatrix()
        #draw grid
        for row in self.row_pos:
            pygame.draw.line(self.__display, self.__grid_color, (0, row),
                             (self.__size[0], row))
        for col in self.col_pos:
            pygame.draw.line(self.__display, self.__grid_color, (col, 0),
                             (col, self.__size[1]))
        #draw info
        self.__display.blit(self.__font_info.render("Generation: " +
                             str(self.__gen_counter),  True, (0, 255, 0)), (100, 15))
        self.__display.blit(self.__font_info.render("T(period): " +
                             str(self.__gen_sleep),  True, (0, 255, 0)), (300, 15))
        self.__display.blit(self.__font_info.render("Start/Stop : s",
                             True, (0, 255, 255)), (500, 15))
        self.__display.blit(self.__font_info.render("Clear : c",
                             True, (0, 255, 255)), (500, 35))
        self.__display.blit(self.__font_info.render("Reduce/Increase T:  -/+",
                             True, (0, 255, 255)), (500, 55))

        pygame.display.update()


    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.__running = False

        while( self.__running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def __gridCalc(self):
        #set space from rows and columns
        self.__rect_length = self.__size[0]/self.__X
        self.__rect_width = self.__size[1]/self.__Y

        #calculate position of every rows and store it in array
        row_pos = 0
        self.row_pos = []
        for i in xrange(0, self.__Y):
            row_pos += self.__rect_width
            self.row_pos.append(row_pos)

        #calculate position of every columns and store it in array
        col_pos = 0
        self.col_pos = []
        for i in xrange(0, self.__X):
            col_pos += self.__rect_length
            self.col_pos.append(col_pos)

    def __drawMatrix(self):
        #retrieve current state of grid
        self.__matrix = self.__GOL.getGrid()
        #for evert rows and columns if 1(alive) draw a rect
        for i in range(0, len(self.__matrix)):
            for j in range(0, len(self.__matrix[i])):
                if self.__matrix[i][j] == 1:
                    pygame.draw.rect(self.__display,  self.__cells_color,
                                     [
                                      self.col_pos[j]-self.__rect_length,
                                      self.row_pos[i]-self.__rect_width,
                                      self.__rect_length,
                                      self.__rect_width
                                     ]
                                    )

    def __startEvolving(self):
        self.__run = True
        self.__cells_color = (255, 255, 255)
        self.__gen_counter = 0

    def __stopEvolving(self):
        self.__run = False
        self.__cells_color = (150, 150, 150)

if __name__ == "__main__" :
    # TODO: manage argv for rows, columns,  size and fullscreen
    app = pyGOL(192, 108, (1920, 1080))
    app.on_execute()
