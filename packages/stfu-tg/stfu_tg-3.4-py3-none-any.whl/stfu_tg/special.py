from stfu_tg.doc import Element


class InvisibleSymbol(Element, str):
    def __str__(self):
        return '&#8288;'


class Spacer(Element, str):
    def __str__(self):
        return ' '
