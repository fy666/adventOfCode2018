#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

struct PointXY {
  int x = 0;
  int y = 0;
};

struct Move {
  int direction[2] = {0, 0};
  int steps = 0;
};

Move day9parser(const std::string x) {
  const boost::regex expr("([RLUD]) (\\d*)");
  boost::smatch what;
  Move move{0};
  if (boost::regex_search(x, what, expr)) {
    if (what[1] == "R") {
      move.direction[0] = 1;
    } else if (what[1] == "U") {
      move.direction[1] = -1;
    } else if (what[1] == "D") {
      move.direction[1] = 1;
    } else if (what[1] == "L") {
      move.direction[0] = -1;
    }
    move.steps = stoi(what[2]);
  } else {
    BOOST_LOG_TRIVIAL(error) << fmt::format("Could not parse {}", x);
  }
  return move;
}

void moveTail(PointXY &head, PointXY &tail) {
  int dx = head.x - tail.x;
  int dy = head.y - tail.y;
  /* Nothing to do */
  if (abs(dx) <= 1 && abs(dy) <= 1) {
    return;
  }
  if (dx != 0) {
    tail.x += dx / abs(dx);
  }
  if (dy != 0) {
    tail.y += dy / abs(dy);
  }
}

void moveHead(PointXY &head, std::vector<PointXY> &tails, const Move &move, std::set<std::pair<int, int>> &positions) {
  for (uint s = 1; s <= move.steps; ++s) {
    head.x += move.direction[0];
    head.y += move.direction[1];
    moveTail(head, tails[0]);
    for (uint i = 1; i < tails.size(); i++) {
      moveTail(tails[i - 1], tails[i]);
    }
    positions.insert({tails.back().x, tails.back().y});
  }
}

int part1(const std::vector<Move> &moves, const std::size_t numberOfTails) {
  std::set<std::pair<int, int>> positions;
  PointXY head{0, 0};
  std::vector<PointXY> tails{numberOfTails};
  for (const auto &move : moves) {
    moveHead(head, tails, move, positions);
  }

  return positions.size();
}

void day9Run(bool test) {
  std::string fileName = fmt::format("../inputs/day9{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  std::vector<Move> moves;
  moves.reserve(data.size());
  for (const auto &x : data) {
    moves.push_back(day9parser(x));
  }
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", moves.size());
  BOOST_LOG_TRIVIAL(debug) << fmt::format("[{} {}] {}", moves[0].direction[0], moves[0].direction[1], moves[0].steps);

  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", part1(moves, 1));
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", part1(moves, 9));
}
