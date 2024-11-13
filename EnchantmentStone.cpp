#include "EnchantmentStone.h"
#include <cmath>
#include <stdexcept>
#include <random>
#include <iostream>
#include <chrono>

static unsigned seed = std::chrono::steady_clock::now().time_since_epoch().count();
static std::mt19937 rng(seed);

EnchantmentStone::EnchantmentStone(int level):
    level(level)
{
    if (level > 115 || level < 50){
        throw new std::runtime_error("out of level range");
    }
    //std::random_device myRandomDevice;
}

bool EnchantmentStone::compare(EnchantmentStone e)
{
    return e.level == level;
}

bool EnchantmentStone::enchant(int enchantLevel, int gearLevel){
    double chance = calcChance(enchantLevel, gearLevel);
    double rand = rng() / (double)rng.max();
    //std::cout << rand << std::endl;

    return rand <= chance;
}

double EnchantmentStone::calcChance(int enchantLevel, int gearLevel){
    double chance = 0;
    double multiplier = (enchantLevel < 10) ? 0.01 : 0.0075;
    double maxchance = (enchantLevel < 10) ? 0.8 : 0.5;
    int calclevel = 55 - gearLevel;
    double baseline = (enchantLevel < 10) ? 0.8 : 0.6;
    int baselinestone = (enchantLevel < 10) ? 100 : 125;
    chance = baseline - ((baselinestone - level - calclevel) * multiplier);

    chance = fmin(chance, maxchance);

    return chance;
}

int EnchantmentStone::increaseToNextPrice()
{
    if (level >= 115){
        return level;
    }
    int currentprice = pricemap[level - 50];
    while(currentprice == pricemap[level - 50]){
        level++;
        if (level >= 115){
            return level;
        }
    }
    currentprice = pricemap[level - 50];
    while(currentprice == pricemap[level - 50]){
        level++;
        if (level >= 115){
            return level;
        }
    }
    level--;
    return level;
}

int EnchantmentStone::decreaseToNextPrice()
{
    if (level <= 50){
        return level;
    }
    int currentprice = pricemap[level - 50];
    while(currentprice == pricemap[level - 50]){
        level--;
        if (level <= 50){
            return level;
        }
    }
    return level;
}

int EnchantmentStone::price()
{
    return pricemap[level - 50];
}
