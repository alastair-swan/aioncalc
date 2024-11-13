#include "EnchantmentStone.h"
#include "Gear.h"
#include <cmath>
#include <algorithm>
#include <vector>
#include <iostream>
#include <chrono>

int main(int argc, char** argv){

    std::default_random_engine rng;
    rng.seed(std::chrono::system_clock::now().time_since_epoch().count());
    std::mt19937 gen(rng());
    std::uniform_real_distribution<double> dist(0.0, 1.0);

    std::vector<EnchantmentStone> stoneSequence = {
        EnchantmentStone(70),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(80),
        EnchantmentStone(110),
        EnchantmentStone(110),
        EnchantmentStone(110)
    };

    std::vector<Gear> testGearList;

    int tests = 100000;
    double percentile = 1-0.05;
    for (int i = 0; i < tests; i++){
        Gear testGear(55, 0);
        testGear.enchant(stoneSequence, 15);
        testGearList.push_back(testGear);
    }
    sort(testGearList.begin(), testGearList.end());
    std::cout << std::endl;
    std::cout << (testGearList.at((int) (tests * percentile)).enchantCost / 1000000.0) << std::endl;
    std::cout << (testGearList.at((int) (tests * percentile)).sequence.size()) << std::endl;
    int L110 = 0;
    for (u_long i = 0; i < testGearList.at((int) (tests * percentile)).sequence.size(); i++){
        if (testGearList.at((int) (tests * percentile)).sequence.at(i).level == 110){
            L110++;
        }
    }
    std::cout << L110 << std::endl;
    return 0;
}