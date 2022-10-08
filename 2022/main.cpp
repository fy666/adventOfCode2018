#include <fmt/core.h>
#include <iostream>
#include <vector>

#include "day1.hpp"
//#include "utils.hpp"
std::vector<int> get_data() { return std::vector<int>{1, 2, 3, 4, 5}; }

int main() {
  int a = 4;
  std::cout << "Hello world, a = " << a << std::endl;
  std::cout << fmt::format("Coucou {}", a) << std::endl;
  run();
//   auto result = read_file("lol");
//   for (const auto &r : result) {
//     std::cout << r << std::endl;
//   }
  return 1;
}