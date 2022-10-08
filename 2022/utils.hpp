#pragma once
#include <string>
#include <vector>
#include <functional>

template<typename T>
extern std::vector<T> read_file(std::string filename,std::function<T(std::string)> func);