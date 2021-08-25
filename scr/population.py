#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:55:27 2021

@author: nataoliveirasousa
"""

from virus import Virus
from individual import Individual
from random import random
from math import ceil


class Population:
    def __init__(self, window_canvas_size=(), simulation_square_size=20, social_isolament_rate=20):
        self.population = []
        self._social_isolament_rate = social_isolament_rate
        
        sizex = ceil(window_canvas_size[0]/simulation_square_size)
        sizey = ceil(window_canvas_size[1]/simulation_square_size)

        self.population_size  = sizex*sizey
        print(f'{sizex}x{sizey}')
    
        for x in range(sizex):
            self.population.append([])

            for y in range(sizey):
                self.population[x].append(Individual())

                if self._social_isolament_rate > random()*100:
                    self.population[x][y]._isolated = True


        self.infected        = []
        self._rounds         = 1
        self._death          = []
        self._critical_stage = []
        self._healed         = []
        self._isolated       = []

    def initializePopulation(self):
        i = 0
        for group in self.population:
            j = 0
            for individual in group:
                
                individual.restart()

                if self._social_isolament_rate > random()*100:
                    individual._isolated = True
                    self._isolated.append((i,j),)
    
                j+=1
            i+=1

        self.infected        = []
        self._rounds         = 1
        self._death          = []
        self._critical_stage = []
        self._healed         = []
        self._isolated       = []


    def contactBetweenIndividuals(self, virus, from_individual, to_individual):
        infected = False
        if (from_individual.isAlive() and to_individual.isAlive()):
            if random()*100 <= virus._infection_rate:
                if virus._mask_usage_data:
                    if from_individual.wearingMask() and to_individual.wearingMask():
                        if random()*100 <= virus.rate_infection_mm:
                            from_individual.transmitTo(to_individual)
                            infected = True

                    elif not from_individual.wearingMask() and to_individual.wearingMask():
                        if random()*100 <= virus.rate_infection_wm:
                            from_individual.transmitTo(to_individual)
                            infected = True

                    elif from_individual.wearingMask() and not to_individual.wearingMask():
                        if random()*100 <= virus.rate_infection_mw:
                            from_individual.transmitTo(to_individual)
                            infected = True

                    elif not from_individual.wearingMask() and not to_individual.wearingMask():
                        if random()*100 <= virus.rate_infection_ww:
                            from_individual.transmitTo(to_individual)
                            infected = True
                            
                else:
                    from_individual.transmitTo(to_individual)
                    infected = True
            
        return infected
    
    def virusEradicate(self):
        return (len(self.infected) == 0) and len(self._critical_stage) == 0
        
    def extinctPopulation(self):
        return self.population_size == 0

    def _checkInfection(self, virus=Virus(), contact_probability=70, contact_probability_isolated=30):
        
        new_infected = []

        for coord in self.infected:

            i = coord[0]
            j = coord[1]

            neighbors = [
                (i-1, j+1),
                (i, j+1),
                (i+1, j+1),
                (i+1, j),
                
                (i+1, j-1),
                (i, j-1),
                (i-1, j-1),
                (i-1, j)
            ]

            for coord_neighbors in neighbors:
                if  (coord_neighbors[0] >= 0 and coord_neighbors[0] < len(self.population)) and \
                    (coord_neighbors[1] >= 0 and coord_neighbors[1] < len(self.population[i])):
                    
                    if not self.population[coord_neighbors[0]][coord_neighbors[1]].isContaminated():                        
                  
                        contact = contact_probability
                        if self.population[coord_neighbors[0]][coord_neighbors[1]].isolated():
                            contact = contact_probability_isolated
                  
                        if contact > random()*100:
                            if self.contactBetweenIndividuals(virus, self.population[i][j], 
                                                                self.population[coord_neighbors[0]][coord_neighbors[1]]):

                                new_infected.append((coord_neighbors[0], coord_neighbors[1]), )


        for coord in new_infected:
            self.population[coord[0]][coord[1]]._round_infected = self._rounds
            self.infected.append(coord)

    def _checkCurePopulation(self, virus, recuperation_in_critical_stage):
        for coord_individual in self.infected:
            i = coord_individual[0]
            j = coord_individual[1]

            time_infected = self._rounds - self.population[i][j]._round_infected

            if time_infected * virus.recoveryValue()/virus.lethalityValue() >= random() * 100:
                if self.population[i][j]._critical:
                    
                    critical_time = self._rounds - self.population[i][j]._critical_time

                    if critical_time*recuperation_in_critical_stage > random()*100:
                        self.population[i][j]._critical = False
                        self.population[i][j]._critical_time = 0
                        self._critical_stage.remove(coord_individual)
                    

                else:    
                    self.population[i][j]._toHeal()
                    self.infected.remove(coord_individual)
                    self._healed.append(coord_individual)

    def _checkCriticalWorsening(self):
        for coord_individual in self.infected:

            i = coord_individual[0]
            j = coord_individual[1]

            time_infected = self._rounds - self.population[i][j]._round_infected
            
            if time_infected > random()*100:
                self.population[i][j]._critical = True                
                self.population[i][j]._critical_time = self._rounds
                self._critical_stage.append(coord_individual)

    def _checkDeath(self, virus):
        for coord_individual in self._critical_stage:
            
            i = coord_individual[0]
            j = coord_individual[1]

            critical_time = self._rounds - self.population[i][j]._critical_time

            if virus.lethalityValue()*critical_time > random()*100:
                self.population[i][j]._death()
                self._critical_stage.remove(coord_individual)

                if coord_individual in self.infected:
                    self.infected.remove(coord_individual)
                
                self._death.append(coord_individual)

    def updatePandemicInformation(self, virus, contact_probability=70, 
                                contact_probability_isolated=20, recuperation_in_critical_stage=10):
        
        self._rounds += 1
        self._checkInfection(virus, contact_probability, contact_probability_isolated)
        self._checkCriticalWorsening()
        self._checkCurePopulation(virus, recuperation_in_critical_stage)
        self._checkDeath(virus)
