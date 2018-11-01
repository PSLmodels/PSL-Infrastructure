import os

import requests
import requests_mock
import pytest

from catalog_builder import catalog


@pytest.fixture
def current_path():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def pages_dir(tmpdir_factory):
    """
    A temporary directory to write catalog output files to. This simulates
    writing the files without cluttering up the production files or having to
    setup/teardown our own tempfiles. This directory is available for
    the entire session. A unique directory is provided each session.

    returns: name of the path for the directory
    """
    tmpdir_factory.mktemp("Catalog", numbered=False)
    return tmpdir_factory.getbasetemp()


@pytest.fixture
def mock_markdown_doc(current_path):
    mpath = os.path.join(current_path, "markdown.md")
    with open(mpath, "r") as f:
        text = f.read()
    return text


@pytest.fixture
def mock_catalog_meta(current_path):
    mpath = os.path.join(current_path, "TestProject", "PSL_catalog.json")
    with open(mpath, "r") as f:
        text = f.read()
    return text


@pytest.fixture
def mock_gh_api(mock_markdown_doc, mock_catalog_meta, monkeypatch):
    """
    Mock out `utils._get_from_github_api`. I would rather create mock response
    data than mock out the `_get_from_github_api` but the structure of the
    response is so convoluted that I'm not even going to try.
    """

    def _gh_api(org, repo, branch, filename):
        url = f"https://api.github.com/repos/{org}/{repo}/contents/{filename}?ref={branch}"
        response = requests.get(url)
        return response.text

    monkeypatch.setattr(catalog.utils, "_get_from_github_api", _gh_api)
    with requests_mock.Mocker() as mock:
        url = "https://api.github.com/repos/noorg/TestProject/contents/markdown.md?ref=master"
        mock.get(url, text=mock_markdown_doc)
        url = "https://api.github.com/repos/noorg/TestProject/contents/PSL_catalog.json?ref=master"
        mock.get(url, text=mock_catalog_meta)
        yield


@pytest.fixture
def cb(mock_gh_api, current_path, pages_dir):
    projects = [{"org": "noorg", "repo": "TestProject", "branch": "master"}]
    cb = catalog.CatalogBuilder(
        projects,
        index_dir=pages_dir,
        card_dir=os.path.join(pages_dir, 'Catalog')
    )
    cb.load_catalog()
    return cb


def test_load_catalog(mock_gh_api, current_path):
    projects = [{"org": "noorg", "repo": "TestProject", "branch": "master"}]
    cb = catalog.CatalogBuilder(
        projects,
        index_dir=current_path,
        card_dir=os.path.join(current_path, 'Catalog')
    )
    cb.load_catalog()
    assert cb.catalog
    assert "TestProject" in cb.catalog
    assert "project_overview" in cb.catalog["TestProject"]


def test_catalog_schema(cb):
    exp_keys = set(["source", "value"])
    for project in cb.catalog:
        for _, item in cb.catalog[project].items():
            assert set(item.keys()) == exp_keys


def test_catalog_write_html(cb):
    cb.write_pages()


def test_catalog_dumps(cb):
    assert cb.dump_catalog()


def test_catalog_on_real_data():
    cb = catalog.CatalogBuilder()
    # only do the first project
    cb.projects = [cb.projects[0]]
    cb.load_catalog()
    cb.write_pages()
    cb.dump_catalog()
