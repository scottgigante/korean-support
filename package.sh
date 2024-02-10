#!/usr/bin/env bash
./build.sh

rm -f korean.zip
find korean -type d -name "__pycache__" | xargs rm -rf
find korean -type f -name "desktop.ini" | xargs rm -rf
cd korean && zip -r ../korean.zip * && cd ..
