#!/bin/bash

cd $HOME/build_catalog/PSL/Tools/Catalog-Builder/catalog_builder
git fetch upstream
git merge upstream/master
export DATE=`date +%Y-%m-%d`
export BRANCH_NAME=catalog-$DATE
git checkout -b $BRANCH_NAME
which /Users/petermetz/anaconda3/bin/python
/Users/petermetz/anaconda3/bin/python catalog.py 
git status
git add -A
git commit -m "Update catalog for date $DATE"
git push origin catalog-$DATE
git checkout master
git pull --no-edit origin $BRANCH_NAME
git push origin master
git branch -D $BRANCH_NAME
git push origin --delete $BRANCH_NAME