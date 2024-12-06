import html
from abc import ABC
from typing import List, Protocol


class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...


class Element(ABC):
    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def __add__(self, other):
        return Doc(self, other)

    def __str__(self) -> str:
        return self.to_html()

    def to_html(self, *args) -> str:
        raise NotImplementedError(f"This element ({self.__class__.__name__}) does not support string conversion.")

    def to_md(self) -> str:
        raise NotImplementedError(f"This element ({self.__class__.__name__}) does not support Markdown conversion.")


class MDOnlyElement(Element):
    def to_html(self):
        raise ValueError("This element does not support HTML type!")


class PreformattedHTML(Element, str):
    """Preformatted HTML Element, you can use it when you're sure that the string contains a valid HTML formatting, and you don't want to escape it."""
    def to_md(self) -> str:
        return self

    def to_html(self) -> str:
        return self


class EscapedStr(Element):
    def __init__(self, item: SupportsStr | Element):
        self.item = item

    def to_md(self) -> str:
        # No escaping
        if isinstance(self.item, Element):
            return self.item.to_md()
        else:
            return str(self.item)

    def to_html(self) -> str:
        if isinstance(self.item, Element):
            return self.item.to_html()
        else:
            return html.escape(str(self.item), quote=False)


class Doc(Element, List[Element | SupportsStr]):
    # Contains child items
    # Also an abstract class for other arguments that contains child elements.

    def __init__(self, *items: Element | SupportsStr):
        super().__init__(item for item in items if item)

    def __iadd__(self, other: Element | SupportsStr):  # type: ignore
        self.append(other)
        return self

    def to_html(self) -> str:
        return '\n'.join(EscapedStr(item).to_html() for item in self)

    def to_md(self) -> str:
        return '\n'.join(EscapedStr(item).to_md() for item in self)

    def __repr__(self):
        return f'<{self.__class__.__name__}>({self})'
