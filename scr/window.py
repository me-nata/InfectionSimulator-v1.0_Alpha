#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 16:44:07 2021

@author: nataoliveirasousa
"""

from time       import sleep
from tkinter    import *
from population import Population
from individual import Individual
from virus      import Virus
from random     import randint, random
from cell       import *


#adjust window
window_sizex = 1250
window_sizey = 900

root = Tk()
root.title = 'Infection Simulator'
root.geometry(f'{window_sizex}x{window_sizey}')

#canva definitions
canvas_sizex = 900
canvas_sizey = 900

#frames and widgets
frame_canvas = Frame(root)
frame_canvas.place(
                x=0,
                y=0, 
                width=canvas_sizex, 
                height=canvas_sizey)

frame_adjustment = Frame(root)
frame_adjustment.place(
                    x=canvas_sizex, 
                    y=0, 
                    width=window_sizex-canvas_sizex, 
                    height=window_sizey)

canvas = Canvas(
        frame_canvas, 
        width=canvas_sizex, 
        height=canvas_sizey, 
        bg='white')

scale  = Scale(
        frame_adjustment,
        label='speed',
        from_=0, 
        to=5, 
        orient='horizontal', 
        resolution=0.5) 

start  = Button(
            frame_adjustment,
            text='start')

#windows elements
scale.pack()
start.pack()
canvas.pack()

#drawing definitions
square_size=20

#simulator definitions
population = Population((canvas_sizex, canvas_sizey), simulation_square_size=square_size) 
corona     = Virus(infection_rate=8, lethality=10)
cell       = Cells(canvas)

#contamination functions
def initializeSimulation():
    population.initializePopulation()
    corona.infectPopulation(population)
    cell.initializeCells(population=population)
    cell.updateCellsState(population)
    startSimulator()

def startSimulator():
    delay = scale.get()
    start.config(text='restart')

    while not population.virusEradicate() or population.extinctPopulation():
        population.updatePandemicInformation(corona)
        cell.updateCellsState(population=population)
        sleep(delay)
        
    start.config(text='start')


if __name__ == '__main__':
    cell.drawPopulation(square_size=square_size)
    start.config(command=initializeSimulation)

root.mainloop()