import os

import requests_mock
import pytest

from catalogue_builder.catalogue import CatalogueBuilder


@pytest.fixture
def markdown_doc():
    current_path = os.path.abspath(os.path.dirname(__file__))
    mpath = os.path.join(current_path, 'markdown.md')
    with open(mpath, 'r') as f:
        text = f.read()
    return text


@pytest.fixture
def cb(markdown_doc):
    current_path = os.path.abspath(os.path.dirname(__file__))
    projects = [
        {'org': 'noorg', 'repo': 'TestProject', 'branch': 'master'},
    ]
    cb = CatalogueBuilder(projects, project_dir=current_path)
    with requests_mock.Mocker() as mock:
        url = ('https://raw.githubusercontent.com/noorg/'
                'TestProject/master/markdown.md')
        mock.get(url, text=markdown_doc)
        cb.load_catalogue()
    return cb


def test_load_catalogue(markdown_doc):
    current_path = os.path.abspath(os.path.dirname(__file__))
    projects = [
        {'org': 'noorg', 'repo': 'TestProject', 'branch': 'master'},
    ]
    cb = CatalogueBuilder(projects, project_dir=current_path)
    with requests_mock.Mocker() as mock:
        url = ('https://raw.githubusercontent.com/noorg/'
                'TestProject/master/markdown.md')
        mock.get(url, text=markdown_doc)
        cb.load_catalogue()

    assert cb.catalogue

    assert 'TestProject' in cb.catalogue
    assert 'project_overview' in cb.catalogue['TestProject']


def test_catalogue_schema(cb):
    exp_keys = set(['source', 'value'])
    for project in cb.catalogue:
        for _, item in cb.catalogue[project].items():
            assert set(item.keys()) == exp_keys


def test_catalogue_write_html(cb):
    cb.write_html()


def test_catalogue_dumps(cb):
    assert cb.dump_catalogue()


def test_catalogue_on_real_data():
    projects = [
        {'org': 'open-source-economics',
         'repo': 'Tax-Calculator',
         'branch': 'master'}
    ]
    cb = CatalogueBuilder(projects)
    cb.load_catalogue()
    cb.write_html()
    cb.dump_catalogue()