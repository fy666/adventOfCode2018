#include "days.hpp"
#include <iostream>
#include <map>
#include <stack>
#include <vector>

struct Beacon {
  int x;
  int y;
  int d;
  int sensorX;
  int sensorY;
};

static std::vector<Beacon> parse(const std::vector<std::string> &data) {
  const boost::regex expr("Sensor at x=(-?\\d*), y=(-?\\d*): closest beacon is at x=(-?\\d*), y=(-?\\d*)");
  std::vector<Beacon> beacons;
  for (const auto &x : data) {
    boost::smatch what;
    if (boost::regex_search(x, what, expr)) {
      int sensorPosX = stoi(what[1]);
      int sensorPosY = stoi(what[2]);
      int beaconPosX = stoi(what[3]);
      int beaconPosY = stoi(what[4]);
      int manathand = abs(sensorPosX - beaconPosX) + abs(sensorPosY - beaconPosY);
      beacons.push_back(Beacon{sensorPosX, sensorPosY, manathand, beaconPosX, beaconPosY});
    }
  }
  return beacons;
}

std::vector<std::pair<int, int>> mergeIntervals(std::vector<std::pair<int, int>> &intervals) {
  if (intervals.size() <= 0)
    return {};

  std::vector<std::pair<int, int>> result;

  // sort the intervals in increasing order of start time
  sort(intervals.begin(), intervals.end());
  result.push_back(intervals[0]);

  // Start from the next interval and merge if necessary
  int resultIndex = 0;
  for (int i = 1; i < intervals.size(); i++) {
    if (result[resultIndex].second < intervals[i].first) {
      result.push_back(intervals[i]);
      resultIndex += 1;
    } else if (result[resultIndex].second < intervals[i].second) {
      result[resultIndex].second = intervals[i].second;
    }
  }
  return result;
}

std::vector<std::pair<int, int>> part1(const std::vector<Beacon> &beacons, int yValue) {
  int beaconsAndSensorToRemove = 0;
  std::vector<std::pair<int, int>> intervals;
  for (const auto &beacon : beacons) {
    int dy = abs(yValue - beacon.y);
    int dxMax = beacon.d - dy;
    if (abs(dy) <= beacon.d) {
      intervals.push_back({beacon.x - dxMax, beacon.x + dxMax});
    }
    if (beacon.y == yValue) {
      beaconsAndSensorToRemove += 1;
    }
    if (beacon.sensorY == yValue) {
      beaconsAndSensorToRemove += 1;
    }
  }

  return mergeIntervals(intervals);
}

uint64_t part2(const std::vector<Beacon> &beacons, int gridSize) {
  for (int y = 0; y < gridSize; y++) {
    auto mergedIntervals = part1(beacons, y);
    if (mergedIntervals.size() > 1) {
      int x = mergedIntervals[1].first - 1;
      return uint64_t(x) * 4000000ULL + uint64_t(y);
    }
  }
  return 0;
}

void day15Run(bool test) {
  std::string fileName = fmt::format("../inputs/day15{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  int value;
  int valuePart2;
  if (test) {
    value = 10;
    valuePart2 = 20;
  } else {
    value = 2000000;
    valuePart2 = 4000000;
  }

  auto beacons = parse(data);
  auto result = part1(beacons, value);
  /* Add all intervals */
  int size = 0;
  for (const auto &i : result) {
    size += i.second - i.first;
  }
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", size);
  uint64_t result2 = part2(beacons, valuePart2);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", result2);
}