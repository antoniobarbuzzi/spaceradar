#!/bin/bash

export STAGE="localtest"
REUSE_VENV=false
USE_VENV=true
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
VENV="$DIR/.venv_tests"
REQUIREMENTS="$DIR/tests/requirements.txt"

function printHelp() {
    echo "Run tests"
    echo "$0 [-h|--help] [-r|--reuse-venv] [--dont-use-venv]"
    echo ""
}

function initializeVirtualenv() {
    type virtualenv >/dev/null 2>&1 || \
        { echo >&2 "Virtualenv is not installed - installing it for local user only" >&2;
          echo "You may install using the command 'pip3 install --user virtualenvwrapper'" >&2;
          exit 1; }

    if [ $REUSE_VENV != true ]; then
        echo "Creating/recreating virtualenv"
        rm -rf "$VENV"
        mkdir -p "$VENV"
        virtualenv --python=python3 "$VENV" || { echo "ERROR - Virtualenv creation failed; aborting" >&2; exit 1; }
    else
        echo "Skipping venv creation - reusing existing one"
    fi

    source "$VENV/bin/activate"
}

function installRequirements() {
    [ -z ${VIRTUAL_ENV+x} ] && { echo "ERROR - this method needs to run inside virtualenv" >&2; exit 1; }

    if [ $REUSE_VENV != true ]; then
        echo "Installing requirements"
        pip3 install --upgrade --requirement "$REQUIREMENTS" || { echo "ERROR - Failed to install requirements" >&2; exit 1; }
    else
        echo "Skipping installing requirements"
    fi
}

function checkSyntaxErrors() {
    echo "Checking python files for syntax errors"
    find "$DIR" -path '*/.venv' -prune -o -type f -name "*.py" -print0  | xargs -0 -n1 python3 -m py_compile || \
        { echo "ERRORS: invalid syntax" >&2; exit 1; }
}



while [[ $# > 0 ]];
do
    key="$1"
    case $key in
        -r|--reuse-venv)
            REUSE_VENV=true
        ;;
        --dont-use-venv)
            USE_VENV=false
        ;;
        -h|--help)
            printHelp
            exit 0
        ;;
        *)
            echo "Invalid argument '$1'" >&2
            printHelp
            exit 1
        ;;
    esac
    shift # past argument or value
done


if [ $USE_VENV == true ]; then
    initializeVirtualenv
    installRequirements
fi
export PYTHONDONTWRITEBYTECODE=1
checkSyntaxErrors
# python -m unittest discover -v
python3 setup.py test
