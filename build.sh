#!/usr/bin/env bash
mkdir -p korean/lib
cd lib/gTTS
rm -rf ../../korean/lib/gtts
cp -r gtts ../../korean/lib/
cp LICENSE ../../korean/lib/gtts
cd ../kengdic
rsync -ah python/kengdic/ ../../korean/lib/kengdic/ --delete
cp LICENSE ../../korean/lib/kengdic
cd ../NaverTTS
rsync -ah navertts/ ../../korean/lib/navertts/ --delete
cp LICENSE ../../korean/lib/navertts
cd ../../
