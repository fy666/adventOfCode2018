#include "days.hpp"
#include <fmt/format.h>
#include <iostream>
#include <list>
#include <numeric>
#include <vector>

void moveIndexes(std::vector<int> &positions, int startingIndex, int insertedIndex) {
  int N = positions.size();
  int low = std::min(startingIndex, insertedIndex);
  int high = std::max(startingIndex, insertedIndex);
  int toAdd = -1;
  if (startingIndex > insertedIndex) {
    toAdd = 1;
  }
  for (uint x = 0; x < positions.size(); ++x) {
    if (positions[x] <= high && positions[x] >= low) {
      positions[x] = (positions[x] + toAdd); //% N;
    }
  }
}

std::string printCurrent(const std::vector<int> &positions, const std::vector<int64_t> &data) {
  std::vector<std::string> result;
  for (uint x = 0; x < positions.size(); ++x) {
    int index = std::find(positions.begin(), positions.end(), x) - positions.begin();
    result.push_back(fmt::format("{}", data[index]));
  }
  return fmt::format("{}", fmt::join(result, ","));
}

void mix(const std::vector<int64_t> &data, std::vector<int> &position) {
  int64_t N = data.size() - 1;
  int index = 0;
  int indexZero = 0;
  BOOST_LOG_TRIVIAL(trace) << fmt::format("{}", printCurrent(position, data));

  for (const auto &x : data) {
    if (x == 0) {
      index++;
      continue;
    }
    int startIndex = position[index];

    int64_t newPosition = (int64_t)startIndex + x;
    if (newPosition == 0) {
      newPosition = N;
    } else {
      newPosition = (N + (newPosition % N)) % N;
    }
    if (newPosition == 0) {
      newPosition = N;
    }
    BOOST_LOG_TRIVIAL(trace) << fmt::format("Processing {} : going from {} to {}", x, startIndex, newPosition);
    BOOST_LOG_TRIVIAL(trace) << fmt::format("Indexes before move = {}", fmt::join(position, ","));
    moveIndexes(position, startIndex, newPosition);
    position[index] = newPosition;
    BOOST_LOG_TRIVIAL(trace) << fmt::format("Indexes after move = {}", fmt::join(position, ","));
    BOOST_LOG_TRIVIAL(trace) << fmt::format("{}", printCurrent(position, data));
    index++;
  }
}

void part1(const std::vector<int32_t> &data) {
  std::vector<int64_t> input;
  for (const auto &x : data) {
    input.push_back(x);
  }
  std::vector<int> position(data.size());
  std::iota(position.begin(), position.end(), 0);

  mix(input, position);
  int N = data.size();

  int posZero = std::find(position.begin(), position.end(), 0) - position.begin();
  posZero = position[std::find(data.begin(), data.end(), 0) - data.begin()];
  int result = 0;
  std::vector<int> wantedPos{1000, 2000, 3000};
  for (const auto &x : wantedPos) {
    int a = data[std::find(position.begin(), position.end(), (posZero + x) % N) - position.begin()];
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Value at pos {} = {}", x, a);
    result += a;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", result);
}

void part2(const std::vector<int> &data) {
  int64_t key = 811589153LL;
  std::vector<int64_t> input;
  for (const auto &x : data) {
    input.push_back(x * key);
  }

  std::vector<int> position(data.size());
  std::iota(position.begin(), position.end(), 0);

  for (int round = 0; round < 10; ++round) {
    mix(input, position);
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Round {}: {}", round + 1, printCurrent(position, input));
  }
  int N = data.size();

  int posZero = position[std::find(data.begin(), data.end(), 0) - data.begin()];
  int64_t result = 0;
  std::vector<int> wantedPos{1000, 2000, 3000};
  for (const auto &x : wantedPos) {
    int64_t a = input[std::find(position.begin(), position.end(), (posZero + x) % N) - position.begin()];
    BOOST_LOG_TRIVIAL(info) << fmt::format("Value at pos {} = {}", x, a);
    result += a;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", result);
}

void day20Run(bool test) {
  std::string fileName = fmt::format("../inputs/day20{}.txt", test ? "_test" : "");
  auto data = read_file<int>(fileName, my_own_stoi);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  part1(data);
  part2(data);
}