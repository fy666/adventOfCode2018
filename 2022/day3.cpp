#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

void day3Run(bool test) {
  std::string fileName = fmt::format("../inputs/day2{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
}