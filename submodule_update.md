How to update
-------------

```
cd lib/gTTS-token
git pull base master
```

Resolve merge.

```
git add *
git commit -m "update submodule"
git push origin master
cp -r gtts_token ../gTTS/gtts

cd ../gTTS
git pull base master
```

Resolve merge.

```
git add *
git commit -m "update submodule"
git push origin master
rm -rf ../../korean/lib/gtts
cp -r gtts ../../korean/lib/
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
