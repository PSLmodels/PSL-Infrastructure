import requests
import markdown
from bs4 import BeautifulSoup


def parse_section(doc, section_start, section_end):
    """
    Parse section of Markdown text from `section_start` to `section_end`.
    - If `section_start` is `None`, then the entire document is parsed to HTML
        and returned.
    - If `section_end` is `None`, then the entire document is parsed until
        `section_end` is found.

    Note: there's a case for parsing until `section_end` if `section_start` is
        not specified but `section_end` is.

    returns:
    --------
    HTML that was rendered from Markdown
    """
    doc = doc.replace('#.#.#', '\#.\#.\#')
    html = markdown.markdown(doc)
    if section_start is None:
        return html
    soup = BeautifulSoup(html, 'html.parser')
    get_next = False
    data = []
    for node in soup.find_all():
        if node.text == section_start:
            get_next = True
            continue
        if get_next and (section_end is None or section_end not in node.text):
            data.append(str(node))
        else:
            get_next = False
    return ' '.join(data)


def data_from_url(url, start_header, end_header):
    resp = requests.get(url)
    return parse_section(resp.text, start_header, end_header)
