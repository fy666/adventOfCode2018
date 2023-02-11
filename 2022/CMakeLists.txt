# Set the project name
cmake_minimum_required(VERSION 3.16)
project (advent_of_code_2022)

set(Boost_USE_STATIC_LIBS OFF) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF)

set(CMAKE_CXX_COMPILER /usr/bin/g++-10 CACHE PATH "" FORCE)


find_package(Boost 1.71.0 COMPONENTS regex log program_options)
# Create a sources variable with a link to all cpp files to compile


file(GLOB all_SRCS
        "${PROJECT_SOURCE_DIR}/*.cpp"
        )

set(SOURCES
    main.cpp
    utils.cpp
    day1.cpp
    day2.cpp
)

set(CMAKE_CXX_FLAGS "-O3")
set(CMAKE_BUILD_TYPE Debug)
MESSAGE(${Boost_LIBRARIES})
# Add an executable with the above sources
add_executable(main ${all_SRCS})
target_link_libraries(main fmt ${Boost_LIBRARIES} boost_log_setup)
target_compile_features(main PRIVATE cxx_std_17)
# target_compile_features(main PRIVATE cxx_std_20) # Doesnt work with boost 1.70 https://stackoverflow.com/questions/62723053/boost-log-expressions-v1-71-will-not-compile-under-c20
