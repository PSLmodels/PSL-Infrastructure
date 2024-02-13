import sys
import os
import re
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader(searchpath="./templates"),
    autoescape=select_autoescape(['html', 'xml'])
)

def extract_content(md_content):
    """Extracts the main heading from Markdown content."""
    lines = md_content.split('\n')
    heading_regex = re.compile(r'(?m)^(#{1,6} .+)$')
    if lines and lines[0].startswith('# '):
        # Assuming the first line is the main heading
        main_heading = lines[0]
        content = heading_regex.sub(r'<br/>\n\1', '\n'.join(lines[1:]))
    else:
        main_heading = ""
        content = md_content
    
    main_heading_html = markdown.markdown(main_heading, extensions=['tables'])
    content_html = markdown.markdown(content, extensions=['tables'])
    return main_heading_html, content_html

def convert_markdown_to_html(md_file_path):
    """Converts a Markdown file to HTML, extracting the main heading."""
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    return extract_content(md_content)

def render_html_page(main_heading_html, content_html, output_path):
    """Renders the final HTML page using Jinja2"""
    template = env.get_template('template.html')
    rendered_html = template.render(main_heading=main_heading_html, content=content_html)
    with open(output_path, 'w', encoding='utf-8') as html_file:
        html_file.write(rendered_html)

def main(markdown_path, output_path):
    main_heading_html, content_html = convert_markdown_to_html(markdown_path)
    render_html_page(main_heading_html, content_html, output_path)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <markdown_path> <output_html_path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])