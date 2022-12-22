#include "days.hpp"
#include <boost/algorithm/string.hpp>
#include <boost/tokenizer.hpp>
#include <iostream>
#include <map>
#include <vector>

typedef std::pair<int, int> Point;

std::map<char, Point> DIRECTIONS = {{'>', {0, 1}}, {'<', {0, -1}}, {'^', {-1, 0}}, {'v', {1, 0}}};
std::map<char, int> DIRECTION_SCORE = {{'>', 0}, {'v', 1}, {'<', 2}, {'^', 3}};

std::map<char, char> DIRECTION_R = {{'>', 'v'}, {'v', '<'}, {'<', '^'}, {'^', '>'}};
std::map<char, char> DIRECTION_L = {{'>', '^'}, {'^', '<'}, {'<', 'v'}, {'v', '>'}};

bool operator==(const Point &a, const Point &b) { return a.first == b.first && a.second == b.second; }

Point operator+(const Point &a, const Point &b) {
  Point res;
  return {a.first + b.first, a.second + b.second};
}

class Cube;

struct NextPoint {
  Point point;
  char direction;
  const Cube *cube;
};

Point getPointAfterRotation(Point a, char originalDirection, char newDirection, int size) {
  if (originalDirection == '>' && newDirection == '>') {
    return {a.first, 0};
  }
  if (originalDirection == '<' && newDirection == '<') {
    return {a.first, size - 1};
  }
  if (originalDirection == '^' && newDirection == '^') {
    return {size - 1, a.second};
  }
  if (originalDirection == 'v' && newDirection == 'v') {
    return {0, a.second};
  }

  /* 90 rotations to left */
  if (originalDirection == '<' && newDirection == 'v') {
    return {0, a.first};
  }
  if (originalDirection == 'v' && newDirection == '>') {
    return {size - 1 - a.first, 0};
  }
  if (originalDirection == '>' && newDirection == '^') {
    return {size - 1, a.first};
  }
  if (originalDirection == '^' && newDirection == '<') {
    return {size - 1 - a.first, size - 1};
  }

  /* 90 rotations to right */
  if (originalDirection == '<' && newDirection == '^') {
    return {size - 1, size - 1 - a.first};
  }
  if (originalDirection == '^' && newDirection == '>') {
    return {a.second, 0};
  }
  if (originalDirection == '>' && newDirection == 'v') {
    return {0, size - 1 - a.first};
  }
  if (originalDirection == 'v' && newDirection == '<') {
    return {a.second, size - 1};
  }

  /* 180 rotations */
  if (originalDirection == '<' && newDirection == '>') {
    return {size - a.first - 1, 0};
  }
  if (originalDirection == '>' && newDirection == '<') {
    return {size - a.first - 1, size - 1};
  }
  if (originalDirection == '^' && newDirection == 'v') {
    return {0, size - a.second - 1};
  }
  if (originalDirection == 'v' && newDirection == '^') {
    return {size - 1, size - a.second - 1};
  }
  BOOST_LOG_TRIVIAL(warning) << "Combination not found" << std::endl;
  return {0, 0};
}

class Cube {
public:
  int size;
  std::vector<std::string> map;
  Point topLeftCubePos;
  Point topLeftMapPos;
  std::map<char, std::pair<const Cube *, char>> adjacentCubes;

  // Return true if can be at this position
  bool getVal(Point pos) const { return map[pos.first][pos.second] == '.'; }

  void printAdjacentCubes() const {
    BOOST_LOG_TRIVIAL(info) << fmt::format("Adjacent cubes for {},{}:", topLeftCubePos.first, topLeftCubePos.second);
    for (auto direction : {'<', '>', '^', 'v'}) {
      auto item = adjacentCubes.find(direction);
      if (item != adjacentCubes.end()) {
        auto it = item->second;
        BOOST_LOG_TRIVIAL(info) << fmt::format("Adjacent cube in dir {} = {},{}, new dir = {}", direction,
                                               it.first->topLeftCubePos.first, it.first->topLeftCubePos.second,
                                               it.second);
      }
    }
  }

  void computeAdjacentCubesPart1(const std::vector<Cube> &cubes, int mapCubeSize) {

    for (auto direction : {'<', '>', '^', 'v'}) {
      Point dir = DIRECTIONS[direction];
      Point tl = topLeftCubePos + dir;
      tl.first = positive_modulo(tl.first, mapCubeSize);
      tl.second = positive_modulo(tl.second, mapCubeSize);
      auto it = std::find_if(cubes.begin(), cubes.end(), [tl](const auto &cube) { return cube.topLeftCubePos == tl; });
      while (it == cubes.end()) {
        tl = tl + dir;
        tl.first = positive_modulo(tl.first, mapCubeSize);
        tl.second = positive_modulo(tl.second, mapCubeSize);
        it = std::find_if(cubes.begin(), cubes.end(), [tl](const auto &cube) { return cube.topLeftCubePos == tl; });
      }
      adjacentCubes[direction] = {&(*it), direction};
    }
  }

  NextPoint getNextPart1(const NextPoint &p) const {
    NextPoint result;
    result.direction = p.direction;
    result.point = p.point + DIRECTIONS[p.direction];
    BOOST_LOG_TRIVIAL(debug) << fmt::format("{},{} to {},{}", p.point.first, p.point.second, result.point.first,
                                            result.point.second);
    auto adjacent = adjacentCubes.find(p.direction)->second;
    result.cube = adjacent.first;
    result.direction = adjacent.second;
    if (result.point.first < 0 || result.point.second < 0 || result.point.first >= size ||
        result.point.second >= size) {
      result.point = getPointAfterRotation(result.point, p.direction, result.direction, size);
    } else {
      result.cube = this;
    }

    return result;
  }

  void print() const {
    for (const auto &l : map) {
      BOOST_LOG_TRIVIAL(debug) << l;
    }
  }
};

std::string parseDay22(const std::vector<std::string> &data, std::vector<Cube> &cubes) {
  bool inputIsMap = true;
  int lineCounter = 0;
  int mapSize = 0;
  int cubeSize = 1000;
  std::string commandList;
  for (const auto &x : data) {
    if (x.size() == 0) {
      BOOST_LOG_TRIVIAL(debug) << fmt::format("Map ends after {} lines", lineCounter);
      inputIsMap = false;
    } else if (inputIsMap) {
      lineCounter++;
      mapSize = std::max(mapSize, int(x.size()));
      std::string tmp = x;
      boost::erase_all(tmp, " ");
      cubeSize = std::min(cubeSize, int(tmp.size()));
    } else {
      commandList = x;
    }
  }
  mapSize = std::max(mapSize, lineCounter);
  int numCubes = mapSize / cubeSize;
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Map size is {}, cube size is {}, {} cubes", mapSize, cubeSize, numCubes);
  // std::vector<Cube> cubes{size_t(numCubes * numCubes)};
  // int counter = 0;
  // for (auto &c : cubes) {
  //   int colum = counter % numCubes;
  //   int line = counter / numCubes;
  //   c.topLeftCubePos = {line, colum};
  //   c.topLeftMapPos = {1 + line * cubeSize, 1 + colum * cubeSize};
  //   BOOST_LOG_TRIVIAL(debug) << fmt::format("Cube {} at {},{} and {},{}", counter, c.topLeftCubePos.first,
  //                                           c.topLeftCubePos.second, c.topLeftMapPos.first,
  //                                           c.topLeftMapPos.second);
  //   c.size = cubeSize;
  //   counter++;
  // }

  lineCounter = 0;
  for (const auto &x : data) {
    if (x.size() == 0) {
      break;
    } else {
      uint i = 0;
      while (x[i] == ' ') {
        ++i;
      }
      while (i + cubeSize <= x.size()) {
        int column = (i + 1) / cubeSize;
        int line = lineCounter / cubeSize;

        BOOST_LOG_TRIVIAL(trace) << fmt::format("Line {} extract from {} to {} (cube {},{})", lineCounter, i,
                                                i + cubeSize, line, column);
        std::string tmp = x.substr(i, cubeSize);
        Point currentMapPos = {line, column};
        auto it = std::find_if(cubes.begin(), cubes.end(),
                               [currentMapPos](const auto &cube) { return cube.topLeftCubePos == currentMapPos; });
        if (it == cubes.end()) {
          Cube c;
          c.size = cubeSize;
          c.topLeftCubePos = {line, column};
          c.topLeftMapPos = {1 + line * cubeSize, 1 + column * cubeSize};
          BOOST_LOG_TRIVIAL(trace) << fmt::format("Creating cube at {},{} and {},{}", c.topLeftCubePos.first,
                                                  c.topLeftCubePos.second, c.topLeftMapPos.first,
                                                  c.topLeftMapPos.second);
          c.map.push_back(tmp);
          cubes.push_back(c);
        } else {
          BOOST_LOG_TRIVIAL(trace) << fmt::format("Adding line to cube at {},{}", it->topLeftCubePos.first,
                                                  it->topLeftCubePos.second);
          it->map.push_back(tmp);
        }
        i += cubeSize;
      }
      lineCounter++;
    }
  }

  return commandList;
}

int part1Day22(std::string inputCommands, std::vector<Cube> &cubes) {
  NextPoint tmp{.point = {0, 0}, .direction = '>'};
  tmp.cube = &cubes.front();

  BOOST_LOG_TRIVIAL(debug) << fmt::format("First position = {},{},{} inside cube {},{}", tmp.point.first,
                                          tmp.point.second, tmp.direction, tmp.cube->topLeftCubePos.first,
                                          tmp.cube->topLeftCubePos.second);

  boost::char_separator<char> sep("", "LR"); // specify only the kept separators
  boost::tokenizer<boost::char_separator<char>> tokens(inputCommands, sep);
  for (std::string t : tokens) {
    if (t == "R") {
      tmp.direction = DIRECTION_R[tmp.direction];
    } else if (t == "L") {
      tmp.direction = DIRECTION_L[tmp.direction];
    } else {
      int steps = stoi(t);
      bool keepMoving = true;
      for (int s = 0; s < steps && keepMoving; s++) {
        NextPoint next = tmp.cube->getNextPart1(tmp);
        BOOST_LOG_TRIVIAL(debug) << fmt::format("Potential next cube = {},{},{} inside cube {},{}", next.point.first,
                                                next.point.second, next.direction, next.cube->topLeftCubePos.first,
                                                next.cube->topLeftCubePos.second);
        keepMoving = next.cube->getVal(next.point);
        // next.cube->print();
        if (keepMoving) {
          BOOST_LOG_TRIVIAL(debug) << fmt::format("Keep moving");
          tmp = next;
        }
      }
    }
    BOOST_LOG_TRIVIAL(debug) << fmt::format("After move {}, position = {},{},{} inside cube {},{}", t, tmp.point.first,
                                            tmp.point.second, tmp.direction, tmp.cube->topLeftCubePos.first,
                                            tmp.cube->topLeftCubePos.second);
  }
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Final position = {},{},{} inside cube {},{}", tmp.point.first,
                                          tmp.point.second, tmp.direction, tmp.cube->topLeftCubePos.first,
                                          tmp.cube->topLeftCubePos.second);

  Point final = tmp.point + tmp.cube->topLeftMapPos;
  BOOST_LOG_TRIVIAL(debug) << fmt::format("cube is at {},{} so final pos is {},{}", tmp.cube->topLeftMapPos.first,
                                          tmp.cube->topLeftMapPos.second, final.first, final.second);
  // The final password is the sum of 1000 times the row, 4 times the column, and the facing.
  return 1000 * final.first + 4 * final.second + DIRECTION_SCORE[tmp.direction];
}

void day22Run(bool test) {
  std::string fileName = fmt::format("../inputs/day22{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  std::vector<Cube> cubes;
  std::string inputCommands = parseDay22(data, cubes);
  std::vector<Cube> cubes2 = cubes;
  for (auto &cube : cubes) {
    cube.computeAdjacentCubesPart1(cubes, 4);
  }
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {} cubes", cubes.size());
  {
    // for (const auto &cube : cubes) {
    //   cube.printAdjacentCubes();
    // }
    auto result = part1Day22(inputCommands, cubes);
    BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", result);
  }
  {
    if (test) {
      cubes2[0].adjacentCubes['>'] = {&cubes2[5], '<'};
      cubes2[0].adjacentCubes['^'] = {&cubes2[1], 'v'};
      cubes2[0].adjacentCubes['v'] = {&cubes2[3], 'v'};
      cubes2[0].adjacentCubes['<'] = {&cubes2[2], 'v'};

      cubes2[1].adjacentCubes['>'] = {&cubes2[2], '>'};
      cubes2[1].adjacentCubes['^'] = {&cubes2[0], 'v'};
      cubes2[1].adjacentCubes['v'] = {&cubes2[4], '^'};
      cubes2[1].adjacentCubes['<'] = {&cubes2[5], '^'};

      cubes2[2].adjacentCubes['>'] = {&cubes2[3], '>'};
      cubes2[2].adjacentCubes['^'] = {&cubes2[0], '>'};
      cubes2[2].adjacentCubes['v'] = {&cubes2[4], '>'};
      cubes2[2].adjacentCubes['<'] = {&cubes2[1], '<'};

      cubes2[3].adjacentCubes['>'] = {&cubes2[5], 'v'};
      cubes2[3].adjacentCubes['^'] = {&cubes2[0], '^'};
      cubes2[3].adjacentCubes['v'] = {&cubes2[4], 'v'};
      cubes2[3].adjacentCubes['<'] = {&cubes2[2], '<'};

      cubes2[4].adjacentCubes['>'] = {&cubes2[5], '>'};
      cubes2[4].adjacentCubes['^'] = {&cubes2[3], '^'};
      cubes2[4].adjacentCubes['v'] = {&cubes2[1], '^'};
      cubes2[4].adjacentCubes['<'] = {&cubes2[2], '^'};

      cubes2[5].adjacentCubes['>'] = {&cubes2[0], '<'};
      cubes2[5].adjacentCubes['^'] = {&cubes2[3], '<'};
      cubes2[5].adjacentCubes['v'] = {&cubes2[1], '>'};
      cubes2[5].adjacentCubes['<'] = {&cubes2[4], '<'};
    } else {
      cubes2[0].adjacentCubes['>'] = {&cubes2[1], '>'};
      cubes2[0].adjacentCubes['^'] = {&cubes2[5], '>'};
      cubes2[0].adjacentCubes['v'] = {&cubes2[2], 'v'};
      cubes2[0].adjacentCubes['<'] = {&cubes2[3], '>'};

      cubes2[1].adjacentCubes['>'] = {&cubes2[4], '<'};
      cubes2[1].adjacentCubes['^'] = {&cubes2[5], '^'};
      cubes2[1].adjacentCubes['v'] = {&cubes2[2], '<'};
      cubes2[1].adjacentCubes['<'] = {&cubes2[0], '<'};

      cubes2[2].adjacentCubes['>'] = {&cubes2[1], '^'};
      cubes2[2].adjacentCubes['^'] = {&cubes2[0], '^'};
      cubes2[2].adjacentCubes['v'] = {&cubes2[4], 'v'};
      cubes2[2].adjacentCubes['<'] = {&cubes2[3], 'v'};

      cubes2[3].adjacentCubes['>'] = {&cubes2[4], '>'};
      cubes2[3].adjacentCubes['^'] = {&cubes2[2], '>'};
      cubes2[3].adjacentCubes['v'] = {&cubes2[5], 'v'};
      cubes2[3].adjacentCubes['<'] = {&cubes2[0], '>'};

      cubes2[4].adjacentCubes['>'] = {&cubes2[1], '<'};
      cubes2[4].adjacentCubes['^'] = {&cubes2[2], '^'};
      cubes2[4].adjacentCubes['v'] = {&cubes2[5], '<'};
      cubes2[4].adjacentCubes['<'] = {&cubes2[3], '<'};

      cubes2[5].adjacentCubes['>'] = {&cubes2[4], '^'};
      cubes2[5].adjacentCubes['^'] = {&cubes2[3], '^'};
      cubes2[5].adjacentCubes['v'] = {&cubes2[1], 'v'};
      cubes2[5].adjacentCubes['<'] = {&cubes2[0], 'v'};
    }
    // for (const auto &cube : cubes2) {
    //   cube.printAdjacentCubes();
    // }
    auto result = part1Day22(inputCommands, cubes2);
    BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", result);
    // 122204 too high
    // 45407 too low
  }
}