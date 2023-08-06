from typing import Optional, Union

from pursuitlib.console.textcolor import TextColor
from pursuitlib.console.textstyle import TextStyle


class TextComponent:
    @staticmethod
    def concat(*components) -> "TextComponent":
        return TextComponent(None, *components)

    def __init__(self, style: Optional[Union[TextStyle, TextColor]] = None, *children):
        self.parent: Optional[TextComponent] = None

        if isinstance(style, TextStyle):
            self.style = style
        elif isinstance(style, TextColor):
            self.style = TextStyle(color=style)
        else: self.style = TextStyle()

        self.children = list(children)

    def set_parent(self, parent: "TextComponent"):
        self.parent = parent

    def get_parent(self) -> Optional["TextComponent"]:
        return self.parent

    def set_style(self, style: TextStyle):
        self.style = style

    def get_style(self) -> TextStyle:
        return self.style

    def append(self, *children):
        for child in children:
            if isinstance(child, TextComponent):
                child.set_parent(self)
            self.children.append(child)

    def appendline(self, *children):
        self.append(*children, '\n')

    def length(self) -> int:
        length = 0
        for child in self.children:
            if isinstance(child, TextComponent):
                length += child.length()
            else: length += len(str(child))
        return length

    def render(self) -> str:
        result = f"{self.get_style().as_formatting(self)}"
        for child in self.children:
            if isinstance(child, TextComponent):
                result += child.render()
                # Reset the formatting to this component's formatting
                result += f"{self.get_style().as_formatting(self)}"
            else: result += str(child)

        # Always finish by resetting the text formatting
        if self.parent is None:
            result += str(TextStyle.FORMAT_RESET)
        return result

    def __len__(self) -> int:
        return self.length()

    def __str__(self) -> str:
        return self.render()
