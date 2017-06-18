// adapted from cudnn-training  https://github.com/tbennun/cudnn-training/

#include <iostream>

#include <cuda_runtime.h>
#include <device_launch_parameters.h>

#include <cublas_v2.h>
#include <cudnn.h>

void checkCudaErrors(size_t status) {
    if(status != 0) {
        std::cout << "ERROR status non-zero: " << status << std::endl;
    }
}

void checkCUDNN(size_t status) {
    if(status != 0) {
        std::cout << "ERROR status non-zero: " << status << std::endl;
    }
}

int main(int argc, char *argv[]) {
    cudnnHandle_t cudnnHandle;
    cublasHandle_t cublasHandle;
    cudnnTensorDescriptor_t dataTensor;

    // Create CUBLAS and CUDNN handles
    int gpuid = 0;
    checkCudaErrors(cudaSetDevice(gpuid));
    checkCudaErrors(cublasCreate(&cublasHandle));
    checkCUDNN(cudnnCreate(&cudnnHandle));

    // Create tensor descriptors
    checkCUDNN(cudnnCreateTensorDescriptor(&dataTensor));

    return 0;
}
