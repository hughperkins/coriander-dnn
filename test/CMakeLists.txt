cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)

# Originally designed to be run from the main CMakeLists.txt, in the root of the Coriander repo
# via include(...)

if(BUILD_TESTS)
else()
set(TESTS_EXCLUDE EXCLUDE_FROM_ALL)
endif()

if(TARGET corianderdnn)
    # runnign embedded
else()
    # running standalone
    include($ENV{COCL_CMAKE}/cocl_vars.cmake)
    include($ENV{COCL_CMAKE}/cocl_impl.cmake)
    include(${COCL_LIB}/cocl/cocl-targets.cmake)
    include(${COCL_LIB}/coriander_plugins/corianderclblast-targets.cmake)
    include(${COCL_LIB}/coriander_plugins/corianderdnn-targets.cmake)
    set(CORIANDERDNN_INCLUDE ${COCL_INCLUDE}/coriander_plugins/corianderdnn)
    add_definitions(-DUSE_CLEW)
    if(WIN32)
        set(CMAKE_CXX_FLAGS "/EHsc")
    else()
        set(CMAKE_CXX_FLAGS "-std=c++11 -fPIC -g")
        set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath,$ORIGIN")
    endif()
endif()

add_subdirectory(gtest)

add_custom_target(tests
    DEPENDS ${BUILD_TEST_TARGETS})
add_custom_target(run-tests
    DEPENDS tests ${RUN_TEST_TARGETS})
