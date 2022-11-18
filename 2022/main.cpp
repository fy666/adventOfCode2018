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
#include <fmt/core.h>
#include <functional>
#include <vector>

namespace logging = boost::log;
namespace expr = boost::log::expressions;
std::vector<int> get_data() { return std::vector<int>{1, 2, 3, 4, 5}; }

/* TODO:
-Argparse

*/

void init() {
  boost::log::add_console_log(std::cout, boost::log::keywords::format =
                                             expr::stream << "[" << expr::format_date_time<boost::posix_time::ptime>("TimeStamp", "%Y-%m-%d %H:%M:%S") << "]"
                                                          << " [" << logging::trivial::severity << "] " << expr::smessage);
  logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::info);
  logging::core::get()->set_filter(logging::trivial::severity >= logging::trivial::debug);
}

int main() {
  logging::add_common_attributes();
  init();

  int day = 1;
  std::vector<std::function<void(void)>> days;
  days.push_back(day1Run);
  days.push_back(day2Run);
  days[0]();
  days[1]();
  return 1;
}