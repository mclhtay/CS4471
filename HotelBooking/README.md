# Hotel Booking

**NOTE**: all commands in scripts are linux commands, if you are running in windows power-shell you might need to find alternatives.

**NOTE** This app runs best with Python 3.7 and has known issues with Python 3.9

## How to Run

1. `./run.sh`

## Database

- The database being used is sqlite, and support for sqlite is built-in in Python, and it should have no problem running on MacOS. If you run into errors, first check if your system has sqlite.
- If the database is corrupt, run `./reset-db.sh` to recreate the database and tables with initial data.
  - Note that the command in the reset script is Linux based and does **NOT** work in windows. You need to find windows equivalent commands for sqlite if you are using windows power-shell.

## Deployment

- The deployment framework is `PyInstaller`
- Deployment configurations for Windows is currently missing
- For MacOS deployment:
  - Easiest way of setting up is by running `brew install pyinstaller`
  - After pyinstaller is installed, run `./deploy.sh -e osx`
  - This will generate the one file MacOS binary inside HotelBooker/
