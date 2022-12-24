#include "days.hpp"
#include <algorithm>
#include <iostream>
#include <limits.h>
#include <map>
#include <vector>

std::vector<std::vector<Point>> MOVES{{{-1, -1}, {0, -1}, {1, -1}}, /* North */
                                      {{-1, 1}, {0, 1}, {1, 1}},    /* South */
                                      {{-1, -1}, {-1, 0}, {-1, 1}}, /* West */
                                      {{1, -1}, {1, 0}, {1, 1}}};   /* East */

std::vector<Point> ALL_MOVES{{-1, -1}, {0, -1}, {1, -1}, {0, 1}, {-1, 0}, {-1, 1}, {1, 0}, {1, 1}};

void parseElves(const std::vector<std::string> &data, std::set<Point> &elves) {
  int line = 0;
  for (const auto &x : data) {
    for (uint i = 0; i < x.size(); ++i) {
      if (x[i] == '#') {
        elves.insert({i, line});
      }
    }
    line++;
  }
}

int getEmptyTilesOnBiggestRect(const std::set<Point> &elves) {
  int xmin = INT_MAX;
  int xmax = 0;
  int ymin = INT_MAX;
  int ymax = 0;
  for (const auto &elve : elves) {
    xmin = std::min(xmin, elve.first);
    xmax = std::max(xmax, elve.first);
    ymin = std::min(ymin, elve.second);
    ymax = std::max(ymax, elve.second);
  }

  int dx = xmax - xmin + 1;
  int dy = ymax - ymin + 1;
  int emptyTiles = dx * dy - elves.size();
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Square of {}x{}, empty tiles = {}", dx, dy, emptyTiles);
  return emptyTiles;
}

std::set<Point> moveElves(const std::set<Point> &elves, int &moveIndex) {
  std::set<Point> elvesNewPos;
  std::map<Point, std::vector<Point>> potentialMoves;
  for (const auto &elve : elves) {
    bool nobodyAround = std::all_of(ALL_MOVES.begin(), ALL_MOVES.end(), [&elves, &elve](const auto &P) {
      Point newPos = elve + P;
      return elves.find(newPos) == elves.end();
    });
    if (nobodyAround) {
      elvesNewPos.insert(elve); /* Elve doesnt move */
    }
    if (nobodyAround == false) {
      /* Add move to potential moves */
      bool found = false;
      for (int ix = 0; ix < MOVES.size(); ix++) {
        int index = (ix + moveIndex) % MOVES.size();
        bool nobodyAround = std::all_of(MOVES[index].begin(), MOVES[index].end(), [&elves, &elve](const auto &P) {
          Point newPos = elve + P;
          return elves.find(newPos) == elves.end();
        });
        if (nobodyAround) {
          Point newPos = elve + MOVES[index][1];
          potentialMoves[newPos].push_back(elve);
          found = true;
          break;
        }
      }
      if (found == false) {
        elvesNewPos.insert(elve); /* Elve doesnt move */
      }
    }
  }

  for (const auto &potentialMove : potentialMoves) {
    if (potentialMove.second.size() == 1) {
      elvesNewPos.insert(potentialMove.first);
    } else {
      for (auto x : potentialMove.second) {
        elvesNewPos.insert(x);
      }
    }
  }
  moveIndex += 1;
  return elvesNewPos;
}

void printElves(const std::set<Point> &elves) {
  int xmin = INT_MAX;
  int xmax = 0;
  int ymin = INT_MAX;
  int ymax = 0;
  for (const auto &elve : elves) {
    xmin = std::min(xmin, elve.first);
    xmax = std::max(xmax, elve.first);
    ymin = std::min(ymin, elve.second);
    ymax = std::max(ymax, elve.second);
  }

  xmin -= 1;
  ymin -= 1;
  xmax += 1;
  ymax += 1;

  for (int y = ymin; y < ymax; ++y) {
    std::string tmp;
    for (int x = xmin; x < xmax; ++x) {
      if (elves.find({x, y}) != elves.end()) {
        tmp += '#';
      } else {
        tmp += '.';
      }
    }
    std::cout << tmp << std::endl;
  }
}

void day23Run(bool test) {
  std::string fileName = fmt::format("../inputs/day23{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());

  std::set<Point> elves;
  parseElves(data, elves);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {} elves", elves.size());
  // printElves(elves);
  int moveIndex = 0;
  int resPart1 = 0;
  int resPart2 = 0;
  for (int x = 1;; ++x) {
    auto newElves = moveElves(elves, moveIndex);
    if (newElves == elves) {
      resPart2 = x;
    }
    elves = newElves;
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Round {}, {} elves, moveIndex = {}", x, elves.size(), moveIndex);
    //  printElves(elves);
    if (x == 10) {
      resPart1 = getEmptyTilesOnBiggestRect(elves);
    }

    if (resPart1 != 0 && resPart2 != 0) {
      break;
    }
  }

  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", resPart1);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", resPart2);
}