#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

std::vector<char> day12Parser(const std::string &x) { return {x.begin(), x.end()}; }
typedef std::pair<int, int> couple;

struct Position {
  int x;
  int y;
};

struct Path {
  Position position;
  int steps = 0;
};

int stepsToFinal(const std::vector<std::vector<char>> &data, Position start) {
  int dir[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
  std::list<Path> paths;

  paths.push_back({start});
  bool keepLooping = true;
  std::map<std::pair<int, int>, int> visitedPositions;

  while (paths.size() && keepLooping) {
    auto p = paths.front();
    BOOST_LOG_TRIVIAL(debug) << fmt::format("{} paths, treating path of size {}", paths.size(), p.steps);

    char currentVal = data[p.position.x][p.position.y];
    if (currentVal == 'S') {
      currentVal = 'a';
    }

    if (currentVal == 'E') {
      BOOST_LOG_TRIVIAL(debug) << fmt::format("Found stop ! at {} {} after {} steps", p.position.x, p.position.y,
                                              p.steps);
      return p.steps;
      keepLooping = false;
    }
    for (uint i = 0; i < 4; ++i) {
      Position newPos{p.position.x + dir[i][0], p.position.y + dir[i][1]};
      if (newPos.x >= 0 && newPos.y >= 0 && newPos.x < data.size() && newPos.y < data[0].size()) {
        char newVal = data[newPos.x][newPos.y];
        if (newVal == 'E') {
          newVal = 'z';
        }
        if (visitedPositions.find({newPos.x, newPos.y}) != visitedPositions.end()) {
          BOOST_LOG_TRIVIAL(debug) << fmt::format("Not adding ({},{}) because duplicate", newPos.x, newPos.y);
        } else if (newVal <= (currentVal + 1)) {
          BOOST_LOG_TRIVIAL(debug) << fmt::format("Adding new pos {} {} in path. current val = {}, new Val = {}",
                                                  newPos.x, newPos.y, currentVal, newVal);
          Path newPath = p;
          newPath.position = newPos;
          newPath.steps += 1;
          paths.push_back(newPath);
          visitedPositions[{newPos.x, newPos.y}] = 1;
        } else {
          BOOST_LOG_TRIVIAL(debug) << fmt::format(
              "Not adding ({},{}) because wrong value. current val = {}, new Val = {}", newPos.x, newPos.y, currentVal,
              newVal);
        }
      }
    }
    paths.pop_front();
  }
  return 1e6;
}

void day12Run(bool test) {
  std::string fileName = fmt::format("../inputs/day12{}.txt", test ? "_test" : "");
  auto data = read_file<std::vector<char>>(fileName, day12Parser);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  Position start;
  std::vector<Position> starts;
  int lineCounter = 0;
  for (const auto &line : data) {
    auto it = std::find(line.begin(), line.end(), 'S');
    if (it != line.end()) {
      int column = it - line.begin();
      start.x = lineCounter;
      start.y = column;
    }
    auto it2 = std::find(line.begin(), line.end(), 'a');
    if (it2 != line.end()) {
      int column = it2 - line.begin();
      starts.push_back({lineCounter, column});
    }
    lineCounter += 1;
  }

  BOOST_LOG_TRIVIAL(info) << fmt::format("Found {} start positions", starts.size());

  int result = stepsToFinal(data, start);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {} steps", result);
  std::vector<int> results;
  for (const auto &pos : starts) {
    results.push_back(stepsToFinal(data, pos));
  }
  std::sort(results.begin(), results.end());
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {} steps", results.front());
  // BOOST_LOG_TRIVIAL(debug) << fmt::format("Start position at {} {}", start.position.x, start.position.y);
}