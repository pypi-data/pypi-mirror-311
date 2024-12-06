from typing import Sequence

from stfu_tg.doc import SupportsStr, Element, EscapedStr, MDOnlyElement


class TableMD(MDOnlyElement):
    def __init__(self, headers: Sequence[SupportsStr | Element], *rows: Sequence[list[SupportsStr | Element]]):
        self.headers = headers
        self.rows = rows

    def to_md(self) -> str:
        # Convert headers to Markdown
        headers_md = "| " + " | ".join(EscapedStr(header).to_md() for header in self.headers) + " |"
        separator = "| " + " | ".join("---" for _ in self.headers) + " |"

        # Convert rows to Markdown
        rows_md = "\n".join(
            "| " + " | ".join(EscapedStr(cell).to_md() for cell in row) + " |"
            for row in self.rows
        )

        # Combine all parts
        return f"{headers_md}\n{separator}\n{rows_md}"
