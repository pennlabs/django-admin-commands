#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: ./init.sh <name of project> <name of github repo> <name of pypi package>"
    exit 1
fi

find . -type f -exec sed -i "s/project-name/$1/g" {} \;
find . -type f -exec sed -i "s/github-project/$2/g" {} \;
find . -type f -exec sed -i "s/pypi-project/$3/g" {} \;

mv README.md.template README.md

rm init.sh
