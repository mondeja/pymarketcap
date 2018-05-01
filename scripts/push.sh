#!/bin/bash

CURRENT_DIR=${PWD##*/}
if [ $CURRENT_DIR = "scripts" ]; then
  cd ..
fi

TESTS=1
if [[ $1 = "no-test" || $1 = "--no-tests" ]]; then
    TESTS=0
fi

# Build documentation
#bash scripts/build_doc.sh


# Install new library version
sudo python3 setup.py install

# Unittesting
if [[ $TESTS -eq 1 ]]; then
    echo "Testing pymarketcap..."
    pytest tests -vs --end2end

    if [ $? -eq 1 ]; then  # Tests failed?
      exit 1
    else
      echo "Tests passed."
    fi
    echo
fi

make clean
make restore-sources

# New version
version=$(python3 scripts/vss.py micro 2>&1)  # Redirect stdout
echo "New version $version"
echo

# Upload to PyPi
echo "Uploading to Pypi..."
sudo python3 setup.py sdist
make restore-sources
sudo twine upload dist/pymarketcap-$version.tar.gz
make clean

if [ $? -eq 1 ] # Upload failed?
then
  echo "Pypi upload failed."
  exit 1
fi

echo "Upload successfully!"
echo

echo "Cleaning..."
make clean

echo
echo "Ready to add, commit and push"
