#pragma once
#include <functional>
#include <string>
#include <vector>

template <typename T> extern std::vector<T> read_file(std::string filename, std::function<T(std::string)> func);