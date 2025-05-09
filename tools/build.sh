#!/bin/bash

set -u
set -e

APWORLD_NAME=mzm
FILES="
    LICENSE
    data
    *.py
"
EXCLUDE="
    data/item_sprites/*.png
    data/item_sprites/README.md
"
if [ $# -ge 1 ]; then
    WORLD_VERSION="$1"
else
    COMMIT="$(git rev-parse HEAD)"
    WORLD_VERSION="${COMMIT:0:7}"
fi

echo "Building AP world version $WORLD_VERSION"

WORLD_DIR="build/$APWORLD_NAME"

mkdir -p build
rm -rf build/*
mkdir "$WORLD_DIR"
cp -r $FILES "$WORLD_DIR"

echo "APWORLD_VERSION = '$WORLD_VERSION'" >> "$WORLD_DIR/data.py"

cd "$WORLD_DIR"
rm -rf $EXCLUDE
cd ..
zip -r "$APWORLD_NAME.apworld" "$APWORLD_NAME"
