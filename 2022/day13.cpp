#include "days.hpp"
#include <boost/algorithm/string.hpp>
#include <iostream>
#include <map>
#include <vector>

enum Comparison { smaller, greater, equal };

bool isList(std::string x) {
  return (std::count(x.begin(), x.end(), '[') == 1 && std::count(x.begin(), x.end(), ']') == 1);
}

std::vector<int> getList(std::string x) {
  std::vector<int> result;
  if (x == "[]") {
    return result;
  }
  replace(x.begin(), x.end(), '[', ' ');
  replace(x.begin(), x.end(), ']', ' ');

  std::vector<std::string> tmpResults;
  boost::split(tmpResults, x, boost::is_any_of(","));
  for (const auto &i : tmpResults) {
    result.push_back(stoi(i));
  }
  return result;
}

Comparison compareList(const std::vector<int> &left, const std::vector<int> &right) {
  for (uint i = 0; i < std::min(left.size(), right.size()); ++i) {
    if (left[i] < right[i]) {
      return smaller;
    } else if (left[i] > right[i]) {
      return greater;
    }
  }
  if (left.size() < right.size()) {
    return smaller;
  } else if (left.size() > right.size()) {
    return greater;
  }
  return equal;
}

std::pair<std::string, std::string> getNextElement(std::string x) {
  int numBrackets = 0;
  int cutPosition = x.size();
  for (uint i = 0; i < x.size(); ++i) {
    if (x[i] == '[') {
      numBrackets += 1;
    } else if (x[i] == ']') {
      numBrackets -= 1;
    }
    if (x[i] == ',' && numBrackets == 1) {
      cutPosition = i;
      break;
    }
  }
  return {x.substr(1, cutPosition - 1), x.substr(cutPosition + 1, x.size() - cutPosition - 2)};
}

Comparison correctOrderPacket(const std::string &left, const std::string &right) {
  std::cout << "Treating left packet = " << left << " right packet = " << right << std::endl;
  if (isList(left) && isList(right)) {
    auto res1 = getList(left);
    auto res2 = getList(right);
    return (compareList(res1, res2));
    // std::cout << "list comparison = " << x << std::endl;
  } else {
    if (isList(left)) {
      auto splittedRight = getNextElement(right);
      auto res = correctOrderPacket(left, splittedRight.first);
      if (res == equal) {
        res = correctOrderPacket(left, splittedRight.second);
      }
    }
    if (isList(right)) {
      auto splittedLeft = getNextElement(left);
      auto res = correctOrderPacket(splittedLeft.first, right);
      if (res == equal) {
        res = correctOrderPacket(splittedLeft.first, right);
      }
    }
    auto res = getNextElement(left);
    std::cout << "Splitting in " << res.first << " and " << res.second << std::endl;
  }

  return equal;
}

void day13Run(bool test) {
  std::string fileName = fmt::format("../inputs/day13{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);

  std::vector<std::pair<std::string, std::string>> packets;
  for (uint i = 0; i < data.size() - 1; i = i + 3) {
    packets.push_back({data[i], data[i + 1]});
  }
  for (const auto &packet : packets) {
    correctOrderPacket(packet.first, packet.second);
  }
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} packets", packets.size());
}