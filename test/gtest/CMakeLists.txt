# Designed to be run from the main CMakeLists.txt, in the root of the Coriander-dnn repo
# via include(...)

if(UNIX)
    add_library(corianderdnn_gtest SHARED  ${TESTS_EXCLUDE} third_party/gtest/gtest-all.cc)
    target_link_libraries(corianderdnn_gtest pthread)
else()
    add_library(corianderdnn_gtest  ${TESTS_EXCLUDE} third_party/gtest/gtest-all.cc)
endif()

add_executable(gtest-tests ${TESTS_EXCLUDE} gtest_main.cpp GtestGlobals.cpp
    test_dnn_conv.cpp test_dnn_act.cpp test_dnn_loss.cpp
    test_dnn_pooling.cpp
)
target_include_directories(gtest-tests PRIVATE ${CORIANDERDNN_INCLUDE})
target_include_directories(gtest-tests PRIVATE third_party/gtest)
target_include_directories(gtest-tests PRIVATE ${COCL_INCLUDE})
target_link_libraries(gtest-tests corianderdnn_gtest easycl)
target_link_libraries(gtest-tests corianderdnn)
# target_compile_options(gtest-tests PRIVATE -DUSE_CLEW)

add_custom_target(run-gtest-tests
    COMMAND echo
    COMMAND echo make run-gtest-tests
    COMMAND ${COCL_DUMP_CL_STR} ${CMAKE_CURRENT_BINARY_DIR}/gtest-tests
    DEPENDS gtest-tests
)

set(BUILD_TEST_TARGETS ${BUILD_TEST_TARGETS} gtest-tests PARENT_SCOPE)
set(RUN_TEST_TARGETS ${RUN_TEST_TARGETS} run-gtest-tests PARENT_SCOPE)
