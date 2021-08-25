#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:02:41 2021

@author: nataoliveirasousa
"""

from random import random, randint

class Virus:
    def __init__(self, infection_rate=5, recovery_rate=20, lethality=20, 
                 rate_infection_mm=100, rate_infection_wm=100,
                 rate_infection_mw=100, rate_infection_ww=100):
        
        self._infection_rate   = infection_rate
        self._recovery_rate    = recovery_rate
        self._lethality        = lethality

        self.rate_infection_mm = rate_infection_mm
        self.rate_infection_wm = rate_infection_wm
        self.rate_infection_mw = rate_infection_mw
        self.rate_infection_ww = rate_infection_ww
    
        self._mask_usage_data =  True
        if self.rate_infection_mm == self.rate_infection_wm == self.rate_infection_mw == self.rate_infection_ww:
            self._mask_usage_data = False


    def infectPopulation(self, population):
        for x in range(randint(1, 5)):
            i = randint(0, len(population.population)-1)
            j = randint(0, len(population.population[i])-1)
                   
            population.population[i][j]._contaminated()
            population.population[i][j]._round_infected = 1
            population.infected.append((i, j),)

    def lethalityValue(self):
        return self._lethality
    
    def recoveryValue(self):
        return self._recovery_rate