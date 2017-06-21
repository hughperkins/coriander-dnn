# Designed to be run from the main CMakeLists.txt, in the root of the Coriander-dnn repo
# via include(...)

if(BUILD_TESTS)
else()
set(TESTS_EXCLUDE EXCLUDE_FROM_ALL)
endif()

add_subdirectory(gtest)

add_custom_target(tests
    DEPENDS ${BUILD_TEST_TARGETS})
add_custom_target(run-tests
    DEPENDS tests ${RUN_TEST_TARGETS})
