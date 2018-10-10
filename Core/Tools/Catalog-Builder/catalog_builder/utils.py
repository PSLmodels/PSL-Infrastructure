import base64
import json

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
    html = markdown.markdown(doc)
    if section_start is None:
        get_next = True
    else:
        get_next = False
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for node in soup.find_all(re.compile("p|h[1-6]|ul|li")):
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


def _get_from_github_api(org, repo, filename):
    """
    Read data from github api. Ht to @andersonfrailey for decoding the response
    """
    # TODO: incorporate master branch
    url = f"https://api.github.com/repos/{org}/{repo}/" f"contents/{filename}"
    response = requests.get(url)
    assert response.status_code == 200
    sanatized_content = response.json()["content"].replace("\n", "")
    encoded_content = sanatized_content.encode()
    decoded_bytes = base64.decodebytes(encoded_content)
    text = decoded_bytes.decode()
    return text


def get_from_github_api(project, config):
    try:
        text = _get_from_github_api(
            project["org"], project["repo"], config["source"]
        )
    except json.decoder.JSONDecodeError:
        text = response.text
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
    "contributor_overview": "Contributor Overview",
    "contributor_guide": "Contributor Guide",
    "governance_overview": "Governance Overview",
    "public_funding": "Public Funding",
    "link_to_webapp": "Link to webapp",
    "public_issue_tracker": "Public Issue Tracker",
    "public_qanda": "Public Q & A",
}
