#include "days.hpp"
#include <iostream>
#include <map>
#include <memory>
#include <set>
#include <vector>

std::vector<int> day8parser(const std::string x) {
  std::vector<int> result;
  for (const auto &c : x) {
    result.push_back(int(c) - 48);
  }
  return result;
}

std::pair<int, bool> view(const std::vector<std::vector<int>> &data, int line, int col, const int direction[2]) {
  bool progress = true;
  int distance = 0;
  bool touchEdge = true;
  bool continuousView = true;
  int treeValue = data[line][col];
  int numLines = data.size();
  int numCols = data[0].size();

  while (1) {
    if (line == 0 || col == 0 || line == numLines - 1 || col == numCols - 1) {
      break;
    }
    line += direction[0];
    col += direction[1];
    if (data[line][col] < treeValue && continuousView) {
      distance += 1;
    } else if (continuousView) {
      distance += 1;
      continuousView = false;
    }
    if (data[line][col] >= treeValue) {
      touchEdge = false;
    }
  }
  return {distance, touchEdge};
}

std::pair<int, int> solve(const std::vector<std::vector<int>> &data) {
  int numLines = data.size();
  int numCols = data[0].size();
  int countTreeView = 0;
  int maxTreeView = 0;
  int directions[4][2]{{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

  for (int line = 1; line < numLines - 1; ++line) {
    for (int col = 1; col < numCols - 1; ++col) {
      int treeView = 1;
      int treeVisibility = 0;
      for (const auto &dir : directions) {
        int distance;
        bool visible;
        std::tie(distance, visible) = view(data, line, col, dir);
        if (visible) {
          treeVisibility = 1;
        }
        treeView *= distance;
      }
      countTreeView += treeVisibility;
      maxTreeView = std::max(treeView, maxTreeView);
    }
  }
  int edges = (2 * numCols) + (2 * numLines) - 4;
  return {countTreeView + edges, maxTreeView};
}

void day8Run(bool test) {
  std::string fileName = fmt::format("../inputs/day8{}.txt", test ? "_test" : "");
  auto data = read_file<std::vector<int>>(fileName, day8parser);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  int numLines = data.size();
  int numCols = data[0].size();
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read matrix of {}x{}", numLines, numCols);

  int visibleTrees, maxTreeView;
  std::tie(visibleTrees, maxTreeView) = solve(data);
  BOOST_LOG_TRIVIAL(info) << fmt::format("{} visible trees", visibleTrees);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Max tree view = {}", maxTreeView);
}