#!/bin/bash

if [ "$1" = "test" ]; then
    twine upload --repository testpypi dist/* --verbose
elif [ "$1" = "prod" ]; then
    twine upload --repository pypi dist/*
else
    echo "Please specify 'test' or 'prod' as an argument"
    exit 1
fi