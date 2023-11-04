#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

void move(std::vector<std::vector<char>> &crates, int stackStart, int stackNumber, int stackEnd) {
  int counter = stackNumber;
  while (counter > 0 && crates[stackStart].size() > 0) {
    crates[stackEnd].push_back(crates[stackStart].back());
    crates[stackStart].pop_back();
    counter -= 1;
  }
}

void move2(std::vector<std::vector<char>> &crates, int stackStart, int stackNumber, int stackEnd) {
  int counter = stackNumber;
  std::vector<char> tmp;
  while (counter > 0 && crates[stackStart].size() > 0) {
    tmp.push_back(crates[stackStart].back());
    crates[stackStart].pop_back();
    counter -= 1;
  }
  while (tmp.size() != 0) {
    crates[stackEnd].push_back(tmp.back());
    tmp.pop_back();
  }
}

std::string day5(const std::vector<std::string> &data, std::vector<std::vector<char>> &crates, bool day1) {
  // move 1 from 2 to 1
  const boost::regex expr("^move (\\d+) from (\\d+) to (\\d+)");
  for (auto d : data) {
    boost::smatch what;
    if (boost::regex_search(d, what, expr)) {
      int stackNumber = stoi(what[1]);
      int stackStart = stoi(what[2]);
      int stackEnd = stoi(what[3]);
      BOOST_LOG_TRIVIAL(trace) << fmt::format("Move {} from {} to {}", stackNumber, stackStart, stackEnd);
      if (day1) {
        move(crates, stackStart - 1, stackNumber, stackEnd - 1);
      } else {
        move2(crates, stackStart - 1, stackNumber, stackEnd - 1);
      }
    }
  }
  std::string result;
  for (auto s : crates) {
    result.append(sizeof(char), s.back());
  }
  return result;
}

void day5Run(bool test) {
  std::string fileName = fmt::format("../inputs/day5{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());

  std::vector<std::vector<char>> crates;
  if (test) {
    crates.push_back({'Z', 'N'});
    crates.push_back({'M', 'C', 'D'});
    crates.push_back({'P'});
  } else {
    crates.push_back({'W', 'M', 'L', 'F'});                     // 1
    crates.push_back({'B', 'Z', 'V', 'M', 'F'});                // 2
    crates.push_back({'H', 'V', 'R', 'S', 'L', 'Q'});           // 3
    crates.push_back({'F', 'S', 'V', 'Q', 'P', 'M', 'T', 'J'}); // 4
    crates.push_back({'L', 'S', 'W'});                          // 5
    crates.push_back({'F', 'V', 'P', 'M', 'R', 'J', 'W'});      // 6
    crates.push_back({'J', 'Q', 'C', 'P', 'N', 'R', 'F'});      // 7
    crates.push_back({'V', 'H', 'P', 'S', 'Z', 'W', 'R', 'B'}); // 8
    crates.push_back({'B', 'M', 'J', 'C', 'G', 'H', 'Z', 'W'}); // 9
  }

  auto d1 = day5(data, crates, true);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Day 1 last crates =  {}", d1);
  auto d2 = day5(data, crates, false);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Day 2 last crates =  {}", d2);
}