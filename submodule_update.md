How to set up
-------------

```
git submodule init
git submodule update
cd lib/gTTS
git remote add base https://github.com/pndurette/gTTS
git checkout master
cd ../NaverTTS
git checkout master
cd ../kengdic
git checkout master
cd ../krdict
git checkout main
cd ../..
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
```

Resolve merge.

```
git add *
git commit -m "update submodule"
git push origin master

cd ../kengdic
git pull origin master
cd ../NaverTTS
git pull origin master
cd ../../
git add *
git commit -m "update submodules"
git push origin master
```

How to build
------------

```
./build.sh
```

How to bundle
-------------

```
./package.sh
```
