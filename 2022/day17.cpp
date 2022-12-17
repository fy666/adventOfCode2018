#include "days.hpp"
#include <fmt/format.h>
#include <iostream>
#include <map>
#include <vector>

const int GRID_COLUMNS = 7;
int convert(std::pair<int, int> input) { return input.second * GRID_COLUMNS + input.first; }
std::pair<int, int> convert(int input) { return {input % GRID_COLUMNS, input / GRID_COLUMNS}; }

class RockShape {
public:
  int columns;
  int lines;
  std::function<std::set<int>(std::pair<int, int>)> getPositions;
};

std::vector<int> getState(const std::set<int> &grid, int rockIndex, int streamIndex) {
  std::vector<int> maxPerColumn{-1, -1, -1, -1, -1, -1, -1};
  for (const auto &x : grid) {
    std::pair<int, int> pos = convert(x);
    maxPerColumn[pos.first] = std::max(maxPerColumn[pos.first], pos.second);
  }
  int maxCol = (*max_element(maxPerColumn.begin(), maxPerColumn.end()));
  for (uint x = 0; x < maxPerColumn.size(); ++x) {
    maxPerColumn[x] = maxCol - maxPerColumn[x];
  }
  maxPerColumn.push_back(rockIndex);
  maxPerColumn.push_back(streamIndex);
  return maxPerColumn;
}

int addOneRock(std::set<int> &grid, const std::string &hotSteam, int hotSteamIndex, const RockShape &rock) {
  std::pair<int, int> rockBottomLeftPosition{2, 3};
  if (grid.size()) {
    std::pair<int, int> highestrock = convert(*grid.rbegin());
    rockBottomLeftPosition.second = highestrock.second + 4;
  }
  BOOST_LOG_TRIVIAL(trace) << fmt::format("Start Bottom left position = {},{} ", rockBottomLeftPosition.first,
                                          rockBottomLeftPosition.second);
  int counter = 0;
  // while no collision or stop
  while (1) {
    auto newPosition = rockBottomLeftPosition;

    if (counter % 2 == 1) {
      /* Move down */
      newPosition.second -= 1;
    } else {
      /* Hot steam */
      if (hotSteam[hotSteamIndex] == '>') {
        newPosition.first += 1;
      } else {
        newPosition.first -= 1;
      }
      hotSteamIndex = (hotSteamIndex + 1) % hotSteam.size();
    }

    BOOST_LOG_TRIVIAL(trace) << fmt::format("Going to {},{} ", newPosition.first, newPosition.second);

    /* Check collision with grid */
    bool collision = false;
    collision =
        (newPosition.second < 0) || (newPosition.first + rock.columns) > GRID_COLUMNS || (newPosition.first < 0);

    /* Check collusion with other rocks */
    if (collision == false) {
      auto rockPositions = rock.getPositions(newPosition);
      std::vector<int> common_data;
      set_intersection(grid.begin(), grid.end(), rockPositions.begin(), rockPositions.end(),
                       std::back_inserter(common_data));
      collision = (common_data.size() != 0);
    }

    /* Collision detected */
    if (collision) {
      if (counter % 2 == 0) {
        /* Collision left or right, continue */
        counter++;
        continue;
      }
      /* Add previous pos to grid set, and move to next piece */
      BOOST_LOG_TRIVIAL(trace) << fmt::format("Collision detected ! Adding {},{} ", rockBottomLeftPosition.first,
                                              rockBottomLeftPosition.second);
      auto rockPositions = rock.getPositions(rockBottomLeftPosition);
      grid.insert(rockPositions.begin(), rockPositions.end());
      return hotSteamIndex;
    }
    counter++;
    rockBottomLeftPosition = newPosition;
  }
  return hotSteamIndex;
}

void day17Run(bool test) {
  std::string fileName = fmt::format("../inputs/day17{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  BOOST_LOG_TRIVIAL(info) << fmt::format("{} steam commands", data[0].size());

  /* Define shapes */
  RockShape rockshapes[5];

  /* 0: horizontal line */
  int rockIndex = 0;
  rockshapes[rockIndex].columns = 4;
  rockshapes[rockIndex].lines = 1;
  rockshapes[rockIndex].getPositions = [](std::pair<int, int> bl) {
    std::set<int> result;
    for (int i = 0; i < 4; ++i) {
      result.insert(convert({bl.first + i, bl.second}));
    }
    return result;
  };
  rockIndex += 1;

  /* 1 : square */
  rockshapes[rockIndex].columns = 3;
  rockshapes[rockIndex].lines = 3;
  rockshapes[rockIndex].getPositions = [](std::pair<int, int> bl) {
    std::set<int> result;
    result.insert(convert({bl.first + 1, bl.second + 1}));
    result.insert(convert({bl.first + 1, bl.second}));
    result.insert(convert({bl.first, bl.second + 1}));
    result.insert(convert({bl.first + 2, bl.second + 1}));
    result.insert(convert({bl.first + 1, bl.second + 2}));
    return result;
  };
  rockIndex += 1;

  /* 2 : corner */
  rockshapes[rockIndex].columns = 3;
  rockshapes[rockIndex].lines = 3;
  rockshapes[rockIndex].getPositions = [](std::pair<int, int> bl) {
    std::set<int> result;
    result.insert(convert({bl.first, bl.second}));
    result.insert(convert({bl.first + 1, bl.second}));
    result.insert(convert({bl.first + 2, bl.second}));
    result.insert(convert({bl.first + 2, bl.second + 1}));
    result.insert(convert({bl.first + 2, bl.second + 2}));
    return result;
  };
  rockIndex += 1;

  /* 3 : vertical line */
  rockshapes[rockIndex].columns = 1;
  rockshapes[rockIndex].lines = 4;
  rockshapes[rockIndex].getPositions = [](std::pair<int, int> bl) {
    std::set<int> result;
    for (int i = 0; i < 4; ++i) {
      result.insert(convert({bl.first, bl.second + i}));
    }
    return result;
  };
  rockIndex += 1;

  /* 4 : cube */
  rockshapes[rockIndex].columns = 2;
  rockshapes[rockIndex].lines = 2;
  rockshapes[rockIndex].getPositions = [](std::pair<int, int> bl) {
    std::set<int> result;
    for (int j = 0; j < 2; ++j) {
      for (int i = 0; i < 2; ++i) {
        result.insert(convert({bl.first + i, bl.second + j}));
      }
    }
    return result;
  };

  rockIndex = 0;
  int hotSteamIndex = 0;
  std::string hotSteam = data[0];
  std::set<int> grid;
  int part1Pieces = 2022;
  int64_t part2Pieces = 1000000000000;

  std::vector<std::vector<int>> lastColumnShapes;
  std::vector<int> heights;

  for (uint64_t x = 0;; ++x) {
    hotSteamIndex = addOneRock(grid, hotSteam, hotSteamIndex, rockshapes[rockIndex]);
    heights.push_back((convert(*grid.rbegin()).second + 1));

    std::vector<int> res = getState(grid, rockIndex, hotSteamIndex);
    auto it = std::find(lastColumnShapes.begin(), lastColumnShapes.end(), res);
    if (it != lastColumnShapes.end()) {
      int index = it - lastColumnShapes.begin();
      int addedHeightPercycle = heights[x] - heights[index];
      int cycle = x - index;
      BOOST_LOG_TRIVIAL(debug) << fmt::format("Found repetition between {} and {}, cycle = {}, dh = {} ", index, x,
                                              cycle, addedHeightPercycle);
      /* Part 1 */
      int64_t part1cycles = (part1Pieces - index) / (cycle);
      int part1remainder = (part1Pieces - index) % cycle;
      int64_t part1Height = part1cycles * addedHeightPercycle + heights[part1remainder + index - 1];
      BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 height = {}", part1Height);
      /* Part 2 */
      int64_t part2cycles = (part2Pieces - index) / (cycle);
      int part2remainder = (part2Pieces - index) % cycle;
      int64_t part2Height = part2cycles * addedHeightPercycle + heights[part2remainder + index - 1];
      BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 height = {}", part2Height);
      break;
    }
    lastColumnShapes.push_back(res);

    rockIndex = (rockIndex + 1) % 5;
  }
}