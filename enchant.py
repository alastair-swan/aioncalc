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
        2000000,  #  80
        2000000,  #  81
        2000000,  #  82
        2000000,  #  83
        2700000,  #  84
        4300000,  #  85
        4300000,  #  86
        4300000,  #  87
        4450000,  #  88
        5300000,  #  89
        7000000,  #  90
        7400000,  #  91
        7500000,  #  92
        10000000, #  93
        10000000, #  94
        13850000, #  95
        13850000, #  96
        13850000, #  97
        13850000, #  98
        17000000, #  99
        18300000, # 100
        18300000, # 101
        18300000, # 102
        18300000, # 103
        18300000, # 104
        18300000, # 105
        18500000, # 106
        19000000, # 107
        24000000, # 108
        27400000, # 109
        27400000] # 110

    if lvl < 80:
        lvl = 80
    if lvl > 110:
        lvl = 110
    return stonecostlist[lvl - 80]

class GearPiece:
    def __init__(self, enchantLevel = 0, gearlevel = 55, geartype="eternal", cost=0):
        self.enchantLevel = enchantLevel
        self.gearlevel = gearlevel
        self.geartype = geartype
        self.cost = 0
        #self.stonelist = []

    def __gt__(self, other):
        if isinstance(other, GearPiece):
            return self.cost > other.cost
        return self.cost > other
    def __lt__(self, other):
        if isinstance(other, GearPiece):
            return self.cost < other.cost
        return self.cost > other
    def __str__(self):
        return "Cost = %i, Total stones = %i" % (self.cost, len(self.stonelist))
    def __add__(self, other):
        if isinstance(other, GearPiece):
            return GearPiece(gearlevel=self.gearlevel, enchantLevel=self.enchantLevel, geartype=self.geartype, cost=(self.cost + other.cost))

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
                    return min(0.8 - ((self.gearlevel + 35 - stone.level) * 0.01), 0.8) + additional
                return min(0.4875 - ((self.gearlevel + 45 - stone.level) * 0.0075), 0.5) + additional
            else:
                if self.enchantLevel < 10:
                    return min(0.8 - ((stone.level - self.gearlevel - 45) * 0.01), 0.8) + additional
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
            #self.stonelist.append(stone)
        else:
            raise Exception("not enchantment stone")

class EnchantmentStone:
    def __init__(self, level):
        if isinstance(level, EnchantmentStone):
            self.level = level.level
            self.cost = level.cost
        else:
            self.level = level
            self.cost = stoneCost(level)
    def __str__(self):
        return f"L%s" % (self.level)
    def __gt__(self, other):
        if isinstance(other, EnchantmentStone):
            return self.level > other.level
        return self.level > other
    def __lt__(self, other):
        if isinstance(other, EnchantmentStone):
            return self.level < other.level
        return self.level < other
    def __ge__(self, other):
        if isinstance(other, EnchantmentStone):
            return self.level >= other.level
        return self.level >= other
    def __le__(self, other):
        if isinstance(other, EnchantmentStone):
            return self.level <= other.level
        return self.level <= other
    def __add__(self, other):
        if isinstance(other, EnchantmentStone):
            return EnchantmentStone(self.level + other.level)
        if isinstance(other, int):
            return EnchantmentStone(self.level + other)
    def __sub__(self, other):
        if isinstance(other, EnchantmentStone):
            return EnchantmentStone(self.level - other.level)
        if isinstance(other, int):
            return EnchantmentStone(self.level - other)
        

args = sys.argv[1:]

displayDistribution = False
enchantend = 15
enchantstart = 10
defaultStonelist = [
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


def simulate(enchantmentStones, output=False, simtime = 10000, fromLevel=0, toLevel=15, threadcount=32):
    simresults = []
    for i in range(simtime):
        gear = GearPiece(enchantLevel=fromLevel)
    #    while(gear.enchantLevel < 12):
    #        gear.enchant(enchantmentStones[gear.enchantLevel])
        simresults.append(gear)


    def enchant(results):
        for result in results:
            while(result.enchantLevel < toLevel):
                result.enchant(enchantmentStones[result.enchantLevel])

    threads = []
    blocks = [simresults[x:x+math.ceil(simtime / threadcount)] for x in range(0, len(simresults), math.ceil(simtime / threadcount))]
    for res in blocks[1:]:
        thread = threading.Thread(target=enchant, args=(res,))
        thread.start()
        threads.append(thread)
    enchant(blocks[0])
    for thread in threads:
        thread.join()
    if output:
        simresults.sort()

        maxCost = simresults[-1].cost

        numberofbins = 30
        binsize = maxCost / numberofbins

        bins = []

        totalcost = 0
        count = 0
        cost = 0
        stones = 0
        for res in simresults:
            count = count + 1
            cost = cost + res.cost
            totalcost = totalcost + res.cost
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
    return sum(res.cost for res in simresults)

#simulate(stonelist, output=True)

class EnchantmentStoneSetting:
    def __init__(self, stonelist):
        self.stonelist = stonelist
        self.cost = -1
    def __gt__(self, other):
        if isinstance(other, EnchantmentStoneSetting):
            return self.cost > other.cost
        return self.cost > other
    def __ge__(self, other):
        if isinstance(other, EnchantmentStoneSetting):
            return self.cost >= other.cost
        return self.cost >= other
    def __lt__(self, other):
        if isinstance(other, EnchantmentStoneSetting):
            return self.cost < other.cost
        return self.cost < other
    def __le__(self, other):
        if isinstance(other, EnchantmentStoneSetting):
            return self.cost <= other.cost
        return self.cost <= other
    def __eq__(self, other):
        if isinstance(other, EnchantmentStoneSetting):
            for i in range(15):
                if not self.stonelist[i].level is other.stonelist[i].level:
                    return False
            return True
        return False
    def __str__(self):
        enlist = ["%5s" % ("L%d" % self.stonelist[i].level) for i in range(15)]
        stringRep = ""
        for stone in enlist:
            stringRep = stringRep + "%s" % (stone) 
        return stringRep
    def calcCost(self, start=0, end=15, simtime=1000, tests=2, threadcount=32):
        self.cost = simulate(self.stonelist, fromLevel=start, toLevel=end, simtime=simtime, threadcount=threadcount)
        for i in range(tests):
            self.cost = max(self.cost, simulate(self.stonelist, fromLevel=start, toLevel=end, simtime=simtime, threadcount=threadcount))
        return self.cost

def optimize(start=0, end=15, tests=3, startStepSize = 12, simtime=10000, threadcount=32):
    stepSize = startStepSize
    #bestStoneUpList = EnchantmentStoneSetting([EnchantmentStone(110-math.floor(random.random() * 31)) for i in range(15)])
    bestStoneUpList = EnchantmentStoneSetting([EnchantmentStone(80) for i in range(15)])
    bestStoneDownList = EnchantmentStoneSetting([EnchantmentStone(110) for i in range(15)])

    needConfirmation = True
    while(stepSize >= 1 and needConfirmation):
        bestStoneUpList.calcCost(start, end, simtime=simtime, tests=tests)
        bestStoneDownList.calcCost(start, end, simtime=simtime, tests=tests)
        decreaseAvailable = tests
        attempts = 0
        while decreaseAvailable >= 0:
            attempts = attempts + 1
            #print("Checking vs: %s, cost: %10d " % (bestStoneUpList, bestStoneUpList.cost))
            uplist = []
            downlist = []
            for i in range (0, 15):
                stepLimit = abs((bestStoneUpList.stonelist[i] - bestStoneDownList.stonelist[i]).level)
                #print(stepLimit)
                uplist.append(EnchantmentStoneSetting([EnchantmentStone(min(max(bestStoneUpList.stonelist[j] + 1 if min(stepLimit, stepSize) < 1 else random.randint(1, min(stepLimit, stepSize)) if random.random() > 0.25 else random.randint(1,stepSize), 80), bestStoneDownList.stonelist[i].level)) if i == j else EnchantmentStone(bestStoneUpList.stonelist[j]) if random.random() < 0.85 and abs((bestStoneUpList.stonelist[j] - bestStoneDownList.stonelist[j]).level) < stepSize else EnchantmentStone(80) for j in range(0, 15)]))
                downlist.append(EnchantmentStoneSetting([EnchantmentStone(max(min(bestStoneDownList.stonelist[j] - 1 if min(stepLimit, stepSize) < 1 else random.randint(1, min(stepLimit, stepSize)) if random.random() > 0.25 else random.randint(1,stepSize), 110), bestStoneUpList.stonelist[i].level)) if i == j else EnchantmentStone(bestStoneDownList.stonelist[j]) if random.random() < 0.85 and abs((bestStoneUpList.stonelist[j] - bestStoneDownList.stonelist[j]).level) < stepSize else EnchantmentStone(110) for j in range(0, 15)]))                
            for q in range(3):
                uplist.append(EnchantmentStoneSetting([EnchantmentStone(bestStoneUpList.stonelist[i] if ((bestStoneDownList.stonelist[i].level) - 80 < 1) else random.randint(80, bestStoneDownList.stonelist[i].level)) for i in range(15)]))
                downlist.append(EnchantmentStoneSetting([EnchantmentStone(bestStoneDownList.stonelist[i].level if ((110 - bestStoneUpList.stonelist[i].level) < 1) else random.randint(bestStoneUpList.stonelist[i].level, 110)) for i in range(15)]))                

            for l in uplist:
                #print(l)
                l.calcCost(start, end, simtime=simtime, tests=tests, threadcount=threadcount)
                print('.', end='', flush=True)
                #print("%d %s" % (l.cost, l))
            for l in downlist:
                l.calcCost(start, end, simtime=simtime, tests=tests, threadcount=threadcount)
                print('.', end='', flush=True)
            uplist.append(bestStoneUpList)
            downlist.append(bestStoneDownList)
            oldBestUpList = bestStoneUpList
            oldBestDownList = bestStoneDownList
            bestStoneUpList = min(uplist)
            bestStoneDownList = min(downlist)
            if (bestStoneDownList == bestStoneUpList) or ((bestStoneUpList == oldBestUpList) and (bestStoneDownList == oldBestDownList)):
                decreaseAvailable = decreaseAvailable - 1
            else:
                decreaseAvailable = tests
                needConfirmation = True
                if(stepSize == 1):
                    stepSize=max(stepSize * 3 + 1, startStepSize)
                print()
                print("failed to converge, attempt: %d" % attempts)
                print("Current Best: %4dkk %s" % (round(bestStoneUpList.cost / 1000000 / simtime), bestStoneUpList))
                print("              %4dkk %s" % (round(bestStoneDownList.cost / 1000000 / simtime), bestStoneDownList))
                print('.', end='\n', flush=True)

        print("\nBest at stepsize %d: %4dkk %s" % (stepSize, round(bestStoneUpList.cost / 1000000 / simtime), bestStoneUpList))
        print("                 %d: %4dkk %s" % (stepSize, round(bestStoneDownList.cost / 1000000 / simtime), bestStoneDownList))

        stepSize = math.floor(stepSize / 2)
        if stepSize == 0:
            stepSize = 1
            needConfirmation = False
    return bestStoneUpList
    #print (bestStoneUpList)
    #print (bestStoneUpList.cost)

optimize(0, 15, tests=8, simtime=1000, threadcount=64, startStepSize=9)