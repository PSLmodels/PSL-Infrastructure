import markdown
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

import re


class SectionHeadersDoNotExist(Exception):
    pass


def parse_section(doc, section_start, section_end):
    """
    Parse section of Markdown text from `section_start` to `section_end`.
    - If `section_start` is `None`, then the document is parsed form the
      beginning to the `section_end` header.
    - If `section_end` is `None`, then the entire document is parsed until
        `section_end` is found.

    Note: there's a case for parsing until `section_end` if `section_start` is
        not specified but `section_end` is.

    returns:
    --------
    HTML that was rendered from Markdown
    """
    doc = doc.replace("#.#.#", "\#.\#.\#")
    html = markdown.markdown(doc)
    if section_start is None:
        get_next = True
    else:
        get_next = False
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for node in soup.find_all(re.compile("p|h[1-6]")):
        if node.text == section_start:
            get_next = True
            continue
        if get_next:
            if section_end is None:
                data.append(str(node))
            elif section_end not in node.text:
                data.append(str(node))
            else:
                break
    if len(data) == 0:
        raise SectionHeadersDoNotExist(
            f"{section_start} and/or {section_end} was not found."
        )
    print(data)
    return " ".join(data)


def render_template(template_path, **render_kwargs):
    """
    Helper method to render the template file and context.

    returns:
    --------
    rendered html
    """
    with open(template_path, "r") as f:
        template_str = f.read()
    template = Template(template_str)
    return template.render(**render_kwargs)


def data_from_url(url, start_header, end_header):
    resp = requests.get(url)
    text = resp.text
    return parse_section(text, start_header, end_header)
