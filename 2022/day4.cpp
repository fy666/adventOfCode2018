#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

std::vector<float> day4Parser(std::string input) {
  std::vector<float> results;
  const boost::regex expr("(\\d+)-(\\d+),(\\d+)-(\\d+)");
  boost::smatch what;
  if (boost::regex_search(input, what, expr)) {
    for (auto x = 1; x < 5; ++x) {
      results.push_back(stof(what[x]));
    }
  } else {
    BOOST_LOG_TRIVIAL(error) << fmt::format("No match found");
  }
  return results;
}

void day4Run(bool test) {
  std::string fileName = fmt::format("../inputs/day4{}.txt", test ? "_test" : "");
  auto data = read_file<std::vector<float>>(fileName, day4Parser);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  int countCompleteOverlap = 0;
  int countOverlap = 0;
  for (auto x : data) {
    if ((x[2] >= x[0] && x[3] <= x[1]) || (x[2] <= x[0] && x[3] >= x[1])) {
      countCompleteOverlap += 1;
    }
    if ((x[2] >= x[0] && x[2] <= x[1]) || (x[3] >= x[0] && x[3] <= x[1]) || (x[0] >= x[2] && x[0] <= x[3]) ||
        (x[1] >= x[2] && x[1] <= x[3])) {
      countOverlap += 1;
    }
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Found {} complete intersections", countCompleteOverlap);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Found {} complete intersections", countOverlap);
}