from typing import Optional, TYPE_CHECKING

from pursuitlib.console.textcolor import TextColor
from pursuitlib.console.textformatting import TextFormatting

if TYPE_CHECKING:
    from pursuitlib.console.textcomponent import TextComponent


class TextStyle:
    FORMAT_RESET = TextFormatting(0)
    FORMAT_BOLD = TextFormatting(1)
    FORMAT_UNDERLINE = TextFormatting(4)
    FORMAT_STRIKETHROUGH = TextFormatting(9)

    def __init__(self, color: Optional[TextColor] = None, bold: Optional[bool] = None, underline: Optional[bool] = None, strikethrough: Optional[bool] = None):
        self.color = color
        self.bold = bold
        self.underline = underline
        self.strikethrough = strikethrough

    def get_color(self) -> Optional[TextColor]:
        return self.color

    def is_bold(self) -> Optional[bool]:
        return self.bold

    def is_underline(self) -> Optional[bool]:
        return self.underline

    def is_strikethrough(self) -> Optional[bool]:
        return self.strikethrough

    def get_effective_color(self, component: Optional["TextComponent"] = None) -> Optional[TextColor]:
        if self.color is not None:
            return self.color
        if component is not None and component.parent is not None:
            return component.parent.get_style().get_effective_color(component.parent)
        return None  # Use the terminal's default color

    def is_effectively_bold(self, component: Optional["TextComponent"] = None) -> bool:
        if self.bold is not None:
            return self.bold
        if component is not None and component.parent is not None:
            return component.parent.get_style().is_effectively_bold(component.parent)
        return False

    def is_effectively_underline(self, component: Optional["TextComponent"] = None) -> bool:
        if self.underline is not None:
            return self.underline
        if component is not None and component.parent is not None:
            return component.parent.get_style().is_effectively_underline(component.parent)
        return False

    def is_effectively_strikethrough(self, component: Optional["TextComponent"] = None) -> bool:
        if self.strikethrough is not None:
            return self.strikethrough
        if component is not None and component.parent is not None:
            return component.parent.get_style().is_effectively_strikethrough(component.parent)
        return False

    def as_formatting(self, component: Optional["TextComponent"] = None) -> TextFormatting:
        color = self.get_effective_color(component)
        bold = self.is_effectively_bold(component)
        underline = self.is_effectively_underline(component)
        strikethrough = self.is_effectively_strikethrough(component)

        # We want the TextFormatting element to be independant from the previous text formatting,
        # so we start by resetting it
        formatting = [TextStyle.FORMAT_RESET]
        if color is not None:
            formatting.append(color)
        if bold:
            formatting.append(TextStyle.FORMAT_BOLD)
        if underline:
            formatting.append(TextStyle.FORMAT_UNDERLINE)
        if strikethrough:
            formatting.append(TextStyle.FORMAT_STRIKETHROUGH)
        return TextFormatting.combine(*formatting)
