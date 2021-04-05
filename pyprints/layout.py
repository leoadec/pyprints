from dataclasses import dataclass

@dataclass
class TextType:
    is_numbered = False

class Layout:
    def body_wrapper(self, text, title=None):
        raise NotImplementedError

    def section_wrapper(self, text, section_name, section_level):
        raise NotImplementedError

    def render(self, text):
        raise NotImplementedError


class HtmlLayout(Layout):
    style_sheet = None

    def __init__(self, style_sheet=None):
        self._style_sheet = style_sheet

    def body_wrapper(self, text, title=None):
        doctype = "<!DOCTYPE html>"
        css = (
            f"<style>\n{self.style_sheet}\n</style>\n"
            if self.style_sheet is not None else ""
        )
        head_title = "" if title is None else f"<title>{title}</title>\n"
        body_title = "" if title is None else f"<h1>{title}</h1>\n"
        text = body_title + text
        head = f'<head>\n<meta charset="utf-8">\n{head_title}{css}</head>'
        return f"{doctype}\n<html>\n{head}\n<body>\n{text}\n</body>\n</html>"

    def section_wrapper(self, text, section_name, section_level):
        header = f"<h{section_level+1}>{section_name}</h{section_level+1}>"
        return f"{header}\n{text}"

    def list_wrapper(self, items):
        return_string = ""
        for item in items:
            return_string += f"{item}\n"
        return return_string[:-1]

    def render(self, text):
        return f"<p>{text}</p>"
