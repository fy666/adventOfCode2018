#include "days.hpp"
#include <cstdint>
#include <iostream>
#include <map>
#include <memory>
#include <vector>

class file {
public:
  std::string name;
  int size = 0;
  std::shared_ptr<file> parent = nullptr;
  std::vector<std::shared_ptr<file>> childs = {};
  file(std::string x) : name(x) {}
  file(std::string x, int size_t) : name(x), size(size_t) {}
};

int64_t part1Answer = 0;
int64_t part2Answer = 70000000;

int getDirSize(std::shared_ptr<file> root) {
  if (root->childs.size() == 0) {
    return root->size;
  }
  int size = 0;
  for (const auto &child : root->childs) {
    size += getDirSize(child);
  }
  root->size = size;
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Dir {} has size {}", root->name, root->size);
  if (root->size < 100000) {
    part1Answer += root->size;
  }
  return size;
}

void runThrough(std::shared_ptr<file> root, int64_t sizeToFree) {
  if (root->childs.size() == 0) {
    return;
  }
  for (const auto &child : root->childs) {
    runThrough(child, sizeToFree);
  }
  if (root->size >= sizeToFree) {
    if (root->size < part2Answer) {
      part2Answer = root->size;
    }
  }
  return;
}

std::shared_ptr<file> run(const std::vector<std::string> &data) {
  const boost::regex exprCd("\\$ cd (.*)");
  const boost::regex exprData("^(\\d*) (.*)");
  const boost::regex exprDir("^dir (\\w*)");
  std::shared_ptr<file> root = std::make_shared<file>("/");
  std::shared_ptr<file> current = root;

  for (const auto &line : data) {
    BOOST_LOG_TRIVIAL(debug) << fmt::format("Reading line : {}", line);
    if (line == "$ ls") {
      BOOST_LOG_TRIVIAL(debug) << "ls";
    } else if (line == "$ cd ..") {
      current = current->parent;
      BOOST_LOG_TRIVIAL(debug) << "Back one level above";
    } else if (line == "$ cd /") {
      current = root;
      BOOST_LOG_TRIVIAL(debug) << "Back to root";
    } else {
      boost::smatch what;
      if (boost::regex_search(line, what, exprCd)) {
        std::string dirName = what[1];
        bool found = false;
        for (const auto &child : current->childs) {
          if (child->name == dirName) {
            found = true;
            current = child;
            break;
          }
        }
        BOOST_LOG_TRIVIAL(debug) << fmt::format("cd to {}, found ? {}", dirName, found);

        if (found == false) {
          BOOST_LOG_TRIVIAL(error) << "child not found !!! ";
          exit(1);
        }
      } else if (boost::regex_search(line, what, exprData)) {
        // add new file
        int size = stoi(what[1]);
        std::string name = what[2];
        std::shared_ptr<file> newNode = std::make_shared<file>(name, size);
        newNode->parent = current;
        current->childs.push_back(newNode);
        BOOST_LOG_TRIVIAL(debug) << fmt::format("Adding new file {}, size= {}", name, size);

      } else if (boost::regex_search(line, what, exprDir)) {
        // create new dir
        std::string name = what[1];
        std::shared_ptr<file> newNode = std::make_shared<file>(name);
        newNode->parent = current;
        current->childs.push_back(newNode);
        BOOST_LOG_TRIVIAL(debug) << fmt::format("Adding new dir {}", name);
      }
    }
  }
  return root;
}

void day7Run(bool test) {
  std::string fileName = fmt::format("../inputs/day7{}.txt", test ? "_test" : "");
  auto data = read_file<std::string>(fileName, my_string);
  BOOST_LOG_TRIVIAL(debug) << fmt::format("Read {} lines", data.size());
  auto directoryTree = run(data);
  int totalSize = getDirSize(directoryTree);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Dir tree of size {}", totalSize);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 1 answer =  {}", part1Answer);
  int sizeLeft = 70000000 - directoryTree->size;
  int sizeToFree = 30000000 - sizeLeft;
  part2Answer = 70000000;
  runThrough(directoryTree, sizeToFree);
  BOOST_LOG_TRIVIAL(info) << fmt::format("Part 2 answer =  {}", part2Answer);
}