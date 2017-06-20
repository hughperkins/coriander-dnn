cmake_minimum_required(VERSION 3.0.0)

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

if(WIN32)
    # set(CORIANDER_DIR "C:\\Program Files\\Coriander" CACHE PATH "Installation directory of Coriander")
    set(CLANG_HOME "C:\\Program Files\\LLVM" CACHE PATH "the downloaded clang-4.0.0 folder, containing lib, bin etc")
else()
    set(CLANG_HOME "/usr/local/opt/llvm-4.0" CACHE PATH "the downloaded clang-4.0.0 folder, containing lib, bin etc")
    # set(CORIANDER_DIR "$ENV{HOME}/coriander" CACHE PATH "Installation directory of Coriander")
endif()

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
foreach(libname cocl clblast easycl clew)
    if(APPLE)
        target_link_libraries(corianderdnn "${CORIANDER_DIR}/lib/lib${libname}.dylib")
    elseif(WIN32)
        target_link_libraries(corianderdnn "${CORIANDER_DIR}\\lib\\lib${libname}.lib")
    else()
        target_link_libraries(corianderdnn "${CORIANDER_DIR}/lib/lib${libname}.so")
    endif()
endforeach()
target_include_directories(corianderdnn PRIVATE "${CORIANDER_DIR}/include")
target_include_directories(corianderdnn PRIVATE "include")
target_include_directories(corianderdnn SYSTEM BEFORE PRIVATE "${CORIANDER_DIR}/include/clew/proxy-headers")
target_include_directories(corianderdnn PRIVATE ${CLANG_HOME}/include)

# include(test/CMakeLists.txt)
add_subdirectory(test)

CONFIGURE_FILE(
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake/corianderdnn.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/cmake/corianderdnn.cmake" @ONLY)
INSTALL(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/cmake/corianderdnn.cmake DESTINATION share/cocl/coriander_plugins)

INSTALL(FILES include/cudnn.h DESTINATION ${CORIANDER_DIR}/include/coriander_plugins/corianderdnn)
FILE(GLOB DNN_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/include/coriander-dnn/*.h)
INSTALL(FILES ${DNN_HEADERS} DESTINATION ${CORIANDER_DIR}/include/coriander_plugins/corianderdnn/coriander-dnn)

install(TARGETS corianderdnn EXPORT corianderdnn-targets
    LIBRARY DESTINATION lib/coriander_plugins
    ARCHIVE DESTINATION lib/coriander_plugins
    RUNTIME DESTINATION lib/coriander_plugins
)
install(EXPORT corianderdnn-targets DESTINATION lib/coriander_plugins)
