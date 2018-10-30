import base64
import json

import markdown
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

import re


class SectionHeadersDoNotExist(Exception):
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
    doc = doc.replace("#.#.#", "\#.\#.\#")
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
    return template.render(**render_kwargs)


def _get_from_github_api(org, repo, branch, filename):
    """
    Read data from github api. Ht to @andersonfrailey for decoding the response
    """
    # TODO: incorporate master branch
    url = f"https://api.github.com/repos/{org}/{repo}/contents/{filename}?ref={branch}"
    response = requests.get(url)
    print(f"GET: {url} {response.status_code}")
    assert response.status_code == 200
    if response.status_code == 403:
        assert "hit rate limit" == 403
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


namemap = {
    "key_features": "Key Features",
    "project_overview": "Project Overview",
    "citation": "Citation",
    "license": "License",
    "user_documentation": "User Documentation",
    "user_changelog_recent": "User Changelog Recent",
    "user_changelog": "User Changelog",
    "dev_changelog": "Developer Changelog",
    "disclaimer": "Disclaimer",
    "user_case_studies": "User Case Studies",
    "project_roadmap": "Project Roadmap",
    "core_maintainers": "Core Maintainers",
    "contributor_overview": "Contributor Overview",
    "contributor_guide": "Contributor Guide",
    "unit_test": "Unit Tests",
    "integration_test": "Integration Tests",
    "governance_overview": "Governance Overview",
    "public_funding": "Public Funding",
    "link_to_webapp": "Link to webapp",
    "public_issue_tracker": "Public Issue Tracker",
    "public_qanda": "Public Q & A",
}
