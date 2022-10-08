#include "utils.hpp"
#include <fmt/core.h>
#include <iostream>
#include <vector>

float my_own_stof(const std::string x){
    return stof(x);
}


void run() {
  std::cout << "Doing day 1 " << std::endl;
  //auto f = [](auto x){return stof(x);};
  auto data = read_file<float>("../inputs/day1_2021.txt",my_own_stof);
  std::cout << "Read " << data.size() << " lines" << std::endl;
  std::cout << "First = " << data[0] << ", last = " << data.back() << std::endl;
  for(const auto& d:data){
    std::cout << d << std::endl;
    break;
  }

}