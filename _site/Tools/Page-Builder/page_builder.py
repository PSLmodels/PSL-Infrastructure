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
    """Extracts the main heading and the first line following the main heading from Markdown content, and inserts <br> tags between sections."""
    lines = md_content.split('\n')
    processed_lines = []
    
    if lines:
        main_heading = lines[0] if lines[0].startswith('# ') else ""
        first_line_index = 1
        
        # Find the first non-empty line after the main heading
        while first_line_index < len(lines) and not lines[first_line_index].strip():
            first_line_index += 1
        first_line = lines[first_line_index] if first_line_index < len(lines) else ""
        
        # Process lines to insert <br> before section headings
        for i, line in enumerate(lines[first_line_index+1:], start=first_line_index+1):
            if line.startswith('#') and i > first_line_index+2:
                processed_lines.append('<br>')
            processed_lines.append(line)
        
        content = '\n'.join(processed_lines)
    else:
        main_heading = ""
        first_line = ""
        content = md_content

    # Convert Markdown to HTML
    main_heading_html = markdown.markdown(main_heading, extensions=['tables'])
    first_line_html = f'<h5>{first_line}</h5>' if first_line else ""
    content_html = markdown.markdown(content, extensions=['tables'])

    return main_heading_html, first_line_html, content_html


def convert_markdown_to_html(md_file_path):
    """Converts a Markdown file to HTML, extracting the main heading."""
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    return extract_content(md_content)


def render_html_page(main_heading_html, first_line_html, content_html, output_path):
    """Renders the final HTML page using Jinja2"""
    template = env.get_template('template.html')
    rendered_html = template.render(
        main_heading=main_heading_html, 
        first_line=first_line_html,
        content=content_html)
    with open(output_path, 'w', encoding='utf-8') as html_file:
        html_file.write(rendered_html)


def main(markdown_path, output_path):
    main_heading_html, first_line_html, content_html = convert_markdown_to_html(markdown_path)
    render_html_page(main_heading_html, first_line_html, content_html, output_path)
    print(f"Generated {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <markdown_path> <output_html_path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
