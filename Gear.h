#pragma once
#include <vector>
#include "EnchantmentStone.h"

class Gear{
    public:
        std::vector<EnchantmentStone> sequence;
        int gearLevel;
        int enchantLevel;
        u_long enchantCost = 0;
        Gear() = delete;
        Gear(int gearLevel, int enchantLevel);

        int enchant(std::vector<EnchantmentStone>& stonemap, int targetLevel);

        bool operator<(const Gear& obj) const
        {
            return enchantCost < obj.enchantCost;
        }
        bool operator>(const Gear& obj) const
        {
            return enchantCost > obj.enchantCost;
        }
        bool operator<=(const Gear& obj) const
        {
            return enchantCost <= obj.enchantCost;
        }
        bool operator>=(const Gear& obj) const
        {
            return enchantCost >= obj.enchantCost;
        }
};