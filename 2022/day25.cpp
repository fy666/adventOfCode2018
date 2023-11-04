#include "days.hpp"
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>

std::map<char, int64_t> SYMBOLS = {{'2', 2}, {'1', 1}, {'0', 0}, {'-', -1}, {'=', -2}};
std::map<int64_t, char> NUM2SYMBOL = {{2, '2'}, {1, '1'}, {0, '0'}, {-1, '-'}, {-2, '='}};

int64_t convertNumber(const std::string &x) {
  auto N = x.size();
  int64_t number = 0;
  for (int i = 0; i < N; ++i) {
    int64_t exposant = N - i - 1;
    number += SYMBOLS[x[i]] * std::pow(5, exposant);
  }
  return number;
}

std::string getNext(std::string x) {
  for (int i = x.size() - 1; i >= 0; --i) {
    auto num = SYMBOLS[x[i]];
    if (num != 2) {
      x[i] = NUM2SYMBOL[num + 1];
      return x;
    } else {
      x[i] = '=';
    }
  }
  return "1" + x;
}

std::string convertNumberToString(int64_t number) {
  // find closest exposant
  int64_t exposant = 0;
  bool keepLooking = true;
  while (keepLooking) {
    exposant++;
    keepLooking = !(number <= std::pow(5, exposant));
  }
  std::string res = "";

  std::vector<char> potentials{'=', '-', '0', '1', '2'};

  for (uint exp = 0; exp < exposant; ++exp) {
    BOOST_LOG_TRIVIAL(debug) << fmt::format("exp {}, res is {}", exp, res);
    for (uint p = 0; p < potentials.size(); ++p) {
      std::string tmp = res + potentials[p];
      std::string minTmp(exposant - exp - 1, '=');
      std::string maxTmp(exposant - exp - 1, '2');

      auto numMin = convertNumber(tmp + minTmp);
      auto numMax = convertNumber(tmp + maxTmp);
      BOOST_LOG_TRIVIAL(trace) << fmt::format("  {}: between {} and {}", potentials[p], numMin, numMax);
      if (numMax >= number && number >= numMin) {
        res = tmp;
        BOOST_LOG_TRIVIAL(debug) << fmt::format("  exp {}, best is {}", exp, potentials[p]);
        break;
      }
    }
  }

  BOOST_LOG_TRIVIAL(debug) << fmt::format("Find {}, ({})", res, convertNumber(res));
  return res;
}

void parseBobInput(const std::vector<std::string> &data) {
  int64_t sum = 0;
  for (const auto &x : data) {
    auto tmp = convertNumber(x);
    sum += tmp;
  }

  auto res = convertNumberToString(sum);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1, sum is {}, in base5 {}", sum, res);
}

void day25Run(bool test) {
  std::string fileName = fmt::format("../inputs/day25{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  parseBobInput(data);
}