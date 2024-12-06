from . import Title
from .doc import Doc, Element, EscapedStr, SupportsStr
from .formatting import Bold, Underline


class Section(Doc):
    def __init__(
            self,
            *items: Element | SupportsStr,
            title: Element | SupportsStr = '',
            title_underline: bool = True,
            title_bold: bool = False,
            indent: int = 1,
            indent_text: str = '  ',
            title_postfix: Element | SupportsStr = ':'
    ):
        self.items = items
        self.title = title
        self.title_underline = title_underline
        self.title_bold = title_bold
        self.indent = indent
        self.indent_text = indent_text
        self.title_postfix = title_postfix

        super().__init__(*items)

    def to_html(self, additional_indent: int = 0) -> str:
        escaped_title = EscapedStr(self.title).to_html()

        if self.title:
            title = Underline(escaped_title).to_html() if self.title_underline else escaped_title
            title = Bold(title).to_html() if self.title_bold else title
            text = f'{title}{EscapedStr(self.title_postfix).to_html()}'
        else:
            text = ''

        for item in self:
            text += '\n'

            if type(item) is Section:
                text += self.indent_text * (self.indent + additional_indent)
                text += item.to_html(additional_indent=additional_indent + self.indent)
            elif type(item) is VList:
                text += item.to_html(additional_indent=(additional_indent + self.indent) * 2)
            else:
                text += self.indent_text * (self.indent + additional_indent)
                text += EscapedStr(item).to_html()

        return text

    def to_md(self) -> str:
        # Try to use more native markdown approach
        return Doc(
            Title(
                self.title,
                level=4
            ),
            *self.items,
        ).to_md()


class VList(Doc):
    def __init__(
            self,
            *items: Element | SupportsStr,
            indent: int = 0,
            prefix: Element | SupportsStr = '- '
    ):
        super().__init__(*items)

        self.prefix = prefix
        self.indent = indent

    def to_html(self, additional_indent: int = 0) -> str:
        indent = self.indent + additional_indent
        space = ' ' * indent if indent else ' '
        text = ''
        for idx, item in enumerate(self):
            if idx > 0:
                text += '\n'
            text += f'{space}{EscapedStr(self.prefix).to_html()}{item}'

        return text

    def __str__(self) -> str:
        return self.to_html()

    def to_md(self) -> str:
        # Markdown doesn't need indents before lists, it does it automatically
        return ''.join(f'\n{self.prefix}{EscapedStr(item).to_md()}' for item in self)
