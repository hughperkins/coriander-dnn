# coriander-dnn
DNN API for Coriander

This repo provides a partial implementation of cuDNN API

## Installation

- first, install [coriander](https://github.com/hughperkins/coriander)
- then run `cocl_plugins install --repo-url https://github.com/hughperkins/coriander-dnn`

## Testing

### Smoke test

This is mostly just to check plugins are working ok. Plugins are new :-)

Download https://github.com/hughperkins/coriander-dnn/raw/master/test/endtoend/basic1.cu to an empty folder somewhere, then,
from that folder, do:
```
cocl_py --clang-home /usr/local/opt/llvm-4.0 basic1.cu
# hopefully compiles ok
# then run it
./basic.cu
# hopefully will print the model of your gpu at least
```

### Unit tests

There are unit tests in [test/gtest].  You can build them:
```
make -j 8 tests
```
And run them:
```
make run-tests
```

### cudnn test

This test uses the cudnn code at https://github.com/tbennun/cudnn-training to test that we can run convolutions and so on.  I modified
it slightly, to add a `USE_OPENCL` option, https://github.com/hughperkins/cudnn-training

To build `cudnn-training` using Coriander-dnn, you can do the following
- first install Coriander, and the Coriander-dnn plugin
- then build cudnn-training:
```
git clone https://github.com/hughperkins/cudnn-training
cd cudnn-training
mkdir build
cd build
ccmake ..
# press 'c' configure
# ignore the error about NVIDIA® CUDA™ toolkit not found, we dont need it
# change `USE_CUDA` to off
# change `USE_OPENCL` to on
# press 'c' configure, then 'g' generate
make
```
- download the mnist data:
```
wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
gunzip train-images-idx3-ubyte.gz
gunzip train-labels-idx1-ubyte.gz
gunzip t10k-images-idx3-ubyte.gz
gunzip t10k-labels-idx1-ubyte.gz
```
- run:
```
./lenet
```
You should see iterations start running.
