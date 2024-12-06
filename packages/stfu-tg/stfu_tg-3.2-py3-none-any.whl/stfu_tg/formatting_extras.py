from .doc import Element, EscapedStr, SupportsStr
from .formatting import Bold


class Title(Element):
    def __init__(
            self,
            item: Element | SupportsStr,
            prefix: Element | SupportsStr = '[',  # Only for HTML
            postfix: Element | SupportsStr = ']',  # Only for HTML
            bold: bool = True,  # Only for HTML
            level: int = 1  # Only for Markdown
    ):
        self.item = item
        self.prefix = prefix
        self.postfix = postfix
        self.bold = bold
        self.level = level

    def to_html(self) -> str:
        text = f"{EscapedStr(self.prefix).to_html()}{EscapedStr(self.item).to_html()}{EscapedStr(self.postfix).to_html()}"

        if self.bold:
            text = str(Bold(text))

        return text

    def to_md(self) -> str:
        # Markdown has native Title supports
        prefix = '#' * self.level
        return f"\n{prefix} {EscapedStr(self.item).to_md()}\n"


class Template(Element):
    def __init__(
            self,
            item: Element | SupportsStr,
            **kwargs: Element | SupportsStr
    ):
        self.item = item
        self.placeholders = kwargs

    def to_html(self, *args) -> str:
        text = str(self.item)

        for k, v in self.placeholders.items():
            text = text.replace(f'{{{k}}}', str(EscapedStr(v).to_html()))

        return text
