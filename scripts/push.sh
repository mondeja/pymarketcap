#!/bin/bash

CURRENT_DIR=${PWD##*/}
if [ $CURRENT_DIR = "scripts" ]
then
  cd ..
fi

# Activate virtualenv
source env/bin/activate

# Install new library version
python3 setup.py install

# Unittesting
echo "Testing pymarketcap..."
cd test
python3 test.py --with-timer -v

if [ $? -eq 1 ] # Tests failed?
then
  exit 1
else
  rm benchmarking.json  # Delete bench results
fi

# New version
cd ..
version=$(python3 scripts/vss.py 2>&1)  # Redirect stdout

echo "New version $version"

# Upload to PyPi
echo "Uploading to Pypi..."
python3 setup.py sdist
sudo twine upload dist/pymarketcap-$version.tar.gz

if [ $? -eq 1 ] # Upload failed?
then
  echo "Upload failed"
  exit 1
fi

echo "Upload successfully!"
echo

echo "Cleaning..."
rm -Rf dist build pymarketcap.egg-info

echo
echo "Ready to add, commit and push"
