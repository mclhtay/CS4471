from pyfiglet import Figlet


def big_print(text: str):
    figlet = Figlet(font="big")
    print(figlet.renderText(text))


def error_print(prefix: str = "", suffix: str = ""):
    print(f'\n{prefix}Please try again{suffix}')
