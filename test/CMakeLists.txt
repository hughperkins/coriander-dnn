# Designed to be run from the main CMakeLists.txt, in the root of the Coriander-dnn repo
# via include(...)

if(BUILD_TESTS)
else()
set(TESTS_EXCLUDE EXCLUDE_FROM_ALL)
endif()

if(UNIX)
    add_library(corianderdnn_gtest SHARED  ${TESTS_EXCLUDE} ../third_party/gtest/gtest-all.cc)
    target_link_libraries(corianderdnn_gtest pthread)
else()
    add_library(corianderdnn_gtest  ${TESTS_EXCLUDE} ../third_party/gtest/gtest-all.cc)
endif()

add_executable(gtest-tests ${TESTS_EXCLUDE} gtest/gtest_main.cpp gtest/GtestGlobals.cpp
    gtest/test_dnn_conv.cpp gtest/test_dnn_act.cpp gtest/test_dnn_loss.cpp
    gtest/test_dnn_pooling.cpp
)
# target_include_directories(gtest-tests PRIVATE src)
target_include_directories(gtest-tests PRIVATE ../include)
# target_include_directories(gtest-tests PRIVATE src/EasyCL/thirdparty/clew/include)
target_include_directories(gtest-tests PRIVATE ../third_party/gtest)
# target_include_directories(gtest-tests PRIVATE ${CLANG_HOME}/include)
target_link_libraries(gtest-tests corianderdnn_gtest easycl)
# target_compile_options(gtest-tests PRIVATE ${LLVM_CXXFLAGS} ${LLVM_DEFINES})
target_link_libraries(gtest-tests corianderdnn)

add_custom_target(run-gtest-tests
    COMMAND echo
    COMMAND echo make run-gtest-tests
    COMMAND ${COCL_DUMP_CL_STR} ${CMAKE_CURRENT_BINARY_DIR}/gtest-tests
    DEPENDS gtest-tests
)

set(BUILD_TEST_TARGETS ${BUILD_TEST_TARGETS} gtest-tests)
set(RUN_TEST_TARGETS ${RUN_TEST_TARGETS} run-gtest-tests)

add_custom_target(tests
    DEPENDS ${BUILD_TEST_TARGETS})
add_custom_target(run-tests
    DEPENDS tests ${RUN_TEST_TARGETS})
