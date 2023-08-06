from typing import List, Tuple

from pursuitlib.console.textcomponent import TextComponent


class Table:
    COLUMN_PADDING = 1

    def __init__(self):
        self.rows: List[Tuple[any]] = []

    def append_row(self, *columns: any):
        self.rows.append(columns)

    def get_row_count(self) -> int:
        return len(self.rows)

    def get_column_count(self) -> int:
        if len(self.rows) == 0:
            return 0
        return max([len(row) for row in self.rows])

    def get_column_widths(self) -> List[int]:
        widths = [0] * self.get_column_count()
        for row in self.rows:
            for col, component in enumerate(row):
                widths[col] = max(widths[col], len(component))
        return widths

    def as_lines(self) -> List[TextComponent]:
        lines = []
        widths = self.get_column_widths()
        for row in self.rows:
            line = TextComponent(None)
            for col, component in enumerate(row):
                padding = widths[col] - len(component)
                if col < len(widths) - 1:  # Do not add column padding after the last column
                    padding += Table.COLUMN_PADDING
                line.append(component, ' ' * padding)
            lines.append(line)
        return lines

    def as_text(self) -> TextComponent:
        text = TextComponent()
        lines = self.as_lines()
        for i, line in enumerate(lines):
            if i < len(lines) - 1:
                text.appendline(line)
            else: text.append(line)  # Do not append a newline at the end of the table
        return text

    def __str__(self) -> str:
        return self.as_text().render()
