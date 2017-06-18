cmake_minimum_required(VERSION 3.0.0)

if(WIN32)
    set(CORIANDER_DIR "C:\\Program Files\\Coriander" CACHE PATH "Installation directory of Coriander")
    set(CLANG_HOME "C:\\Program Files\\LLVM" CACHE PATH "the downloaded clang-4.0.0 folder, containing lib, bin etc")
else()
    set(CLANG_HOME "/usr/local/opt/llvm-4.0" CACHE PATH "the downloaded clang-4.0.0 folder, containing lib, bin etc")
    set(CORIANDER_DIR "/usr/local" CACHE PATH "Installation directory of Coriander")
endif()

set(CMAKE_CXX_FLAGS "-std=c++11 -fPIC -g ${PLATFORM_OPTIONS}")
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath,$ORIGIN")
add_definitions(-DUSE_CLEW)

add_library(corianderdnn SHARED src/cocl_dnn.cpp src/cocl_dnn_act.cpp src/cocl_dnn_conv.cpp src/cocl_dnn_gemm.cpp src/cocl_dnn_pooling.cpp
    coriander_dnn_init.cpp)
foreach(libname cocl clblast easycl clew)
    if(APPLE)
        target_link_libraries(corianderdnn "${CORIANDER_DIR}/lib/lib${libname}.dylib")
    else()
        target_link_libraries(corianderdnn "${CORIANDER_DIR}/lib/lib${libname}.so")
    endif()
endforeach()
target_include_directories(corianderdnn PRIVATE "${CORIANDER_DIR}/include")
target_include_directories(corianderdnn PRIVATE "include")
target_include_directories(corianderdnn SYSTEM BEFORE PRIVATE "/usr/local/include/clew/proxy-headers")
target_include_directories(corianderdnn PRIVATE ${CLANG_HOME}/include)

install(TARGETS corianderdnn EXPORT corianderdnn-targets
    LIBRARY DESTINATION coriander_plugins
    ARCHIVE DESTINATION coriander_plugins
    RUNTIME DESTINATION coriander_plugins
)
install(EXPORT corianderdnn-targets DESTINATION lib/corianderdnn)
