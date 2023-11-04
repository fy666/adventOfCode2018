#include "days.hpp"
#include <algorithm>
#include <chrono>
#include <iostream>
#include <map>
#include <vector>

int getPriority(char c) {
  if (c >= 'A' && c <= 'Z') {
    return uint(c) - 38;
  }
  if (c >= 'a' && c <= 'z') {
    return uint(c) - 96;
  } else {
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Wrong character {}", c);
    return 0;
  }
}

int part1(std::string x) {
  int halfSize = x.size() / 2;
  std::vector<char> char1(x.begin(), x.begin() + halfSize);
  std::vector<char> char2(x.begin() + halfSize, x.end());

  std::sort(char1.begin(), char1.end());
  std::sort(char2.begin(), char2.end());
  std::vector<char> common;
  std::set_intersection(char1.begin(), char1.end(), char2.begin(), char2.end(), std::back_inserter(common));
  return getPriority(common.front());
}

int part2(std::string a, std::string b, std::string c) {
  std::vector<char> char1(a.begin(), a.end());
  std::vector<char> char2(b.begin(), b.end());
  std::vector<char> char3(c.begin(), c.end());

  std::sort(char1.begin(), char1.end());
  std::sort(char2.begin(), char2.end());
  std::sort(char3.begin(), char3.end());
  std::vector<char> common;
  std::vector<char> common2;
  std::set_intersection(char1.begin(), char1.end(), char2.begin(), char2.end(), std::back_inserter(common));
  std::set_intersection(char3.begin(), char3.end(), common.begin(), common.end(), std::back_inserter(common2));
  BOOST_LOG_TRIVIAL(debug) << fmt::format("{}, {} and {}, common = {} (priority {})", a, b, c, common2.front(), getPriority(common2.front()));
  return getPriority(common2.front());
}

void day3Run(bool test) {
  std::string fileName = fmt::format("../inputs/day3{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());

  auto start = std::chrono::high_resolution_clock::now();
  auto firstLine = part1(data[0]);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("First line = {}", firstLine);
  int score = 0;
  for (auto d : data) {
    score += part1(d);
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 total score = {}", score);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("******************");
  score = 0;
  for (uint x = 0; x < data.size() - 2; x += 3) {
    score += part2(data[x], data[x + 1], data[x + 2]);
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 total score = {}", score);
  auto stop = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
  BOOST_LOG_TRIVIAL(info) << fmt::format(">> Day 3 algo run in {:.3} ms", float(duration.count() / 1000.f));
}