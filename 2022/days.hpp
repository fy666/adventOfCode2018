#include "utils.hpp"
#include <boost/log/trivial.hpp>
#include <boost/regex.hpp>
#include <fmt/core.h>
#include <iostream>
#include <vector>

typedef std::pair<int, int> Point;
static Point operator+(const Point &a, const Point &b) {
  Point res;
  return {a.first + b.first, a.second + b.second};
}
static bool operator==(const Point &a, const Point &b) { return a.first == b.first && a.second == b.second; }

static float my_own_stof(const std::string x) {
  if (x.size() == 0) {
    return -1;
  } else {
    return stof(x);
  }
}

static int my_own_stoi(const std::string x) {
  if (x.size() == 0) {
    return -1;
  } else {
    return stoi(x);
  }
}

static int positive_modulo(int i, int n) { return (i % n + n) % n; }
static std::string my_string(const std::string x) { return x; }

#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/repetition/repeat_from_to.hpp>

#define DECL(z, n, data) BOOST_PP_CAT(void day, BOOST_PP_CAT(n, Run(bool test);))

BOOST_PP_REPEAT_FROM_TO(1, 26, DECL, 0)