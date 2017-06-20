cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)

# SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
# SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
# SET(CMAKE_MACOSX_RPATH TRUE)

include($ENV{HOME}/coriander/share/cocl/cocl.cmake)
include($ENV{HOME}/coriander/lib/coriander_plugins/corianderdnn-targets.cmake)
# find_library(corianderdnn)

cocl_add_executable(basic1 basic1.cu)
target_link_libraries(basic1 corianderdnn)

add_custom_target(run
    COMMAND ./basic1
    DEPENDS basic1)
