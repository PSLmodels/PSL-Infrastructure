import os

import requests_mock
import pytest

from catalog_builder.catalog import CatalogBuilder


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
    tmpdir_factory.mktemp("projects", numbered=False)
    return tmpdir_factory.getbasetemp()


@pytest.fixture
def markdown_doc():
    current_path = os.path.abspath(os.path.dirname(__file__))
    mpath = os.path.join(current_path, "markdown.md")
    with open(mpath, "r") as f:
        text = f.read()
    return text


@pytest.fixture
def cb(markdown_doc, current_path, pages_dir):
    projects = [{"org": "noorg", "repo": "TestProject", "branch": "master"}]
    cb = CatalogBuilder(
        projects, project_dir=current_path, pages_dir=pages_dir
    )
    with requests_mock.Mocker() as mock:
        url = (
            "https://raw.githubusercontent.com/noorg/"
            "TestProject/master/markdown.md"
        )
        mock.get(url, text=markdown_doc)
        cb.load_catalog()
    return cb


def test_load_catalog(markdown_doc, current_path):
    projects = [{"org": "noorg", "repo": "TestProject", "branch": "master"}]
    cb = CatalogBuilder(projects, project_dir=current_path)
    with requests_mock.Mocker() as mock:
        url = (
            "https://raw.githubusercontent.com/noorg/"
            "TestProject/master/markdown.md"
        )
        mock.get(url, text=markdown_doc)
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
    cb.write_html()


def test_catalog_dumps(cb):
    assert cb.dump_catalog()


def test_catalog_on_real_data():
    projects = [
        {
            "org": "open-source-economics",
            "repo": "Tax-Calculator",
            "branch": "master",
        }
    ]
    cb = CatalogBuilder(projects)
    cb.load_catalog()
    cb.write_html()
    cb.dump_catalog()
