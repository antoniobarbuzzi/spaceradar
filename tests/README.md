How to run tests
===============================

# TL;DR;

`bash test.sh [--help]`


# Set up the environment

All the tests run inside a virtual environment, where all the dependencies are installed.

# How to run tests

To run all the tests
```
bash test.sh
```

If you want to run the tests multiple times you may want to reuse the same virtualenv, so
```
bash tests.sh -r
```

## Running tests using pycharm/your_ide

The easiest way to run tests in pycharm is to install all the dependencies on your system (`pip2 install --upgrade --requirement tests/requirements.txt`), or configure pycharm to use a virtual environment. 
