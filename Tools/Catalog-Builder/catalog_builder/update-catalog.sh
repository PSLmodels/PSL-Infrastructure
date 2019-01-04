#!/bin/bash

cd $HOME/catalog_update/PSL-Core/Tools/Catalog-Builder/catalog_builder
export DATE=`date +%Y-%m-%d`
export BRANCH_NAME=catalog-$DATE
git checkout -b $BRANCH_NAME
python catalog.py 
git status
git add -u
git commit -m "Update catalog for date $DATE"
git push origin catalog-$DATE
git checkout test_automation
git pull --no-edit origin $BRANCH_NAME
git push origin test_automation
git checkout catalog-update