#include "days.hpp"
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <fmt/format.h>
#include <iostream>
#include <map>
#include <memory>
#include <unordered_map>
#include <vector>

struct Valve {
  std::string name;
  std::vector<std::string> tunnels;
  int flow;
};

struct State {
  std::string valve;
  int remainingTime;
  std::set<std::string> openValves;
};

struct StateHash {
  std::size_t operator()(const State &k) const {
    std::string openValvesStr = fmt::format("{}", fmt::join(k.openValves, ""));
    return ((std::hash<std::string>()(k.valve) ^ (std::hash<int>()(k.remainingTime)) << 1) >> 1) ^
           (std::hash<std::string>()(openValvesStr) << 1);
  }
};

bool operator==(const State &a, const State &b) {
  return a.valve == b.valve && a.remainingTime == b.remainingTime && a.openValves == b.openValves;
}

// Valve OO has flow rate=10; tunnels lead to valves KK, HD, VS, KI
std::map<std::string, Valve> parseValves(const std::vector<std::string> &data) {
  const boost::regex expr("Valve ([A-Z]*) has flow rate=(\\d*); tunnels? leads? to valves? (.*)$");
  std::map<std::string, Valve> valves;
  for (const auto &x : data) {
    boost::smatch what;
    if (boost::regex_search(x, what, expr)) {
      Valve newValve;
      newValve.name = what[1];
      newValve.flow = stoi(what[2]);
      std::vector<std::string> result;
      boost::split(newValve.tunnels, what[3], boost::is_any_of(","));
      valves.insert(std::pair<std::string, Valve>(newValve.name, newValve));
    }
  }
  return valves;
}

std::pair<std::string, int> solve(const std::map<std::string, Valve> &valves,
                                  std::unordered_map<State, std::pair<std::string, int>, StateHash> &savedStates,
                                  State state) {
  bool openValve = (state.openValves.find(state.valve) != state.openValves.end());
  BOOST_LOG_TRIVIAL(debug) << fmt::format("At valve {} ({}), time = {}, open valves = {}", state.valve,
                                          (openValve ? "open" : "closed"), state.remainingTime,
                                          fmt::join(state.openValves, ","));
  std::string openValvesStr = fmt::format("{}", fmt::join(state.openValves, ""));
  auto it = savedStates.find(state);
  if (it != savedStates.end()) {
    if (it->first.openValves.size() > 0) {
      BOOST_LOG_TRIVIAL(debug) << fmt::format("Already computed valve {}, time = {}, open valves = {}", it->first.valve,
                                              it->first.remainingTime, fmt::join(it->first.openValves, ","));
    }
    return savedStates[state];
  }

  if (state.remainingTime <= 0) {
    return {openValvesStr, 0};
  }
  auto currentValve = valves.find(state.valve);

  std::vector<std::pair<std::string, int>> scores;

  for (auto sub : currentValve->second.tunnels) {
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Going from {} to {}", state.valve, sub);
    if (openValve == false && currentValve->second.flow != 0) {
      State newState2{sub, state.remainingTime - 2, state.openValves};
      int remainingTime = state.remainingTime - 1;
      newState2.openValves.insert(state.valve);
      auto newScore = solve(valves, savedStates, newState2);
      newScore.second += currentValve->second.flow * remainingTime;
      scores.push_back(newScore);
    }
    State newState{sub, state.remainingTime - 1, state.openValves};
    scores.push_back(solve(valves, savedStates, newState));
  }

  std::sort(scores.begin(), scores.end(), [](const auto &a, const auto &b) { return a.second > b.second; });
  savedStates.insert({state, scores[0]});
  return scores[0];
}

int part1Recur(const std::map<std::string, Valve> &valves) {
  std::unordered_map<State, std::pair<std::string, int>, StateHash> savedStates;
  State start{"AA", 30, {}};
  auto ans = solve(valves, savedStates, start);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Open valves {}", ans.first);
  return ans.second;
}

int part2Recur(const std::map<std::string, Valve> &valves) {
  std::unordered_map<State, std::pair<std::string, int>, StateHash> savedStates;
  State start{"AA", 26, {}};
  auto ans = solve(valves, savedStates, start);
  BOOST_LOG_TRIVIAL(info) << fmt::format("First run, score = {}, open valves {}", ans.second, ans.first);
  State elephant{"AA", 26, {}};
  savedStates = {};
  for (uint x = 0; x < ans.first.size() - 1; x += 2) {
    elephant.openValves.insert(ans.first.substr(x, 2));
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Elephant state = {}", fmt::join(elephant.openValves, ","));
  auto newAns = solve(valves, savedStates, elephant);
  return ans.second + newAns.second;
}

void day16Run(bool test) {
  std::string fileName = fmt::format("../inputs/day16{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  auto valves = parseValves(data);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {} valves", valves.size());

  auto resultPart1 = part1Recur(valves);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 max pressure =  {}", resultPart1);

  auto resultPart2 = part2Recur(valves);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 max pressure =  {}", resultPart2);
}