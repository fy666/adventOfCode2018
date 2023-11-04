#include "days.hpp"
#include <cstdint>
#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>

struct ComputingMonkey {
  std::string m1;
  std::string m2;
  std::function<int64_t(int64_t, int64_t)> operation;
  std::string operationString;
};

int64_t part1Solve(std::unordered_map<std::string, int64_t> numberMonkeys,
                   std::unordered_map<std::string, ComputingMonkey> computingMonkeys) {
  while (computingMonkeys.size()) {
    for (auto it = computingMonkeys.begin(); it != computingMonkeys.end();) {
      auto itm1 = numberMonkeys.find(it->second.m1);
      if (itm1 == numberMonkeys.end()) {
        it++;
        continue;
      }
      auto itm2 = numberMonkeys.find(it->second.m2);
      if (itm2 == numberMonkeys.end()) {
        it++;
        continue;
      }
      numberMonkeys.insert({it->first, it->second.operation(itm1->second, itm2->second)});
      it = computingMonkeys.erase(it);
    }
  }

  return numberMonkeys["root"];
}

std::string getEquation(const std::unordered_map<std::string, int64_t> &numberMonkeys,
                        const std::unordered_map<std::string, ComputingMonkey> &computingMonkeys, std::string monkey) {
  std::string result = "(";
  if (monkey == "humn") {
    return monkey;
  }
  auto itm = numberMonkeys.find(monkey);
  if (itm != numberMonkeys.end()) {
    return std::to_string(itm->second);
  }

  auto m = computingMonkeys.find(monkey);

  auto itm1 = numberMonkeys.find(m->second.m1);
  if (itm1 != numberMonkeys.end()) {
    result += std::to_string(itm1->second);
  } else {
    result += getEquation(numberMonkeys, computingMonkeys, m->second.m1);
  }
  result += m->second.operationString;

  auto itm2 = numberMonkeys.find(m->second.m2);
  if (itm2 != numberMonkeys.end()) {
    result += std::to_string(itm2->second);
  } else {
    result += getEquation(numberMonkeys, computingMonkeys, m->second.m2);
  }
  result += ")";
  return result;
}

int64_t part2Solve(std::unordered_map<std::string, int64_t> numberMonkeys,
                   std::unordered_map<std::string, ComputingMonkey> computingMonkeys) {
  /* Adapt to part 2 */
  auto it = computingMonkeys.find("root");
  it->second.operation = [](int64_t a, int64_t b) { return a - b; };
  it->second.operationString = "-";
  auto it2 = numberMonkeys.find("humn");
  numberMonkeys.erase(it2);

  /* Reduce */
  bool found = true;
  while (found && computingMonkeys.size()) {
    found = false;
    for (auto it = computingMonkeys.begin(); it != computingMonkeys.end();) {
      auto itm1 = numberMonkeys.find(it->second.m1);
      if (itm1 == numberMonkeys.end()) {
        it++;
        continue;
      }
      auto itm2 = numberMonkeys.find(it->second.m2);
      if (itm2 == numberMonkeys.end()) {
        it++;
        continue;
      }
      numberMonkeys.insert({it->first, it->second.operation(itm1->second, itm2->second)});
      it = computingMonkeys.erase(it);
      found = true;
    }
  }
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {} number monkeys and {} operation monkeys", numberMonkeys.size(),
                                          computingMonkeys.size());
  // for (const auto &x : computingMonkeys) {
  //   BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {}: need {} {}", x.first, x.second.m1, x.second.m2);
  // }

  auto strEq = getEquation(numberMonkeys, computingMonkeys, "root");
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Equation =  {}", strEq);

  numberMonkeys.insert({"humn", 0});
  std::vector<int64_t> tries{10000000000, 10000000000};
  for (const auto &x : tries) {
    numberMonkeys["humn"] = x;
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Say {}, result = {}", x, part1Solve(numberMonkeys, computingMonkeys));
  }

  return numberMonkeys["root"];
}

void parse(const std::vector<std::string> &data, std::unordered_map<std::string, int64_t> &numberMonkeys,
           std::unordered_map<std::string, ComputingMonkey> &computingMonkeys) {
  const boost::regex expr("(\\w+): (\\d+)");
  const boost::regex expr2("(\\w+): (\\w+) ([\\+\\-\\*/]) (\\w+)");
  for (const auto &x : data) {
    boost::smatch what;
    if (boost::regex_search(x, what, expr)) {
      numberMonkeys.insert({what[1], stoi(what[2])});
    } else if (boost::regex_search(x, what, expr2)) {
      ComputingMonkey newMonkey{.m1 = what[2], .m2 = what[4]};
      newMonkey.operationString = what[3];
      if (what[3] == "+") {
        newMonkey.operation = [](int64_t a, int64_t b) { return a + b; };
      } else if (what[3] == "-") {
        newMonkey.operation = [](int64_t a, int64_t b) { return a - b; };
      } else if (what[3] == "/") {
        newMonkey.operation = [](int64_t a, int64_t b) { return a / b; };
      } else if (what[3] == "*") {
        newMonkey.operation = [](int64_t a, int64_t b) { return a * b; };
      } else {
        BOOST_LOG_TRIVIAL(debug) << fmt::format("Monkey on line {} has no operation parsed", x);
      }
      computingMonkeys.insert({what[1], newMonkey});
    } else {
      BOOST_LOG_TRIVIAL(debug) << fmt::format("Line {} not parsed", x);
    }
  }
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {} number monkeys and {} operation monkeys", numberMonkeys.size(),
                                          computingMonkeys.size());
}

void day21Run(bool test) {
  std::string fileName = fmt::format("../inputs/day21{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());

  std::unordered_map<std::string, int64_t> numberMonkeys;
  std::unordered_map<std::string, ComputingMonkey> computingMonkeys;
  parse(data, numberMonkeys, computingMonkeys);
  auto res1 = part1Solve(numberMonkeys, computingMonkeys);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 root =  {}", res1);

  auto res2 = part2Solve(numberMonkeys, computingMonkeys);
}