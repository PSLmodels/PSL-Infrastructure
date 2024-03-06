import base64
import json
import markdown
import requests
import time
from bs4 import BeautifulSoup
from jinja2 import Template

import re

# headers for requests to GitHub API
HEADER = {'User-Agent': 'request'}


class SectionHeadersDoNotExist(Exception):
    pass


class URLFormatError(Exception):
    pass


def pre_parser(text):
    """
    Convert Github-Flavored markdown to Python markdown
    for catalog builder to render text correctly

    Namely, 1) add extra line before bullet points and
    2) use four spaces instead of two to signal a sub-bullet point
    3) add indent to signal third-tier bullet point

    """
    doc_list = text.splitlines()

    list_edit = doc_list

    counter = -1

    for line in doc_list:
        counter += 1
        if line.startswith("* ") or line.startswith("- "):
            list_edit[counter - 1] = doc_list[counter - 1] + '\n'
        elif line.startswith("  *") or line.startswith("  -"):
            list_edit[counter] = "  " + doc_list[counter]
        elif line.startswith("    *") or line.startswith("    -"):
            list_edit[counter] = '\t' + doc_list[counter]

    string_edit = "\n".join(list_edit)

    return string_edit


def parse_section(doc, section_start, section_end):
    """
    Parse section of Markdown text from `section_start` to `section_end`.
    - If `section_start` is `None`, then the document is parsed form the
      beginning to the `section_end` header.
    - If `section_end` is `None`, then the entire document is parsed until
        `section_end` is found.

    Note:
    ------
    If the `SectionHeadersDoNotExist` Exception is raised, check to make sure
    the correct tag is compiled into the regex expression used in the
    `soup.find_all` call.


    returns:
    --------
    HTML that was rendered from Markdown
    """
    doc = doc.replace("#.#.#", r"\#.\#.\#")
    doc = pre_parser(doc)
    html = markdown.markdown(doc)
    html = html.replace('h2>', 'h5>')
    if section_start is None:
        get_next = True
    else:
        get_next = False
    data = []
    for line in html.split("\n"):
        linesoup = BeautifulSoup(line, "html.parser")
        text = linesoup.text
        # set to -1 since section_start and section_end can be None
        text = text.strip() if text is not None else -1
        if section_start == text:
            get_next = True
            continue
        if get_next:
            if section_end != text:
                data.append(line)
            else:
                break
    if len(data) == 0:
        raise SectionHeadersDoNotExist(
            f"{section_start} and/or {section_end} was not found."
        )
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
    template.globals["make_id"] = make_id
    template.globals["make_links"] = make_links
    template.globals["parse_core_maintainers"] = parse_core_maintainers
    template.environment.filters['split'] = split_filter
    return template.render(**render_kwargs)


def _get_from_github_api(org, repo, branch, filename):
    """
    Read data from github api. Ht to @andersonfrailey for decoding the response
    """
    # TODO: incorporate master branch
    if "http" in filename:
        raise URLFormatError(
            "A URL was entered for a 'github_file' type attribute. "
            "For more information, check out the catalog configuration "
            "docs: Tools/Catalog-Builder/README.md"
        )
    url = f"https://api.github.com/repos/{org}/{
        repo}/contents/{filename}?ref={branch}"
    response = requests.request('GET', url, headers=HEADER)
    print(f"GET: {url} {response.status_code}")
    if response.status_code == 403:
        time.sleep(60.5)
        response = requests.request('GET', url, headers=HEADER)
        print(f"Second try at GET: {url} {response.status_code}")
        if response.status_code == 403:
            # if waiting a minute doesn't work, then we're probably rate limited
            assert "hit rate limit" == 403
    assert response.status_code == 200
    sanatized_content = response.json()["content"].replace("\n", "")
    encoded_content = sanatized_content.encode()
    decoded_bytes = base64.decodebytes(encoded_content)
    text = decoded_bytes.decode()
    return text


def get_from_github_api(project, config):
    text = _get_from_github_api(
        project["org"], project["repo"], project["branch"], config["source"]
    )
    return parse_section(text, config["start_header"], config["end_header"])


def make_id(name):
    name = name.replace('.', '')
    return "-".join(name.split())


def split_filter(s, delimiter=None):
    return s.split(delimiter)


def parse_core_maintainers(html_content):
    maintainers = []
    email_pattern = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    soup = BeautifulSoup(html_content, 'html.parser')

    for item in soup.find_all('ul', recursive=False):
        for elem in item.children:
            if elem.name == 'li':
                maintainer = {'name': '', 'link': None}

                if elem.find('a'):
                    anchor = elem.find('a')
                    maintainer['name'] = anchor.get_text(strip=True)
                    maintainer['link'] = anchor.get('href')
                else:
                    text = elem.get_text(strip=True).split('\n')[0]
                    maintainer['name'] = text

                    sibling = elem.next_sibling
                    if sibling and sibling.name == 'ul':
                        nested_text = sibling.get_text(strip=True)
                        email_match = email_pattern.search(nested_text)
                        if email_match:
                            email = email_match.group()
                            maintainer['link'] = f'mailto:{email}'

                if maintainer['name']:
                    maintainers.append(maintainer)

    return maintainers


def make_links(item):
    """
    Returns either an HTML link or an empty string
    """
    def is_html_link(value):
        return value.startswith("<a") and value.endswith("/a>")

    def create_link(info, section_name):
        link_str = "<a class=\"button\" href=\"{}\">{}</a>"
        if info["source"]:
            if info["source"].startswith("http"):
                return link_str.format(info["source"], section_name)
        elif info["value"]:
            if is_html_link(info["value"]):
                linesoup = BeautifulSoup(info["value"], "html.parser")
                a = linesoup.find('a')
                href = a.attrs["href"]
                return link_str.format(href, section_name)
        else:
            return ""

    # list of sections to create links for
    sections = [("user_documentation", "User documentation"),
                ("contributor_overview", "Contributor documentation"),
                ("user_changelog_recent", "Recent changes"),
                ("link_to_webapp", "Link to webapp")]
    links = ""
    for key, section_name in sections:
        try:
            links += create_link(item[key], section_name)
        except:
            pass
    return links
