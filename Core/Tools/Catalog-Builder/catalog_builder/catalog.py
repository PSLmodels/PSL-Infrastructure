import json
import os
from collections import defaultdict

import requests
import markdown
from bs4 import BeautifulSoup
from jinja2 import Template


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
        if get_next and node.text != section_end:
            data.append(str(node))
        else:
            get_next = False
    return ' '.join(data)


class CatalogBuilder:
    """
    Receives list of projects and an optional directory indicating where to look
    for the project metadata. This metadata tells the parser where to look
    for the data to be gathered and written to the catalog. Once the data
    has been gathered, it is saved in a `catalog` attribute. This data is
    dumped into a JSON file `catalog.json` and into HTML templates to be
    served on the web.

    Catalog schema:

    {
        'project1': {
            'attribute1': {
                'value': html data,
                'source': link where HTML was gathered
            },
            'attribute2': {
                ...
            },
            ...
        },
        'project2': {
            'attribute1': {
                ...
            }
            ...
        }
    }
    """

    CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, projects, project_dir=None, pages_dir=None):
        self.projects = projects
        self.project_dir = (
            project_dir or
            os.path.join(self.CURRENT_PATH, '../../../../Catalog/Projects/'))
        self.pages_dir = (
            pages_dir or os.path.join(self.CURRENT_PATH, '../../Web/pages/'))

        self.catalog = defaultdict(dict)

    def load_catalog(self):
        """
        Read meta data from `project_dir` and collect the specified data
        accordingly. The data is retrieved using the raw GitHub links and
        parsed via the `parse_section` function. The parsed data is saved
        to the `catalog` attribute.
        """
        for p in self.projects:
            url_base = (f"https://raw.githubusercontent.com/"
                        f"{p['org']}/{p['repo']}/{p['branch']}/")
            cat_meta = os.path.join(self.project_dir, p['repo'],
                                    'catalog.json')
            with open(cat_meta, 'r') as f:
                cat_meta = json.loads(f.read())
            self.catalog[p['repo']]['name'] = {'value': p['repo'],
                                                 'source': ''}
            for k, v in cat_meta.items():
                url = os.path.join(url_base,
                                   v['from_file'])
                resp = requests.get(url)
                data = parse_section(resp.text, v['start_header'],
                                     v['end_header'])
                res = {'source': url, 'value': data}
                self.catalog[p['repo']][k] = res

    def write_html(self):
        """
        Write HTML from the `catalog` attribute to template files.

        models_template.html is the template for the /models.html page.
        model_template.html is the template for the
            /projects/{project name}.html page.

        Data is written to the `Web/pages` directory
        """
        models_path = os.path.join(self.CURRENT_PATH, '../templates',
                                   'models_template.html')
        model_path = os.path.join(self.CURRENT_PATH, '../templates',
                                  'model_template.html')

        rendered = self.render_template(models_path, catalog=self.catalog)
        pathout = os.path.join(self.pages_dir, 'models.html')
        with open(pathout, 'w') as out:
            out.write(rendered)

        for _, project in self.catalog.items():
            rendered = self.render_template(model_path, project=project)
            pathout = os.path.join(
                self.pages_dir,
                f"projects/{project['name']['value']}.html")
            with open(pathout, 'w') as out:
                out.write(rendered)

    def render_template(self, template_path, **render_kwargs):
        """
        Helper method to render the template file and context.

        returns:
        --------
        rendered html
        """
        with open(template_path, 'r') as f:
            template_str = f.read()
        template = Template(template_str)
        return template.render(**render_kwargs)

    def dump_catalog(self, output_path=None):
        """
        Dumps `catalog` attribute to string. Optionally writes to the
        `output_file` location if provided.

        returns:
        --------
        cat_str: JSON representation of `catalog` attribute
        """
        cat_json = json.dumps(self.catalog)
        if output_path is not None:
            with open(output_path, 'w') as f:
                f.write(cat_json)
        return cat_json

if __name__ == '__main__':
    projects = [
        {'org': 'open-source-economics',
         'repo': 'Tax-Calculator',
         'branch': 'master'}
    ]
    cb = CatalogBuilder(projects)
    cb.load_catalog()
    cb.write_html()
    cb.dump_catalog(os.path.join(cb.project_dir, 'catalog.json'))