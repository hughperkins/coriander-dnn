#include <iostream>

extern "C" {
    void corianderdnn_init();
    void corianderdnn_unload();
}

void corianderdnn_init() {
    std::cout << "corianderdnn_init" << std::endl;
}

void corianderdnn_unload() {
    std::cout << "corianderdnn_unload" << std::endl;
}
