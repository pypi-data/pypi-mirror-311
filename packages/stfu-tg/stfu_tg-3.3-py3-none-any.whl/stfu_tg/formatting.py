import html
from typing import Optional, ClassVar

from stfu_tg.doc import Element, EscapedStr, SupportsStr


class StyleStr(Element):
    prefix: ClassVar[str]
    postfix: ClassVar[str]
    md_marker: ClassVar[str]

    @staticmethod
    def encapsulate(prefix: str, postfix: str, item: Optional[str]) -> str:
        # Do not add prefix and postfix on empty items
        if not item:
            return ''
        return f'{prefix}{item}{postfix}'

    def to_html(self) -> str:
        return self.encapsulate(self.prefix, self.postfix, EscapedStr(self.item).to_html())

    def to_md(self) -> str:
        return self.encapsulate(self.md_marker, self.md_marker, EscapedStr(self.item).to_md())

    def __init__(self, item: Optional[Element | SupportsStr]):
        self.item = item


class Bold(StyleStr):
    prefix = '<b>'
    postfix = '</b>'
    md_marker = '**'


class Italic(StyleStr):
    prefix = '<i>'
    postfix = '</i>'
    md_marker = '*'


class Code(StyleStr):
    prefix = '<code>'
    postfix = '</code>'
    md_marker = '`'


class Strikethrough(StyleStr):
    prefix = '<s>'
    postfix = '</s>'
    md_marker = '~~'


class Underline(StyleStr):
    prefix = '<u>'
    postfix = '</u>'

    # Only Telegram's Markdown!
    md_marker = '__'


class Spoiler(StyleStr):
    prefix = '<tg-spoiler>'
    postfix = '</tg-spoiler>'

    # Only Telegram's Markdown!
    md_marker = '||'


class Pre(StyleStr):
    prefix = '<pre>'
    postfix = '</pre>'

    md_marker = '```\n'

    def __init__(self, item: Element | SupportsStr, language: Optional[str] = None):
        self.language = language
        super().__init__(item)

    def to_html(self) -> str:
        prefix = self.prefix
        if self.language:
            prefix += f'<code class="language-{self.language}">'

        return self.encapsulate(prefix, self.postfix, EscapedStr(self.item).to_html())

    def to_md(self) -> str:
        prefix = self.md_marker
        if self.language:
            prefix = f'``` {self.language}\n'

        return self.encapsulate(prefix, ''.join(reversed(self.md_marker)), EscapedStr(self.item).to_md())


class Url(StyleStr):
    prefix = '<a>'
    postfix = '</a>'

    def __init__(self, item: Element | SupportsStr, link: str):
        self.link = link
        super().__init__(item)

    def to_html(self) -> str:
        # We escape it manually because we need to escape quotes as well
        prefix = f'<a href="{html.escape(self.link)}">'
        return self.encapsulate(prefix, self.postfix, EscapedStr(self.item).to_html())

    def to_md(self) -> str:
        return f'[{EscapedStr(self.item).to_md()}]({self.link})'


class BlockQuote(StyleStr):
    prefix = '<blockquote>'
    postfix = '</blockquote>'

    def __init__(self, item: Element | SupportsStr, expandable: bool = False):
        self.expandable = expandable
        super().__init__(item)

    def to_html(self) -> str:
        prefix = '<blockquote expandable>' if self.expandable else self.prefix
        return self.encapsulate(prefix, self.postfix, EscapedStr(self.item).to_html())

    def to_md(self) -> str:
        # Ignore expandability in Markdown
        return '> ' + EscapedStr(self.item).to_md().replace('\n', ' \\\n> ')
