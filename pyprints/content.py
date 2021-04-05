from dataclasses import dataclass

@dataclass
class Paragraph:
    text: str

@dataclass
class Section:
    title: str
    section_parts: list

@dataclass 
class Content:
    title: str
    content_parts: list

def parse_content(content, filter=None):
    if filter is None:
        filter = lambda x: x

    if isinstance(content, dict) and (len(content) == 1):
        title, actual_content = list(content.items())[0]
    else:
        actual_content = content
        title = None

    return Content(
        content_parts=_parse_content_part(actual_content, filter),
        title=title,
    )


def _parse_content_part(content_part, filter):
    filtered_content =  filter(content_part)

    if isinstance(filtered_content, str):
        return Paragraph(filtered_content)
    if hasattr(filtered_content, "__init__"):
        if isinstance(filtered_content, dict):
            if all([hasattr(Paragraph, key) for key in filtered_content]):
                return Paragraph(**filtered_content)
            else:
                return [
                    Section(
                        title=key,
                        section_parts=_parse_content_part(value, filter)
                    )
                    for key, value in filtered_content.items()
                ]
        else:
            return [
                _parse_content_part(part, filter) for part in filtered_content
            ]
    return Paragraph(str(filtered_content))


def render_content(content, layout):
    starting_level = 1 if (content.title is not None) else 0
    body = _render_content_part(content.content_parts, layout, starting_level)
    return layout.body_wrapper(body, title=content.title)


def _render_content_part(content, layout, level):
    if isinstance(content, Paragraph):
        return layout.render(content.text)
    elif isinstance(content, Section):
        return layout.section_wrapper(
            _render_content_part(content.section_parts, layout, level+1),
            section_name=content.title,
            section_level=level,
        )
    elif isinstance(content, list):
        return layout.list_wrapper(
            [_render_content_part(part, layout, level) for part in content]
        )
    return layout.render(str(content))
