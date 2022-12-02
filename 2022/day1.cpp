#include "days.hpp"
#include <algorithm>
#include <iostream>
#include <vector>

void testRegex() {
  BOOST_LOG_TRIVIAL(info) << "Doing a regex";
  const boost::regex expr("(\\d{4})");
  std::string a = "doudou 1234 lol 4567";
  boost::smatch what;
  if (boost::regex_search(a, what, expr)) {
    std::cout << what[0] << '\n';
    std::cout << what[1] << "_" << what[2] << '\n';
  } else {
    std::cout << "No match found;" << std::endl;
  }
  BOOST_LOG_TRIVIAL(debug) << "Bye";
  BOOST_LOG_TRIVIAL(info) << fmt::format("Computing something: {}", what.size());
}

void day1Run() {
  BOOST_LOG_TRIVIAL(info) << "*** Doing day 2 ***";
  auto data = read_file<float>("../inputs/day1.txt", my_own_stof);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines. First item = {}, last = {}", data.size(), data[0], data.back());

  int count = 0;
  std::vector<float> elves;
  for (const auto &d : data) {
    if (d == -1) {
      elves.push_back(count);
      count = 0;
    } else {
      count += d;
    }
  }
  std::sort(elves.begin(), elves.end(), std::greater<float>());
  float sum = elves[0] + elves[1] + elves[2];
  BOOST_LOG_TRIVIAL(info) << fmt::format("Top elves has {:.0f} calories", elves[0]);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Top 3 elves ({:.0f} + {:.0f} + {:.0f}) carry {:.0f} calories", elves[0], elves[1], elves[2], sum);
  /* part 2 */
}

/* void day1Run() {
  BOOST_LOG_TRIVIAL(info) << "Doing day 1 ";
  // auto f = [](auto x){return stof(x);};
  auto data = read_file<float>("../inputs/day1_2021.txt", my_own_stof);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines. First item = {}, last = {}", data.size(), data[0], data.back());
  int count_increase = 0;
  auto last = data[0];
  for (const auto &d : data) {
    if (d > last) {
      count_increase += 1;
    }
    last = d;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("{} increases measured", count_increase);
  /* part 2 */
// count_increase = 0;
// int last_sum = data[0] + data[1] + data[2];
// for (uint i = 0; i < data.size() - 3; i++) {
//   int local_sum = data[i] + data[i + 1] + data[i + 2];
//   if (local_sum > last_sum) {
//     count_increase += 1;
//   }
//   last_sum = local_sum;
// }
// BOOST_LOG_TRIVIAL(info) << fmt::format("{} increases measured for sum of 3", count_increase);
// testRegex();
// }
// * /