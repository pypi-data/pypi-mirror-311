from stfu_tg.doc import MDOnlyElement


class HRuler(MDOnlyElement):
    def to_md(self) -> str:
        return '---'
