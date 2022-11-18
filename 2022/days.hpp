#include "utils.hpp"
#include <boost/log/trivial.hpp>
#include <boost/regex.hpp>
#include <fmt/core.h>
#include <iostream>
#include <vector>

static float my_own_stof(const std::string x) { return stof(x); }

void day1Run();
void day2Run();