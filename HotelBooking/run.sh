#!/bin/bash


#if this shell script is not working, navigate you self to the home directory of the HotelBooker project and type 
#command 'python3 -m HotelBooking'


#add --user at the end of the command if you are using windows computer
pip3 install -r requirements.txt

pre-commit install

cd ..

python3 -m HotelBooking.main
