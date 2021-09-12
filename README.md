# Space Radar [![Build Status](https://app.travis-ci.com/antoniobarbuzzi/spaceradar.svg?branch=main)](https://app.travis-ci.com/antoniobarbuzzi/spaceradar)

## TL; DR; 
bash run.sh

The script will try to create a virtualenv and install the package inside it.


## Installing
`python setup.py install`

You may want to run it into a virtualenv (see run.sh)
`space_radar` command will be available, which may be used to run the command line interface. 

## Running
Type:
`space_radar`

## CI

Travis is enabled on this repo for continous integration. Click the badge on the top to check build status.

## Local development overview
- See [separate README](tests/README.md) for testing 
- Package 
 `python setup.py sdist`
- Clean
  `python setup.py clean`
 or
  `make clean`
