import json
import os

import requests
from jinja2 import Template


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read_url(url):
    """
    Assume url leads to some a link providing raw catalogue JSON payload
    """
    pass


def read_filepath(path):
    assert os.path.exists(path)
    print(f'reading {path}')
    with open(path, 'r') as f:
        cat = json.loads(f.read())
    return cat


def get_data_from_project(location, is_url=True):
    if is_url:
        return read_url(location)
    else:
        return read_filepath(location)


def load_catalogue():
    # will swap out file paths for urls in the future. however, this
    # functionality will be helpful for testing new catalogue entries

    rel_path = os.path.join(CURRENT_PATH, '../../../Catalog/Projects/')
    locations = {
        'Tax-Calcualtor': os.path.join(rel_path, 
                                       'Tax-Calculator/catalogue.json'),
    }
    catalogue = {}
    for name, location in locations.items():
        catalogue[name] = get_data_from_project(location, False)
    return catalogue


def write_html(catalogue):
    models_path = os.path.join(CURRENT_PATH, 'models_template.html')
    model_path = os.path.join(CURRENT_PATH, 'model_template.html')
    
    with open(models_path, 'r') as f:
        models_string = f.read()
    models_template = Template(models_string)
    models_rendered = models_template.render(catalogue=catalogue)
    pathout = os.path.join(CURRENT_PATH, '../Web/pages/models.html')
    with open(pathout, 'w') as out:
        out.write(models_rendered)

    for _, project in catalogue.items():
        with open(model_path, 'r') as f:
            model_string = f.read()
        model_template = Template(model_string)
        model_rendered = model_template.render(project=project)
        pathout = os.path.join(CURRENT_PATH, 
                               f"../Web/pages/projects/{project['name']['value']}.html")
        with open(pathout, 'w') as out:
            out.write(model_rendered)



if __name__ == '__main__':
    catalogue = load_catalogue()
    write_html(catalogue)