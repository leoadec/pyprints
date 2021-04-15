import pyprints

contents = pyprints.parse_api(pyprints)

layout = pyprints.HtmlLayout()

for name, content in contents.items():
    filename = f"docs/{name.replace(' ', '_')}.html"
    with open(filename, "w") as output_file:
        output_file.write(pyprints.render_content(content, layout))
