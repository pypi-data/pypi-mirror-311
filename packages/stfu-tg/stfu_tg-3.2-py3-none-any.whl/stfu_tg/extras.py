from .doc import Element, Doc, EscapedStr, SupportsStr
from .formatting import Bold


class KeyValue(Element):
    def __init__(
            self,
            title: Element | SupportsStr,
            value: Element | SupportsStr,
            suffix: Element | SupportsStr = ': ',
            title_bold: bool = True
    ):
        self.title = title
        self.value = value
        self.suffix = suffix
        self.title_bold = title_bold

    def to_html(self, *args) -> str:
        title = EscapedStr(self.title).to_html()
        if self.title_bold:
            title = Bold(title).to_html()
        return f'{title}{EscapedStr(self.suffix).to_html()}{EscapedStr(self.value).to_html()}'

    def to_md(self) -> str:
        title = EscapedStr(self.title).to_md()
        if self.title_bold:
            title = Bold(title).to_md()
        return f'{title}{EscapedStr(self.suffix).to_md()}{EscapedStr(self.value).to_md()}'


class HList(Doc):
    def __init__(
            self,
            *args: Element | SupportsStr,
            prefix: Element | SupportsStr = '',
            divider: Element | SupportsStr = ' '
    ):
        super().__init__(*args)

        self.prefix = prefix
        self.divider = divider

    def parse(self, markdown: bool) -> str:
        text = ''
        for idx, item in enumerate(self):
            if idx > 0:
                text += EscapedStr(self.divider).to_md() if markdown else EscapedStr(self.divider).to_html()
            if self.prefix:
                text += EscapedStr(self.prefix).to_md() if markdown else EscapedStr(self.prefix).to_html()
            text += EscapedStr(item).to_md() if markdown else EscapedStr(item).to_html()

        return text

    def to_html(self) -> str:
        return self.parse(markdown=False)

    def to_md(self) -> str:
        return self.parse(markdown=True)
