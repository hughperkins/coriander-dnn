cmake_minimum_required(VERSION 4.0.0)

option(BUILD_TESTS OFF)

IF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    if(WIN32)
        SET(CMAKE_INSTALL_PREFIX
            "$ENV{HOME}/coriander" CACHE PATH "Installation prefix, default '${HOME}/coriander'" FORCE
        )
    else()
        SET(CMAKE_INSTALL_PREFIX
            "$ENV{HOME}/coriander" CACHE PATH "Installation prefix, default '${HOME}/coriander'" FORCE
        )
    endif()
ENDIF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)

# bring in just the targets we need/depend on
# (if we bring in all targets, the dnn target has the same name as ourselves, and conflicts)
include($ENV{COCL_CMAKE}/cocl_vars.cmake)
include($ENV{COCL_CMAKE}/cocl_impl.cmake)
include(${COCL_LIB}/cocl/cocl-targets.cmake)
include(${COCL_LIB}/coriander_plugins/corianderclblast-targets.cmake)
# include(${COCL_CMAKE}/coriander_plugins/corianderclblast.cmake)

set(CORIANDER_DIR ${CMAKE_INSTALL_PREFIX})

SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib/coriander_plugins")
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
SET(CMAKE_MACOSX_RPATH TRUE)

if(WIN32)
    set(CMAKE_CXX_FLAGS "/EHsc ${PLATFORM_OPTIONS}")
else()
    set(CMAKE_CXX_FLAGS "-std=c++11 -fPIC -g ${PLATFORM_OPTIONS}")
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath,$ORIGIN")
endif()
add_definitions(-DUSE_CLEW)

add_library(corianderdnn SHARED
    src/cocl_dnn.cpp src/cocl_dnn_act.cpp src/cocl_dnn_conv.cpp
    src/cocl_dnn_gemm.cpp src/cocl_dnn_pooling.cpp)
target_include_directories(corianderdnn PRIVATE "${CORIANDER_DIR}/include")
target_include_directories(corianderdnn PRIVATE "include")
target_include_directories(corianderdnn SYSTEM BEFORE PRIVATE "${CORIANDER_DIR}/include/clew/proxy-headers")
# I kind of want the dnn to be blas-agnostic, ie use any blas, but that's not the case currently
target_include_directories(corianderdnn SYSTEM BEFORE PRIVATE "${CORIANDER_DIR}/include/coriander_plugins/corianderclblast")
target_include_directories(corianderdnn PRIVATE ${CLANG_HOME}/include)
target_link_libraries(corianderdnn cocl clblast easycl clew)

# for testing
set(CORIANDERDNN_INCLUDE ${CMAKE_CURRENT_SOURCE_DIR}/include)
set(GTEST_HOME ${CMAKE_CURRENT_SOURCE_DIR}/third_party/gtest)
add_subdirectory(test)

CONFIGURE_FILE(
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake/corianderdnn.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/cmake/corianderdnn.cmake" @ONLY)
INSTALL(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/cmake/corianderdnn.cmake DESTINATION share/cocl/coriander_plugins)

INSTALL(FILES include/cudnn.h DESTINATION ${CORIANDER_DIR}/include/coriander_plugins/corianderdnn)
FILE(GLOB DNN_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/include/coriander-dnn/*.h)
INSTALL(FILES ${DNN_HEADERS} DESTINATION ${CORIANDER_DIR}/include/coriander_plugins/corianderdnn/coriander-dnn)

install(TARGETS corianderdnn EXPORT corianderdnn-targets
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/coriander_plugins
    ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/coriander_plugins
    RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/coriander_plugins
)
install(EXPORT corianderdnn-targets DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/coriander_plugins)
