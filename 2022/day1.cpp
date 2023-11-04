#include "days.hpp"
#include <algorithm>
#include <iostream>
#include <vector>

void day1Run(bool test) {
  std::string fileName = fmt::format("../inputs/day1{}.txt", test ? "_test" : "");
  auto data = read_file<float>(fileName, my_own_stof);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines. First item = {}, last = {}", data.size(), data.front(),
                                          data.back());

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
  BOOST_LOG_TRIVIAL(info) << fmt::format("Top 3 elves ({:.0f} + {:.0f} + {:.0f}) carry {:.0f} calories", elves[0],
                                         elves[1], elves[2], sum);

  auto printEnumeration = [idx = std::size_t{0}](const auto &T) mutable {
    BOOST_LOG_TRIVIAL(trace) << fmt::format("{} = {}", idx, T);
    idx++;
    return;
  };
  std::for_each(data.cbegin(), data.cend(), printEnumeration);
  // auto enumeration = [idx = std::size_t{0}](const float &T) mutable { return std::pair{idx++, T}; };
  // for (const auto &[index, d] : data | std::ranges::views::transform(enumeration)) {
  //   std::cout << index << ", " << d << std::endl;
  //   // BOOST_LOG_TRIVIAL(info) << fmt::format("{} = {}", index, d);
  // }
  /* part 2 */
}