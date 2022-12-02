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

void day1Run();
void day2Run();