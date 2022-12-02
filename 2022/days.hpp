#include "utils.hpp"
#include <boost/log/trivial.hpp>
#include <boost/regex.hpp>
#include <fmt/core.h>
#include <iostream>
#include <vector>

static float my_own_stof(const std::string x) {
  if (x.size() == 0) {
    return -1;
  } else {
    return stof(x);
  }
}

static std::string my_string(const std::string x) { return x; }

void day1Run(bool test);
void day2Run(bool test);
void day3Run(bool test);
void day4Run(bool test);
void day5Run(bool test);
void day6Run(bool test);
void day7Run(bool test);
void day8Run(bool test);
void day9Run(bool test);
void day10Run(bool test);
void day11Run(bool test);
void day12Run(bool test);
void day13Run(bool test);
void day14Run(bool test);
void day15Run(bool test);
void day16Run(bool test);
void day17Run(bool test);
void day18Run(bool test);
void day19Run(bool test);
void day20Run(bool test);
void day21Run(bool test);
void day22Run(bool test);
void day23Run(bool test);
void day24Run(bool test);
void day25Run(bool test);