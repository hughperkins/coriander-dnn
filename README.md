# coriander-dnn
DNN API for Coriander

This repo acts as both:
- demonstration of creating plugins for [Coriander](https://github.com/hughperkins/coriander)
- partial implementation of cuDNN API

Note that you need the branch [pluggable](https://github.com/hughperkins/coriander/tree/pluggable) of Coriander, for the time being.

## Installation

- first, install the [pluggable branch](https://github.com/hughperkins/coriander/tree/pluggable) of Coriander
- then run `cocl_plugins install --repo-url https://github.com/hughperkins/coriander-dnn`

## Testing

Download https://github.com/hughperkins/coriander-dnn/raw/master/test/endtoend/basic1.cu to an empty folder somewhere, then,
from that folder, do:
```
cocl_py --clang-home /usr/local/opt/llvm-4.0 basic1.cu
# hopefully compiles ok
# then run it
./basic.cu
# hopefully will print the model of your gpu at least
```
