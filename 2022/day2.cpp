#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

void day2Run(bool test) {
  std::string fileName = fmt::format("../inputs/day2{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines. First item = {}, Last = {}", data.size(), data[0], data.back());
  std::map<std::string, int> rule1 = {{"A X", 4}, {"A Y", 8}, {"A Z", 3}, {"B X", 1}, {"B Y", 5}, {"B Z", 9}, {"C X", 7}, {"C Y", 2}, {"C Z", 6}};
  std::map<std::string, int> rule2 = {{"A X", 3}, {"A Y", 4}, {"A Z", 8}, {"B X", 1}, {"B Y", 5}, {"B Z", 9}, {"C X", 2}, {"C Y", 6}, {"C Z", 7}};
  int totalScorePart1 = 0;
  int totalScorePart2 = 0;
  for (auto d : data) {
    totalScorePart1 += rule1[d];
    totalScorePart2 += rule2[d];
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Total score part 1 = {}", totalScorePart1);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Total score part 2 = {}", totalScorePart2);
}