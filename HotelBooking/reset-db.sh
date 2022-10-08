#!/bin/bash

rm Database/Hotel.db

sqlite3 Database/Hotel.db -init Database/create_database.sql .quit