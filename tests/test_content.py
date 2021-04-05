import pyprints

def test_render_content():
    layout = pyprints.HtmlLayout()

    raw_content = {"a": ["content", "more\ncontent", {"b": "extra", "c": "content"}]}

    parsed_content = pyprints.parse_content(raw_content)
    output = pyprints.render_content(parsed_content, layout)

    expected_output = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>a</title>
</head>
<body>
<h1>a</h1>
<p>content</p>
<p>more\ncontent</p>
<h2>b</h2>
<p>extra</p>
<h2>c</h2>
<p>content</p>
</body>
</html>"""

    assert isinstance(output, str)
    assert output == expected_output
