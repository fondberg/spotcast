#!/bin/bash

PYTHON_VER="3.9.7"

echo "This script will install dependencies for the developper environnement of Spotcast"
echo -n "Do you wish to continue [Y/n]: "
read -r accept
accept=${accept^^}
valid=false

while [[ "$valid" != true ]]; do

    if [[ "$accept" == "N" ]]; then
        exit 0
    elif [[ "$accept" == "Y" ]]; then
        valid=true
    else
        echo -n "invalid choice. Do you wish to continue [Y/n]: "
        read -r accept
        accept=${accept^^}
    fi
done

# install current Python version
