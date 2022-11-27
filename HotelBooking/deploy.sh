#!/bin/bash

# using while in case we add more flags in the future
while getopts e: flag
do
  case "${flag}" in
    e) env=${OPTARG};;
  esac
done

if [ -z "$env" ]; then
  echo "Empty deployment environment, use -e <OS> to generate executable"
elif [ $env == "osx" ]; then
  echo "Deploying for Mac OSX"
  pyinstaller --onefile \
    --collect-all pyfiglet \
    main.py
  mkdir -p HotelBooker/DB
  mv dist/main HotelBooker/HotelBooker
  cp Database/Hotel.db HotelBooker/DB/
elif [ $env == "windows" ]; then
  echo "Deploying for Windows"
else
  echo "Not valid environment, pick between 'osx' and 'windows'"
fi
