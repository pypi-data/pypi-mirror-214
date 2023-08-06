from typing import Tuple


class TextFormatting:
    ESCAPE = "\x1b"

    @staticmethod
    def combine(*formatting: "TextFormatting") -> "TextFormatting":
        codes = []
        for fmt in formatting:
            codes += list(fmt.get_codes())
        return TextFormatting(*codes)

    def __init__(self, *codes: int):
        self.codes = codes

    def get_codes(self) -> Tuple[int]:
        return self.codes

    def __str__(self) -> str:
        return f"{TextFormatting.ESCAPE}[" + ";".join([str(code) for code in self.get_codes()]) + "m"
