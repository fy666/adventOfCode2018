#include "days.hpp"
#include <boost/algorithm/string.hpp>
#include <iostream>
#include <map>
#include <vector>

typedef std::pair<int, int> Point;

void printGrid(const std::set<std::pair<int, int>> &rocks) {
  for (uint x = 0; x < 10; ++x) {
    for (uint y = 494; y < 504; ++y) {
      if (rocks.find({y, x}) == rocks.end()) {
        std::cout << ". ";
      } else {
        std::cout << "# ";
      }
    }
    std::cout << std::endl;
  }
}

uint fillRocks(const std::vector<std::string> &data, std::set<std::pair<int, int>> &rocks) {
  const boost::regex expr("(\\d*),(\\d*)");
  boost::sregex_token_iterator end;
  uint lowestRock = 0;
  for (const auto &x : data) {
    boost::sregex_token_iterator iter(x.begin(), x.end(), expr, 0);
    std::vector<Point> vectorOfRocks;
    for (; iter != end; ++iter) {
      std::vector<std::string> result;
      boost::split(result, *iter, boost::is_any_of(","));
      vectorOfRocks.push_back({stoi(result[0]), stoi(result[1])});
    }
    for (uint i = 0; i < vectorOfRocks.size() - 1; ++i) {
      uint startx = std::min(vectorOfRocks[i].first, vectorOfRocks[i + 1].first);
      uint stopx = std::max(vectorOfRocks[i].first, vectorOfRocks[i + 1].first);
      uint starty = std::min(vectorOfRocks[i].second, vectorOfRocks[i + 1].second);
      uint stopy = std::max(vectorOfRocks[i].second, vectorOfRocks[i + 1].second);
      for (uint ix = startx; ix <= stopx; ++ix) {
        for (uint iy = starty; iy <= stopy; ++iy) {
          rocks.insert({ix, iy});
          lowestRock = std::max(lowestRock, iy);
        }
      }
    }
  }
  return lowestRock;
}

bool pourSand(std::set<std::pair<int, int>> &rocks, uint lowestRock) {
  Point pos{500, 0};
  bool continueDown = true;
  bool isRested = false;
  while (continueDown) {
    if (rocks.find({pos.first, pos.second + 1}) == rocks.end()) {
      pos.second += 1;
    } else if (rocks.find({pos.first - 1, pos.second + 1}) == rocks.end()) {
      pos.first -= 1;
      pos.second += 1;
    } else if (rocks.find({pos.first + 1, pos.second + 1}) == rocks.end()) {
      pos.first += 1;
      pos.second += 1;
    } else {
      continueDown = false;
      isRested = true;
      rocks.insert(pos);
    }
    if (pos.second > lowestRock) {
      continueDown = false;
    }
  }
  return isRested;
}

bool pourSandPart2(std::set<std::pair<int, int>> &rocks, uint lowestRock) {
  Point pos{500, 0};
  bool continueDown = true;

  while (continueDown) {
    if (rocks.find({pos.first, pos.second + 1}) == rocks.end()) {
      pos.second += 1;
    } else if (rocks.find({pos.first - 1, pos.second + 1}) == rocks.end()) {
      pos.first -= 1;
      pos.second += 1;
    } else if (rocks.find({pos.first + 1, pos.second + 1}) == rocks.end()) {
      pos.first += 1;
      pos.second += 1;
    } else {
      if (pos.first == 500 && pos.second == 0) {
        return false;
      }
      continueDown = false;
      rocks.insert(pos);
    }
    if (pos.second == lowestRock) {
      continueDown = false;
      rocks.insert(pos);
    }
  }
  return true;
}

void day14Run(bool test) {
  std::string fileName = fmt::format("../inputs/day14{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());

  std::set<std::pair<int, int>> rocks;
  uint lowestRock = 0;
  lowestRock = fillRocks(data, rocks);
  std::set<std::pair<int, int>> rocksPart2 = rocks;
  BOOST_LOG_TRIVIAL(debug) << fmt::format("{} rocks found, lowest rock at {}", rocks.size(), lowestRock);

  // printGrid();

  int sandCount = 0;
  while (pourSand(rocks, lowestRock)) {
    sandCount += 1;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 sand count = {} ", sandCount);

  int sandCount2 = 1;
  while (pourSandPart2(rocksPart2, lowestRock + 1)) {
    sandCount2 += 1;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 sand count = {}", sandCount2);
}