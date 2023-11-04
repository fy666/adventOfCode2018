#include "days.hpp"
#include <cstdint>
#include <iostream>
#include <map>
#include <sys/types.h>
#include <unistd.h>
#include <unordered_map>
#include <vector>

class Point4 {
public:
  int ore = 0;
  int clay = 0;
  int obsidian = 0;
  int geode = 0;

  void addOne(int pos) {
    if (pos == 0) {
      ore += 1;
    } else if (pos == 1) {
      clay += 1;
    } else if (pos == 2) {
      obsidian += 1;
    } else if (pos == 3) {
      geode += 1;
    }
  }
  Point4() {}
  Point4(int a, int b, int c, int d) : ore(a), clay(b), obsidian(c), geode(d) {}

  Point4 operator+(Point4 const &obj) {
    Point4 res;
    res.ore = ore + obj.ore;
    res.clay = clay + obj.clay;
    res.obsidian = obsidian + obj.obsidian;
    res.geode = geode + obj.geode;
    return res;
  }

  Point4 operator-(Point4 const &obj) {
    Point4 res;
    res.ore = ore - obj.ore;
    res.clay = clay - obj.clay;
    res.obsidian = obsidian - obj.obsidian;
    res.geode = geode - obj.geode;
    return res;
  }

  std::string toString() { return fmt::format("{},{},{},{}", ore, clay, obsidian, geode); }
};

class Blueprint {
public:
  // ore, clay, obsidian, geode
  Blueprint(std::vector<int> givenRules) {
    rules.push_back({givenRules[0], 0, 0, 0});
    rules.push_back({givenRules[1], 0, 0, 0});
    rules.push_back({givenRules[2], givenRules[3], 0, 0});
    rules.push_back({givenRules[4], 0, givenRules[5], 0});
    std::vector<int> oreRules{givenRules[0], givenRules[1], givenRules[2], givenRules[4]};
    auto maxOre = (*max_element(oreRules.begin(), oreRules.end()));
    maxRules = {maxOre, givenRules[3], givenRules[5], 0};
  }

  std::vector<Point4> rules;
  Point4 maxRules;

  Point4 canBeConstructed(const Point4 &items) const {
    Point4 tmp{};
    int i = 0;
    for (const auto &rule : rules) {
      if (items.ore >= rule.ore && items.clay >= rule.clay && items.obsidian >= rule.obsidian) {
        tmp.addOne(i);
      }
      i++;
    }
    return tmp;
  }
};

struct RobotState {
  Point4 robots{1, 0, 0, 0};
  Point4 items{0, 0, 0, 0};
  int minutesLeft = 24;
};

bool operator==(const Point4 &a, const Point4 &b) {
  return a.ore == b.ore && a.clay == b.clay && a.obsidian == b.obsidian && a.geode == b.geode;
}

bool operator==(const RobotState &a, const RobotState &b) {
  return a.robots == b.robots && a.items == b.items && a.minutesLeft == b.minutesLeft;
}

struct StateHash {
  std::size_t operator()(const RobotState &k) const {
    std::size_t ret = k.minutesLeft;
    uint32_t multiplier = 100;
    std::vector<int> data{k.robots.ore, k.robots.clay, k.robots.obsidian, k.robots.geode,
                          k.items.ore,  k.items.clay,  k.items.obsidian,  k.items.geode};
    for (const auto &d : data) {
      ret += (uint32_t)d * multiplier;
      multiplier *= 1000;
    }
    return ret;
  }
};

int run(RobotState current, const Blueprint &bp, std::unordered_map<RobotState, int, StateHash> &robotStateHistory) {
  if (current.minutesLeft == 0) {
    return current.items.geode;
  }

  auto it = robotStateHistory.find(current);
  if (it != robotStateHistory.end()) {
    return robotStateHistory[current];
  }
  // current.items = current.items + current.robots;
  auto toConstruct = bp.canBeConstructed(current.items);
  current.items = current.items + current.robots;
  current.minutesLeft -= 1;
  std::vector<int> scores;

  if (toConstruct.geode == 1) {
    RobotState newState = current;
    newState.robots.geode += 1;
    newState.items = newState.items - bp.rules[3];
    // BOOST_LOG_TRIVIAL(debug) << fmt::format("Construct geode, items = ({})", newState.items.toString());

    int score = run(newState, bp, robotStateHistory);
    robotStateHistory.insert({current, score});
    return score;
  }
  if (toConstruct.ore && (current.robots.ore < bp.maxRules.ore)) {
    RobotState newState = current;
    newState.robots.ore += 1;
    newState.items = newState.items - bp.rules[0];
    scores.push_back(run(newState, bp, robotStateHistory));
  }
  if (toConstruct.clay && (current.robots.clay < bp.maxRules.clay)) {
    RobotState newState = current;
    newState.robots.clay += 1;
    newState.items = newState.items - bp.rules[1];
    scores.push_back(run(newState, bp, robotStateHistory));
  }
  if (toConstruct.obsidian && (current.robots.obsidian < bp.maxRules.obsidian)) {
    RobotState newState = current;
    newState.robots.obsidian += 1;
    newState.items = newState.items - bp.rules[2];
    scores.push_back(run(newState, bp, robotStateHistory));
  }

  RobotState newState = current;
  scores.push_back(run(newState, bp, robotStateHistory));
  int score = (*max_element(scores.begin(), scores.end()));
  robotStateHistory.insert({current, score});
  return score;
}

std::vector<Blueprint> parseRobots(const std::vector<std::string> &data) {
  // Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay.
  // Each geode robot costs 3 ore and 8 obsidian.
  const boost::regex expr(
      "Blueprint (\\d*): Each ore robot costs (\\d*) ore. Each clay robot costs (\\d*) ore. Each obsidian robot "
      "costs (\\d*) ore and (\\d*) clay. Each geode robot costs (\\d*) ore and (\\d*) obsidian");
  std::vector<Blueprint> blueprints;
  for (const auto &x : data) {
    boost::smatch what;
    if (boost::regex_search(x, what, expr)) {
      std::vector<int> rules;
      for (uint i = 2; i < 8; ++i) {
        rules.push_back(stoi(what[i]));
      }
      blueprints.push_back({rules});
    }
  }
  return blueprints;
}

void day19Part1(const std::vector<Blueprint> &blueprints) {
  int index = 1;
  int qualityLevel = 0;
  for (const auto &bp : blueprints) {
    RobotState start;
    std::unordered_map<RobotState, int, StateHash> robotStateHistory;
    int maxNumberOfGeodes = run(start, bp, robotStateHistory);
    BOOST_LOG_TRIVIAL(debug) << fmt::format("BP {}, found {} geodes", index, maxNumberOfGeodes);
    qualityLevel += index * maxNumberOfGeodes;
    index++;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 quality level = {}", qualityLevel);
}

void day19Part2(const std::vector<Blueprint> &blueprints) {
  int qualityLevel = 1;
  for (int index = 0; index < 3; ++index) {
    RobotState start;
    start.minutesLeft = 32;
    std::unordered_map<RobotState, int, StateHash> robotStateHistory;
    int maxNumberOfGeodes = run(start, blueprints[index], robotStateHistory);
    BOOST_LOG_TRIVIAL(debug) << fmt::format("BP {}, found {} geodes", index, maxNumberOfGeodes);
    qualityLevel *= maxNumberOfGeodes;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 product = {}", qualityLevel);
}

void day19Run(bool test) {
  std::string fileName = fmt::format("../inputs/day19{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  auto blueprints = parseRobots(data);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {} blueprints", blueprints.size());
  // day19Part1(blueprints);
  day19Part2(blueprints);
}