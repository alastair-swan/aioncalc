#!/bin/python3
# coding=utf-8
import os
import sys
import random
import math
from colorama import Fore, Back, Style
import threading

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
        return self.cost > other
    def __lt__(self, other):
        if isinstance(other, GearPeice):
            return self.cost < other.cost
        return self.cost > other
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
            if self.enchantLevel >= 15:
                return
            if random.random() < self.calcChance(stone, supplements):
                self.enchantLevel = self.enchantLevel + 1
            else:
                if self.enchantLevel > 10:
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
    EnchantmentStone(110),
    EnchantmentStone(110),
    EnchantmentStone(105),
    EnchantmentStone(105),
    EnchantmentStone(110)]

simtime = 100000
simresults = []


for i in range(simtime):
    gear = GearPeice(enchantLevel=0)
#    while(gear.enchantLevel < 12):
#        gear.enchant(enchantmentStones[gear.enchantLevel])
    simresults.append(gear)


def enchant(results):
    for result in results:
        while(result.enchantLevel < 12):
            result.enchant(enchantmentStones[result.enchantLevel])

threads = []
for res in [simresults[x:x+10000] for x in range(0, len(simresults), 10000)]:
    thread = threading.Thread(target=enchant, args=(res,))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()

simresults.sort()

maxCost = simresults[-1].cost

numberofbins = 30
binsize = maxCost / numberofbins

bins = []

count = 0
cost = 0
stones = 0
for res in simresults:
    count = count + 1
    cost = cost + res.cost
    stones = stones + len(res.stonelist)
    if res > (binsize * (len(bins) + 1)):
        bins.append([count, cost / count, stones / count])
        count = 0
        cost = 0
        stones = 0
#for res in simresults:
#    print(res)

def binkey(item):
    return item[0]

maxwidth = 70
eimarkcheck = 0
for (i, bin) in enumerate(bins):
    eimarkcheck = eimarkcheck + bin[0]
    if (eimarkcheck / simtime) < 0.8:
        print(Fore.GREEN, end='')
    else:
        print(Fore.WHITE, end='')
    print("%5dkk, <=%4d stones" % (math.floor(bin[1] / 1000000), bin[2]), end='\t')
    for i in range(round(bin[0] / max(bins, key=binkey)[0] * maxwidth)):
        print("#", end='')
    print()

print(len(bins))