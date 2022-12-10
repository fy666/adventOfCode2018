#include "days.hpp"
#include <iostream>
#include <map>
#include <vector>

static int run(const std::vector<std::string> &commands) {
  const boost::regex expr("addx (-*\\d*)");
  std::vector<int> cycles{20, 60, 100, 140, 180, 220};
  int signalStrenght = 0;
  int cycleNum = 1;
  int registerValue = 1;
  char CRT[240];

  auto endOfCycle = [&CRT, &cycleNum, &cycles, &signalStrenght, &registerValue]() {
    if (std::find(cycles.begin(), cycles.end(), cycleNum) != cycles.end()) {
      BOOST_LOG_TRIVIAL(debug) << fmt::format("Instruction {}, reg value of {}", cycleNum, registerValue);
      signalStrenght += registerValue * cycleNum;
    }
    if (abs((cycleNum - 1) % 40 - registerValue) < 2) {
      CRT[cycleNum - 1] = '#';
    } else {
      CRT[cycleNum - 1] = '.';
    }
    cycleNum += 1;
    return;
  };

  for (const auto &command : commands) {
    endOfCycle();
    if (command != "noop") {
      endOfCycle();
      int numberToAdd = stoi(std::string(command.substr(5, command.size())));
      registerValue += numberToAdd;
    }
  }

  /* Draw CRT */
  for (uint i = 0; i < 240; ++i) {
    if ((i % 40) == 0) {
      std::cout << std::endl;
    }
    std::cout << CRT[i];
  }
  std::cout << std::endl;
  return signalStrenght;
}

void day10Run(bool test) {
  std::string fileName = fmt::format("../inputs/day10{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part1 = {}", run(data));
}