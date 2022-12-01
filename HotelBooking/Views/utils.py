import os
from pyfiglet import Figlet
from datetime import datetime


def big_print(text: str, cls=True):
    """
    ASCII art console print in big font
    """
    if cls:
        # dedicated clear console function depending on user OS
        def cls_fn(): return os.system('cls' if os.name == 'nt' else 'clear')
        cls_fn()
    figlet = Figlet(font="big")
    print(figlet.renderText(text))


def medium_print(text: str):
    """
    ASCII art console print in medium font
    """
    figlet = Figlet(font="standard")
    print(figlet.renderText(text))


def error_print(prefix: str = "", suffix: str = ""):
    """
    Reusable error message template
    """
    print(f'\n{prefix}Please try again{suffix}')


def validate_date(date_text):
    """
    Validaters user date input against database date format
    """
    try:
        datetime.strptime(date_text, '%m/%d/%Y')
    except ValueError:
        return False
    return True
