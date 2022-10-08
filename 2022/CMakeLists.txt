# Set the project name
project (advent_of_code_2022)

# Create a sources variable with a link to all cpp files to compile
set(SOURCES
    main.cpp
    utils.cpp
)

# Add an executable with the above sources
add_executable(main ${SOURCES})
target_link_libraries(main fmt)