#include "days.hpp"
#include <iostream>
#include <map>
// #include <unordered_map>
#include <vector>

typedef std::tuple<int, int, int> Pos3D;

int parseLava(std::set<Pos3D> &lavaMap, const std::vector<std::string> &data) {
  const boost::regex expr("(\\d*),(\\d*),(\\d*)");
  int maxPos = -100;
  for (const auto &x : data) {
    boost::smatch what;
    if (boost::regex_search(x, what, expr)) {
      int x = stoi(what[1]);
      int y = stoi(what[2]);
      int z = stoi(what[3]);
      maxPos = std::max(maxPos, x);
      maxPos = std::max(maxPos, y);
      maxPos = std::max(maxPos, z);
      lavaMap.insert({x, y, z});
    }
  }
  return maxPos;
}

bool isAirTrapped(const std::set<Pos3D> &lavaMap, Pos3D air, int maxPos, std::set<Pos3D> &alreadyVisited) {
  const std::vector<Pos3D> directions{{1, 0, 0}, {0, 0, 1}, {0, 1, 0}, {-1, 0, 0}, {0, 0, -1}, {0, -1, 0}};
  if (std::get<0>(air) > maxPos || std::get<0>(air) < 0 || std::get<1>(air) > maxPos || std::get<1>(air) < 0 ||
      std::get<2>(air) > maxPos || std::get<2>(air) < 0) {
    return false;
  }
  bool result = true;
  alreadyVisited.insert(air);
  for (const auto &dir : directions) {
    Pos3D sideCube = {std::get<0>(air) + std::get<0>(dir), std::get<1>(air) + std::get<1>(dir),
                      std::get<2>(air) + std::get<2>(dir)};
    if (alreadyVisited.find(sideCube) == alreadyVisited.end() && lavaMap.find(sideCube) == lavaMap.end()) {
      result &= isAirTrapped(lavaMap, sideCube, maxPos, alreadyVisited);
    } else {
    }
  }
  return result;
}

std::pair<int, int> countLavaFace(std::set<Pos3D> &lavaMap, int maxPos) {
  std::vector<Pos3D> directions{{1, 0, 0}, {0, 0, 1}, {0, 1, 0}, {-1, 0, 0}, {0, 0, -1}, {0, -1, 0}};
  std::set<Pos3D> airMap;
  std::set<Pos3D> insideAirMap;
  std::set<Pos3D> outsideAirMap;

  int countFaces = 0;

  for (const auto &lava : lavaMap) {
    for (const auto &dir : directions) {
      Pos3D sideCube = {std::get<0>(lava) + std::get<0>(dir), std::get<1>(lava) + std::get<1>(dir),
                        std::get<2>(lava) + std::get<2>(dir)};
      if (lavaMap.find(sideCube) == lavaMap.end()) {
        std::set<Pos3D> tmp;
        if (outsideAirMap.find(sideCube) == outsideAirMap.end() &&
            (insideAirMap.find(sideCube) != insideAirMap.end() || isAirTrapped(lavaMap, sideCube, maxPos, tmp))) {
          airMap.insert(sideCube);
          insideAirMap.insert(tmp.begin(), tmp.end());
        } else {
          outsideAirMap.insert(tmp.begin(), tmp.end());
        }
        countFaces += 1;
      }
    }
  }

  BOOST_LOG_TRIVIAL(debug) << fmt::format("Trapped air = {}", airMap.size());

  int trappedAirInContactWithLava = 0;
  for (const auto &air : airMap) {
    for (const auto &dir : directions) {
      Pos3D sideCube = {std::get<0>(air) + std::get<0>(dir), std::get<1>(air) + std::get<1>(dir),
                        std::get<2>(air) + std::get<2>(dir)};
      if (lavaMap.find(sideCube) != lavaMap.end()) {
        trappedAirInContactWithLava += 1;
      }
    }
  }

  BOOST_LOG_TRIVIAL(debug) << fmt::format("Trapped faces = {}, part 2 = {}", trappedAirInContactWithLava,
                                          countFaces - trappedAirInContactWithLava);

  return {countFaces, countFaces - trappedAirInContactWithLava};
}

void day18Run(bool test) {
  std::string fileName = fmt::format("../inputs/day18{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  std::set<Pos3D> lavaMap;
  auto extrema = parseLava(lavaMap, data);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Found {} lava pos", lavaMap.size());
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Extrema = {}", extrema);

  auto result = countLavaFace(lavaMap, extrema);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 = {}", result.first);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 = {}", result.second);
}