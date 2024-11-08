#!/bin/python3
# coding=utf-8
import os
import sys
import random

random.seed()

def stoneCost(lvl):
    stonecostlist = [
        2000000,
        2000000,
        2000000,
        2400000,
        2500000,
        4000000,
        4450000,
        4800000,
        4870000,
        5000000,
        6500000,
        7200000,
        7200000,
        8000000,
        10000000,
        13850000,
        14000000,
        16000000,
        16000000,
        16000000,
        17000000,
        17000000,
        17000000,
        17000000,
        17000000,
        17000000,
        18500000,
        23300000,
        24000000,
        25000000,
        26900000]

    if lvl < 80:
        lvl = 80
    if lvl > 110:
        lvl = 110
    return stonecostlist[lvl - 80]

class GearPeice:
    def __init__(self, gearlevel = 55, enchantLevel = 0, geartype="eternal"):
        self.enchantLevel = enchantLevel
        self.gearlevel = gearlevel
        self.geartype = geartype
        self.cost = 0
        self.stonelist = []

    def __gt__(self, other):
        if isinstance(other, GearPeice):
            return self.cost > other.cost
    def __lt__(self, other):
        if isinstance(other, GearPeice):
            return self.cost < other.cost
    
    def __str__(self):
        return "Cost = %i, Total stones = %i" % (self.cost, len(self.stonelist))

    def canEnchant(self):
        return self.enchantLevel < 15

    def calcChance(self, stone, supplements = 'none'):
        if isinstance(stone, EnchantmentStone):
            additional = 0
            match supplements:
                case '':
                    additional = 0
                case 'lesser':
                    additional = 0.05
                case 'normal':
                    additional = 0.1
                case 'greater':
                    additional = 0.15
            if self.geartype=="fabled":
                if self.enchantLevel < 10:
                    return min(80 - ((self.gearlevel + 35 - stone.level) * 0.01), 0.8) + additional
                return min(0.4875 - ((self.gearlevel + 45 - stone.level) * 0.0075), 0.5) + additional
            else:
                if self.enchantLevel < 10:
                    return min(80 - ((self.gearlevel + 45 - stone.level) * 0.01), 0.8) + additional
                return min(0.4875 - ((self.gearlevel + 55 - stone.level) * 0.0075), 0.5) + additional
        return 1

    def enchant(self, stone, supplements = 'none'):
        if isinstance(stone, EnchantmentStone):
            if random.random() < self.calcChance(stone, supplements):
                self.enchantLevel = self.enchantLevel + 1
            else:
                if self.enchantLevel >= 15:
                    return
                elif self.enchantLevel > 10:
                    self.enchantLevel = 10
                elif self.enchantLevel > 0:
                    self.enchantLevel = self.enchantLevel - 1
                else:
                    self.enchantLevel = 0
                self.cost = self.cost + stone.cost
                self.stonelist.append(stone)
        else:
            raise Exception("not enchantment stone")

class EnchantmentStone:
    def __init__(self, enchantLevel):
        self.level = enchantLevel
        self.cost = stoneCost(enchantLevel)

    def __gt__(self, other):
        if isinstance(other, EnchantmentStone):
            return self.enchantLevel > other.enchantLevel
    def __lt__(self, other):
        if isinstance(other, EnchantmentStone):
            return self.enchantLevel < other.enchantLevel

args = sys.argv[1:]

displayDistribution = False
enchantend = 15
enchantstart = 10
enchantmentStones = [
    EnchantmentStone(80), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(95), 
    EnchantmentStone(105),
    EnchantmentStone(105),
    EnchantmentStone(105),
    EnchantmentStone(105),
    EnchantmentStone(105)]

index = 0
while index < len(args):
    if args[index] == '-p':
        displayDistribution = True
        index = index + 1
    if args[index] == '-e':
        index = index + 1
        enchantend = (int)(args[index])
        index = index + 1
    if args[index] == '-b':
        index = index + 1
        enchantstart = (int)(args[index])
        index = index + 1
    if args[index] == '-c':
        index = index + 1
        stonechance = (float)(args[index])
        index = index + 1
    if args[index] == '-s':
        index = index + 1
        simtime = (int)(args[index])
        index = index + 1

simtime = 10
simresults = []
for i in range(simtime):
    gear = GearPeice()
    print(gear.enchantLevel)
    while(gear.canEnchant()):
        gear.enchant(enchantmentStones[gear.enchantLevel])
        print(gear)
    simresults.append(gear)

#sortResults()

simresults.sort()

totalGTE10 = 0

for res in simresults:
    print(res)