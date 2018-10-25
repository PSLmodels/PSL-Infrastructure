import os
import pytest
import json
import filecmp
from page_builder import pagebuilder


@pytest.fixture(scope='session')
def test_path():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def pages_json(test_path):
    file_path = os.path.join(test_path, 'TestFiles/pages.json')
    with open(file_path) as f:
        return json.load(f)


@pytest.fixture(scope='session')
def cmp_file(test_path):
    return os.path.join(test_path, 'TestFiles/testpage.html')


def test_page_builder(test_path, pages_json, cmp_file):
    pb = pagebuilder.PageBuilder(pages_json)
    pb.build_pages()
    # assert that a file was rendered and saved
    assert os.path.isfile('testpage.html')
    # assert the file was rendered correctly
    assert filecmp.cmp('testpage.html', cmp_file)
    os.remove('testpage.html')


def test_incomplete_json():
    """
    Ensure a page entry that is missing required content raises an error
    """
    incomplete_dict = {
        "Bad Page": {
            "template": None,
            "content": "content/bad.md"
        }
    }
    pb = pagebuilder.PageBuilder(incomplete_dict)
    with pytest.raises(AssertionError):
        pb.build_pages()
