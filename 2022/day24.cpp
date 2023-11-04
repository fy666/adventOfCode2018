#include "days.hpp"
#include <algorithm>
#include <iostream>
#include <map>
#include <unordered_set>
#include <vector>

std::map<char, Point> OBS_DIRECTIONS = {{'>', {0, 1}}, {'<', {0, -1}}, {'^', {-1, 0}}, {'v', {1, 0}}, {'#', {0, 0}}};
std::map<Point, char> DIRECTIONS_OBS = {{{0, 1}, '>'}, {{0, -1}, '<'}, {{-1, 0}, '^'}, {{1, 0}, 'v'}, {{0, 0}, '#'}};

Point parseDay24(const std::vector<std::string> &data, std::map<Point, std::vector<Point>> &obstacles) {

  int x = 0;
  for (const auto &s : data) {
    for (int y = 0; y < s.size(); ++y) {
      if (s[y] != '.') {
        obstacles[{x, y}].push_back(OBS_DIRECTIONS[s[y]]);
      }
    }
    ++x;
  }
  return {x, data[0].size()};
}

void printMap(std::map<Point, std::vector<Point>> &obstacles, Point mapSize) {
  std::cout << "***************" << std::endl;
  for (int x = 0; x < mapSize.first; ++x) {
    for (int y = 0; y < mapSize.second; ++y) {
      auto it = obstacles.find({x, y});
      if (it == obstacles.end()) {
        std::cout << ".";
      } else {
        if (it->second.size() == 1) {
          std::cout << DIRECTIONS_OBS[it->second[0]];
        } else {
          std::cout << it->second.size();
        }
      }
    }
    std::cout << std::endl;
  }
  std::cout << "***************" << std::endl;
}

int customModulo(int x, int N) {
  // int res = positive_modulo(x, N);
  int res = x;
  if (res == 0) {
    return N - 2;
  } else if (res == N - 1) {
    return 1;
  }
  return res;
}

std::map<Point, std::vector<Point>> computeNextState(std::map<Point, std::vector<Point>> &obstacles, Point mapSize) {
  std::map<Point, std::vector<Point>> newObstacles;
  for (const auto &[pos, items] : obstacles) {
    for (const auto &dir : items) {
      if (dir.first == 0 && dir.second == 0) {
        newObstacles[pos].push_back(dir);
      } else {
        Point newPos = pos + dir;
        newPos.first = customModulo(newPos.first, mapSize.first);
        newPos.second = customModulo(newPos.second, mapSize.second);
        newObstacles[newPos].push_back(dir);
      }
    }
  }
  return newObstacles;
}

struct BlizzardPath {
  Point position;
  int steps = 0;
  int score = 0;
};

struct BlizzardHash {
  std::size_t operator()(const BlizzardPath &k) const {
    std::vector<int> vec{k.position.first, k.position.second, k.steps};
    std::size_t ret = 0;
    for (auto &i : vec) {
      ret ^= std::hash<uint32_t>()(i);
    }
    return ret;
  }
};

bool operator==(const BlizzardPath &a, const BlizzardPath &b) { return a.position == b.position && a.steps == b.steps; }

int getScore(const BlizzardPath &a, const Point &b) {
  return abs(a.position.first - b.first) + abs(a.position.second - b.second) + a.steps;
}

bool compareBlizzard(const BlizzardPath &a, const BlizzardPath &b) { return a.score < b.score; }
std::string getString(const BlizzardPath &a) {
  return fmt::format("({},{}),{}, score={}", a.position.first, a.position.second, a.steps, a.score);
}

BlizzardPath shortestPathToExit(std::vector<std::map<Point, std::vector<Point>>> &states, Point mapSize,
                                BlizzardPath start, Point targetPosition) {
  std::vector<Point> POT_MOVES = {{0, 1}, {0, -1}, {-1, 0}, {1, 0}, {0, 0}};
  start.score = getScore(start, targetPosition);
  std::list<BlizzardPath> paths{start};
  std::unordered_set<BlizzardPath, BlizzardHash> alreadyVisited{start};

  int countIterations = 0;
  while (paths.size()) {
    paths.sort(compareBlizzard);

    auto current = paths.front();
    if (current.position == targetPosition) {
      return current;
    }
    for (const auto &move : POT_MOVES) {
      BlizzardPath newPosition;
      newPosition.position = current.position + move;
      newPosition.steps = current.steps + 1;
      if (newPosition.position.first < 0 || newPosition.position.second < 0 ||
          newPosition.position.first >= mapSize.first || newPosition.position.second >= mapSize.second) {
        continue;
      }
      newPosition.score = getScore(newPosition, targetPosition);
      if (alreadyVisited.find(newPosition) != alreadyVisited.end()) {
        continue;
      }
      while (states.size() <= newPosition.steps) {
        states.push_back(computeNextState(states.back(), mapSize));
      }
      auto &blizzardMap = states[newPosition.steps];

      if (blizzardMap.find(newPosition.position) == blizzardMap.end()) {
        paths.push_back(newPosition);
        alreadyVisited.insert(newPosition);
      }
    }

    paths.pop_front();
    ++countIterations;
  }
  return {};
}

void day24Run(bool test) {
  std::string fileName = fmt::format("../inputs/day24{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  std::map<Point, std::vector<Point>> obstacles;
  Point mapSize = parseDay24(data, obstacles);

  BOOST_LOG_TRIVIAL(debug) << fmt::format("Map of {}x{}, {} obstacles positions found", mapSize.first, mapSize.second,
                                          obstacles.size());

  std::vector<std::map<Point, std::vector<Point>>> states{obstacles};

  Point start = {0, 1};
  Point target = {mapSize.first - 1, mapSize.second - 2};

  BlizzardPath startPosition = {.position = {0, 1}, .steps = 0};
  auto result = shortestPathToExit(states, mapSize, startPosition, target);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Shortest Path for Part 1 = {}", result.steps);

  result = shortestPathToExit(states, mapSize, result, start);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Shortest return trip = {}", result.steps);

  result = shortestPathToExit(states, mapSize, result, target);

  BOOST_LOG_TRIVIAL(info) << fmt::format("Shortest Path for Part 2 = {}", result.steps);
}