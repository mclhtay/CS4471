#!/bin/bash

pip3 install -r requirements.txt --user

pre-commit install

cd ..

py -m HotelBooking