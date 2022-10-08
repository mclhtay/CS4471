#!/bin/bash

pip3 install -r requirements.txt

pre-commit install

cd ..

python3 -m HotelBooking.main