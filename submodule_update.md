How to set up
-------------

```
git submodule init
git submodule update
cd lib/gTTS
git remote add base https://github.com/pndurette/gTTS
cd ../gTTS-token
git remote add base https://github.com/Boudewijn26/gTTS-token
```

How to build
------------

```
mkdir -p korean/lib
cd lib/gTTS
rm -rf ../../korean/lib/gtts
cp -r gtts ../../korean/lib/
cp LICENSE ../../korean/lib/gtts
cd ../gTTS-token
cp -r gtts_token ../../korean/lib/gtts
cp LICENSE ../../korean/lib/gtts/gtts_token
cd ../kengdic
rsync -ah python/kengdic/ ../../korean/lib/kengdic/ --delete
cp LICENSE ../../korean/lib/kengdic
cd ../../
```


How to update
-------------

```
cd lib/gTTS
git pull base master
```

Resolve merge.

```
git add *
git commit -m "update submodule"
git push origin master

cd ../gTTS-token
git pull base master
```

Resolve merge.

```
git add *
git commit -m "update submodule"
git push origin master

cd ../kengdic
git pull origin master
cd ../../
git add *
git commit -m "update submodules"
git push origin master
```

How to bundle
-------------

```
find korean -type d -name "__pycache__" | xargs rm -rf
find korean -type f -name "desktop.ini" | xargs rm -rf
zip -r korean.zip korean
```
