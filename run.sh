#!/bin/bash
echo "Getting files for creating virtual environment"
pip install virtualenv
echo "Building Virtual Environment..."
virtualenv .RealEstateWebsite-env
python -venv 
echo "Starting Virtual Environment..."
source ./.RealEstateWebsite-env/bin/activate
echo "Done!"
echo "Building..."
pip install -r ./requirements.txt
echo "Done!"
echo "Site is now going live ..."
python main.py
echo "Deactivating Virutal Environment"
deactivate 
echo "Cleaning up"
rm -r .RealEstateWebsite-env

