#include "Gear.h"
#include <iostream>

Gear::Gear(int gearLevel, int enchantLevel):
gearLevel(gearLevel), enchantLevel(enchantLevel)
{
}

int Gear::enchant(std::vector<EnchantmentStone>& stonemap, int targetLevel)
{
    u_long cost = 0;
    while (enchantLevel < targetLevel){
        cost += stonemap.at(enchantLevel).price();
        sequence.push_back(stonemap.at(enchantLevel));
        if (stonemap.at(enchantLevel).enchant(enchantLevel, gearLevel)){
            enchantLevel++;
        }
        else{
            enchantLevel = (enchantLevel < 10) ? enchantLevel - 1 : 10;
            if (enchantLevel < 0){
                enchantLevel = 0;
            }
        }
    }
    enchantCost = cost;
    return cost;
}
