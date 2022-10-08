#include "utils.hpp"
#include <fstream>
#include <iostream>


template<typename T>
std::vector<T> read_file(std::string filename, std::function<T(const std::string)> func) {
  std::vector<T> result;
  std::ifstream myfile;
  myfile.open(filename);
  std::string myline;
  if (myfile.is_open()) {
    while (myfile) {
      std::getline(myfile, myline);
      result.push_back(func(myline));
    }
  }
  return result;
}


template std::vector<std::string> read_file<std::string>(std::string filename,std::function<std::string(const std::string)> func);
template std::vector<float> read_file<std::string>(std::string filename,std::function<float(const std::string)> func);


// void test() {
//   std::cout << "Main in utils.cpp" << std::endl;
//   auto result = read_file("lol");
//   for (const auto &r : result) {
//     std::cout << r << std::endl;
//   }
// }