#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

void day6Run(bool test) {
  std::string fileName = fmt::format("../inputs/day6{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  std::string message = data[0];
  for (uint x = 0; x < message.size() - 4; ++x) {
    std::set<int> mySet(message.begin() + x, message.begin() + x + 4);
    if (mySet.size() == 4) {
      BOOST_LOG_TRIVIAL(debug) << fmt::format("First part = {}", x + 4);
      break;
    }
  }

  for (uint x = 0; x < message.size() - 14; ++x) {
    std::set<int> mySet(message.begin() + x, message.begin() + x + 14);
    if (mySet.size() == 14) {
      BOOST_LOG_TRIVIAL(debug) << fmt::format("Second part = {}", x + 14);
      break;
    }
  }
}