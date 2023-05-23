#Engine of mechanic based on 18-05-23 version of Mythic Bastionland (https://www.bastionland.com/)
import random
import os
import sys
import itertools


#Setting directory
os.chdir(os.path.dirname(sys.argv[0]))

#################################
#             Classes           #
#################################

# Warband classes with options from book (p. 9)
class Warband():
    def __init__(self, vig, GD, dmg, armor, n = None): # new materials have to be updated here
        self.vig: int = vig
        self.GD: int = GD
        self.dmg: int = dmg
        self.life: bool = True
        self.armor:int = armor
        self.n:int = n

    def __str__(self):
        return(f"vig = {self.vig}, GD = {self.GD}, dmg = k{self.dmg}. warband{self.n} is alive: {self.life}")

    def recieve_dmg(self, dmg):
        #print(dmg)
        dmg -= self.armor
        if dmg < 0:
            dmg = 0
            
        if dmg < self.GD:
            self.GD -= dmg
            #print(dmg, self)
        else:
            dmg -= self.GD
            self.GD = 0
            #print(dmg, self)

        if dmg >= self.vig/2:
            self.vig -= dmg
            self.life = False
            #print(dmg, self)
        else:
            self.vig -= dmg
            #print(dmg, self)

class Warband_conscripts(Warband):
    def __init__(self, vig = 10, GD = 4, dmg = 6, armor = 0, n = None):

        super().__init__(vig, GD, dmg, armor, n)

class Warband_mercenaries(Warband):
    def __init__(self, vig = 10, GD = 5, dmg = 8, armor = 0, n = None):

        super().__init__(vig, GD, dmg, armor, n)

class Warband_knights(Warband):
    def __init__(self, vig = 13, GD = 7, dmg = 8, armor = 3, n = None):

        super().__init__(vig, GD, dmg, armor, n)

#################################
#           Functions           #
#################################

def roll_dmg(*args, bonus = None):
    dmg = []

    for attacker in args:
        if attacker.life == True:
            dmg.append(random.randrange(1, attacker.dmg+1, 1))

    if dmg != [] and bonus != None:
        dmg.append(random.randrange(1, bonus+1, 1)) #add bonus dice

    if dmg != []: return(max(dmg)) #If multiple attackers return only the biggest value
    else: return(0)

def deal_dmg_to(*args, dmg):
    for defender in args:
        if defender.life == True:
            defender.recieve_dmg(dmg)
            dmg = 0
            break



# Function to calculate the average dmg on attack with multiple dice.

def Multiple_attack_avg_dmg(*values):
    dice_values = values
    num_dice = len(values)
    
    all_throws = itertools.product(*[range(1, dice_value + 1) for dice_value in dice_values])
    max_results = [max(throw) for throw in all_throws]
    sum_max_results = sum(max_results)
    num_throws = len(max_results)
    
    return sum_max_results / num_throws