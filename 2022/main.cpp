#include "days.hpp"
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/log/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/sources/record_ostream.hpp>
#include <boost/log/sources/severity_logger.hpp>
#include <boost/log/support/date_time.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>
#include <boost/log/utility/setup/console.hpp>
#include <boost/program_options.hpp>
#include <chrono>
#include <fmt/core.h>
#include <functional>
#include <vector>

namespace logging = boost::log;
namespace expr = boost::log::expressions;

void init(bool debug) {
  boost::log::add_console_log(
      std::cout, boost::log::keywords::format =
                     expr::stream << "["
                                  << expr::format_date_time<boost::posix_time::ptime>("TimeStamp", "%Y-%m-%d %H:%M:%S")
                                  << "]"
                                  << " [" << logging::trivial::severity << "] " << expr::smessage);
  logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::info);
  if (debug) {
    logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
  }
}

int main(int ac, char **av) {
  boost::program_options::options_description desc("Allowed options");
  desc.add_options()("help", "produce help message");
  desc.add_options()("day", boost::program_options::value<int>()->default_value(10),
                     "set day")("debug", "logger in debug")("test", "Run test input");

  boost::program_options::variables_map vm;
  boost::program_options::store(boost::program_options::parse_command_line(ac, av, desc), vm);
  boost::program_options::notify(vm);

  if (vm.count("help")) {
    std::cout << desc << "\n";
    return 0;
  }
  int day = vm.at("day").as<int>();
  bool debug = vm.count("debug");
  bool test = vm.count("test");

  logging::add_common_attributes();
  init(debug);

  BOOST_LOG_TRIVIAL(info) << fmt::format("*** Doing day {} {}***", day, test ? "test input" : "");
  std::vector<std::function<void(bool)>> days;
  days.push_back(day1Run);
  days.push_back(day2Run);
  days.push_back(day3Run);
  days.push_back(day4Run);
  days.push_back(day5Run);
  days.push_back(day6Run);
  days.push_back(day7Run);
  days.push_back(day8Run);
  days.push_back(day9Run);
  days.push_back(day10Run);
  days.push_back(day11Run);
  days.push_back(day12Run);
  days.push_back(day13Run);
  days.push_back(day14Run);
  days.push_back(day15Run);
  days.push_back(day16Run);
  days.push_back(day17Run);
  days.push_back(day18Run);
  days.push_back(day19Run);
  days.push_back(day20Run);
  days.push_back(day21Run);
  days.push_back(day22Run);
  days.push_back(day23Run);
  days.push_back(day24Run);
  days.push_back(day25Run);

  auto start = std::chrono::high_resolution_clock::now();

  days[(day - 1)](test);
  auto stop = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
  BOOST_LOG_TRIVIAL(info) << fmt::format(">> Day {} run in {:.3} ms", day, float(duration.count() / 1000.f));

  return 1;
}