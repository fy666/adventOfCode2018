#include "days.hpp"
#include <algorithm>
#include <iostream>
#include <map>
#include <vector>

struct PointXY {
  int x = 0;
  int y = 0;
};

struct Move {
  PointXY direction = {0};
  int steps = 0;
};

static PointXY operator+(const PointXY &a, const PointXY &b) {
  PointXY res;
  return {a.x + b.x, a.y + b.y};
}

static PointXY operator-(const PointXY &a, const PointXY &b) {
  PointXY res;
  return {a.x - b.x, a.y - b.y};
}

PointXY &operator+=(PointXY &a, const PointXY &b) {
  a.x += b.x;
  a.y += b.y;
  return a;
}

Move day9parser(const std::string x) {
  const boost::regex expr("([RLUD]) (\\d*)");
  boost::smatch what;
  Move move{0};
  if (boost::regex_search(x, what, expr)) {
    if (what[1] == "R") {
      move.direction.x = 1;
    } else if (what[1] == "U") {
      move.direction.y = -1;
    } else if (what[1] == "D") {
      move.direction.y = 1;
    } else if (what[1] == "L") {
      move.direction.x = -1;
    }
    move.steps = stoi(what[2]);
  } else {
    BOOST_LOG_TRIVIAL(error) << fmt::format("Could not parse {}", x);
  }
  return move;
}

void moveTail(PointXY &head, PointXY &tail) {
  auto d = head - tail;

  /* Nothing to do */
  if (abs(d.x) <= 1 && abs(d.y) <= 1) {
    return;
  }
  if (d.x != 0) {
    tail.x += d.x / abs(d.x);
  }
  if (d.y != 0) {
    tail.y += d.y / abs(d.y);
  }
}

void moveHead(PointXY &head, std::vector<PointXY> &tails, const Move &move, std::set<std::pair<int, int>> &positions) {
  for (uint s = 1; s <= move.steps; ++s) {
    head += move.direction;
    moveTail(head, tails[0]);
    for (uint i = 1; i < tails.size(); ++i) {
      moveTail(tails[i - 1], tails[i]);
    }
    positions.insert({tails.back().x, tails.back().y});
  }
}

int day9(const std::vector<Move> &moves, const std::size_t numberOfTails) {
  std::set<std::pair<int, int>> positions;
  PointXY head{0, 0};
  std::vector<PointXY> tails{numberOfTails};
  // for (const auto &move : moves) {
  //   moveHead(head, tails, move, positions);
  // }
  std::for_each(moves.cbegin(), moves.cend(), [&head, &tails, &positions](auto &move) {
    moveHead(head, tails, move, positions);
    return;
  });

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
  BOOST_LOG_TRIVIAL(debug) << fmt::format("[{} {}] {}", moves[0].direction.x, moves[0].direction.y, moves[0].steps);

  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", day9(moves, 1));
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", day9(moves, 9));
}
