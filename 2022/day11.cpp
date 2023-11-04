#include "days.hpp"
#include <cstdint>
#include <iostream>
#include <list>
#include <map>

class Monkey {
public:
  std::list<int64_t> items{};
  int64_t countItems = 0;
  std::function<int64_t(int64_t)> operation;
  std::function<int64_t(int64_t)> test;
  void run(std::vector<Monkey> &monkeys, bool part1, int64_t divisor) {
    while (items.size()) {
      auto item = items.front();
      BOOST_LOG_TRIVIAL(trace) << fmt::format("Monkey treat item {}", item);
      if (part1) {
        item = int64_t(operation(item) / 3);
      } else {
        item = (operation(item) % divisor);
      }
      BOOST_LOG_TRIVIAL(trace) << fmt::format("after operation = {}", item);
      auto newMonkey = test(item);
      BOOST_LOG_TRIVIAL(trace) << fmt::format("send to monkey {}", newMonkey);
      monkeys[newMonkey].items.push_back(item);
      countItems += 1;
      items.pop_front();
    }
  }
  Monkey(std::list<int64_t> t_items) : items(t_items){};
};

int64_t part1(std::vector<Monkey> monkeys) {
  for (int64_t turn = 0; turn < 20; ++turn) {
    for (int64_t i = 0; i < monkeys.size(); ++i) {
      monkeys[i].run(monkeys, true, 0);
    }
  }
  std::vector<int64_t> scores;
  for (int64_t i = 0; i < monkeys.size(); ++i) {
    scores.push_back(monkeys[i].countItems);
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Monkey {} inspected {} items", i, monkeys[i].countItems);
  }
  std::sort(scores.begin(), scores.end(), std::greater<int64_t>());
  return scores[0] * scores[1];
}

uint64_t part2(std::vector<Monkey> monkeys, int64_t divisor) {
  for (int64_t turn = 0; turn < 10000; ++turn) {
    for (int64_t i = 0; i < monkeys.size(); ++i) {
      monkeys[i].run(monkeys, false, divisor);
    }
  }
  std::vector<int64_t> scores;
  for (int64_t i = 0; i < monkeys.size(); ++i) {
    scores.push_back(monkeys[i].countItems);
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Monkey {} inspected {} items", i, monkeys[i].countItems);
  }
  std::sort(scores.begin(), scores.end(), std::greater<int64_t>());
  return scores[0] * scores[1];
}

void day11Run(bool test) {
  std::string fileName = fmt::format("../inputs/day11{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  std::vector<Monkey> monkeys;
  int64_t divisor;

  if (test) {
    monkeys.push_back({{79, 98}});
    monkeys[0].operation = [](int64_t input) { return input * 19; };
    monkeys[0].test = [](int64_t input) {
      if ((input % 23) == 0) {
        return 2;
      } else {
        return 3;
      }
    };
    monkeys.push_back({{54, 65, 75, 74}});
    monkeys[1].operation = [](int64_t input) { return input + 6; };
    monkeys[1].test = [](int64_t input) {
      if ((input % 19) == 0) {
        return 2;
      } else {
        return 0;
      }
    };

    monkeys.push_back({{79, 60, 97}});
    monkeys[2].operation = [](int64_t input) { return input * input; };
    monkeys[2].test = [](int64_t input) {
      if ((input % 13) == 0) {
        return 1;
      } else {
        return 3;
      }
    };

    monkeys.push_back({{74}});
    monkeys[3].operation = [](int64_t input) { return input + 3; };
    monkeys[3].test = [](int64_t input) {
      if ((input % 17) == 0) {
        return 0;
      } else {
        return 1;
      }
    };
    divisor = 23 * 19 * 13 * 17;
  } else {
    monkeys.push_back({{71, 86}});
    monkeys[0].operation = [](int64_t input) { return input * 13; };
    monkeys[0].test = [](int64_t input) {
      if ((input % 19) == 0) {
        return 6;
      } else {
        return 7;
      }
    };
    monkeys.push_back({{66, 50, 90, 53, 88, 85}});
    monkeys[1].operation = [](int64_t input) { return input + 3; };
    monkeys[1].test = [](int64_t input) {
      if ((input % 2) == 0) {
        return 5;
      } else {
        return 4;
      }
    };

    monkeys.push_back({{97, 54, 89, 62, 84, 80, 63}});
    monkeys[2].operation = [](int64_t input) { return input + 6; };
    monkeys[2].test = [](int64_t input) {
      if ((input % 13) == 0) {
        return 4;
      } else {
        return 1;
      }
    };

    monkeys.push_back({{82, 97, 56, 92}});
    monkeys[3].operation = [](int64_t input) { return input + 2; };
    monkeys[3].test = [](int64_t input) {
      if ((input % 5) == 0) {
        return 6;
      } else {
        return 0;
      }
    };
    monkeys.push_back({{50, 99, 67, 61, 86}});
    monkeys[4].operation = [](int64_t input) { return input * input; };
    monkeys[4].test = [](int64_t input) {
      if ((input % 7) == 0) {
        return 5;
      } else {
        return 3;
      }
    };
    monkeys.push_back({{61, 66, 72, 55, 64, 53, 72, 63}});
    monkeys[5].operation = [](int64_t input) { return input + 4; };
    monkeys[5].test = [](int64_t input) {
      if ((input % 11) == 0) {
        return 3;
      } else {
        return 0;
      }
    };

    monkeys.push_back({{59, 79, 63}});
    monkeys[6].operation = [](int64_t input) { return input * 7; };
    monkeys[6].test = [](int64_t input) {
      if ((input % 17) == 0) {
        return 2;
      } else {
        return 7;
      }
    };

    monkeys.push_back({{55}});
    monkeys[7].operation = [](int64_t input) { return input + 7; };
    monkeys[7].test = [](int64_t input) {
      if ((input % 3) == 0) {
        return 2;
      } else {
        return 1;
      }
    };
    divisor = 19 * 2 * 13 * 5 * 7 * 11 * 17 * 3;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", part1(monkeys));
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", part2(monkeys, divisor));
}