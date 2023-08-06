# DaisyKit

Documentation: [https://daisykit.nrl.ai](https://daisykit.nrl.ai)

DaisyKit is an easy AI toolkit for software engineers to integrate pretrained AI models and pipelines into their projects. You DON'T need to be an AI engineer to build AI software. This open source project includes:

- **DaisyKit SDK - C++**, the core of models and algorithms in NCNN deep learning framework.
- **DaisyKit Python** wrapper for easy integration with Python.
- **DaisyKit Android** - Example app demonstrate how to use DaisyKit SDK in Android.

Python wrapper of DaisyKit with [pybind11](https://github.com/pybind/pybind11), only support python3.x now.

Install from pip
==================

DaisyKit is available as wheel packages for macOS, Windows and Linux distributions, you can install with pip:

```
python -m pip install -U pip
python -m pip install -U daisykit
```

# Build from source

If you want to build daisykit with some options not as default, or just like to build everything yourself, it is not difficult to build DaisyKit from source.

## Prerequisites

**On Unix (Linux, OS X)**

* A compiler with C++11 support
* CMake >= 3.4

**On Mac**

* A compiler with C++11 support
* CMake >= 3.4

**On Windows**

* Visual Studio 2015 or higher
* CMake >= 3.4

## Build

1. Clone DaisyKit and initialize submodules

```bash
cd /pathto/daisykit
git submodule init && git submodule update
```

2. Build

```bash
mkdir build
cd build
cmake -DBUILD_PYTHON=ON ..
make
```

## Install

```bash
cd /pathto/daisykit/python
pip install .
```

if you use conda or miniconda, you can also install as following:
```bash
cd /pathto/daisykit/python
python3 setup.py install
```
