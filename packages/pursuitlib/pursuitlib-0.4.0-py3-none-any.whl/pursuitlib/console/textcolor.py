from pursuitlib.console.textformatting import TextFormatting


class TextColor(TextFormatting):
    @staticmethod
    def standard(code: int) -> "TextColor":
        return TextColor(code)

    @staticmethod
    def rgb(color: int) -> "TextColor":
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        return TextColor(38, 2, r, g, b)
