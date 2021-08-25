#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 18:01:01 2021

@author: nataoliveirasousa
"""

from operator import xor
from random import random

class Individual:
    def __init__(self):
        self.__alive          =  True
        self.__contaminated   = False
        self.__heal           = 1
        self.__mask           = False
        self._isolated        = False 
        self._round_infected  = 0
        self._critical        = False
        self._critical_time   = 0
    
    def _death(self):
        self.__alive          = False
        self.__contaminated   = False
        self.__heal           = -1
        self.__mask           = False 
        self._round_infected  = -1
        self._critical_time   = -1
        self._critical        = False
        self._isolated        = False 

    def restart(self):
        self.__alive          =  True
        self.__contaminated   = False
        self.__heal           = 1
        self.__mask           = False
        self._round_infected  = 0
        self._critical        = False
        self._isolated        = False 


    def isAlive(self):
        return self.__alive is True

    def isContaminated(self):
        return self.__contaminated is True
    
    def _contaminated(self):
        self.__contaminated = True

    def wearingMask(self):
        return self.__mask is True

    def _toHeal(self):
        self.__contamineted = False
        self.__heal += 1
        self._round_infected  = 0
        self._critical        = False
        self._critical_time   = 0

    def transmitTo(self, individual):
        individual._contaminated()
        
    def isHeal(self):
        return (self.__heal > 1)
        
    def _putMask(self):
        self.__mask = True

    def isolated(self):
        return self._isolated

    def critical(self):
        return self._critical