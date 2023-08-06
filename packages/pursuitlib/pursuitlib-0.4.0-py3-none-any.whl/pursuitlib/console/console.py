import sys
from typing import Optional, Union, IO

from pursuitlib.console.textcolor import TextColor
from pursuitlib.console.textcolors import TextColors
from pursuitlib.console.textcomponent import TextComponent
from pursuitlib.console.textstyle import TextStyle

##################
# Console writer #
##################


def write(item, style: Optional[Union[TextStyle, TextColor]] = None):
    write_to(sys.stdout, item, style)


def write_line(item="", style: Optional[Union[TextStyle, TextColor]] = None):
    write(f"{item}\n", style)


def write_err(item, style: Optional[Union[TextStyle, TextColor]] = None):
    if style is None:
        style = TextColors.LIGHT_RED
    write_to(sys.stderr, item, style)


def write_err_line(item="", style: Optional[Union[TextStyle, TextColor]] = None):
    write_err(f"{item}\n", style)


def write_to(stream: IO, item, style: Optional[Union[TextStyle, TextColor]] = None):
    if style is None:
        stream.write(str(item))
    else:
        if isinstance(style, TextColor):
            style = TextStyle(color=style)
        stream.write(str(TextComponent(style, item)))


def confirm(prompt: str, default_answer: Optional[bool] = None) -> bool:
    while True:
        if default_answer is None:
            choices = "[y/n]"
        elif default_answer:
            choices = "[Y/n]"
        else:  # not default_answer
            choices = "[y/N]"

        result = input(f"{prompt} {choices} ").strip().lower()

        if result == "" and default_answer is not None:
            return default_answer
        elif result == "y":
            return True
        elif result == "n":
            return False
