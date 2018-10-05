import json
import os
from collections import defaultdict

from catalog_builder import utils


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
        self.project_dir = project_dir or os.path.join(
            self.CURRENT_PATH, "../../../../Catalog/Projects/"
        )
        self.pages_dir = pages_dir or os.path.join(
            self.CURRENT_PATH, "../../Web/pages/"
        )

        self.catalog = defaultdict(dict)

    def load_catalog(self):
        """
        Read meta data from `project_dir` and collect the specified data
        accordingly. The data is retrieved using the raw GitHub links and
        parsed via the `parse_section` function. The parsed data is saved
        to the `catalog` attribute.
        """
        for p in self.projects:
            cat_meta = os.path.join(
                self.project_dir, p["repo"], "catalog.json"
            )
            with open(cat_meta, "r") as f:
                cat_meta = json.loads(f.read())
            self.catalog[p["repo"]]["name"] = {
                "value": p["repo"],
                "source": "",
            }
            for k, v in cat_meta.items():
                if v["type"] == "github_file":
                    url_base = (
                        f"https://raw.githubusercontent.com/"
                        f"{p['org']}/{p['repo']}/{p['branch']}/"
                    )
                    source = os.path.join(url_base, v["source"])
                    value = utils.data_from_url(
                        source, v["start_header"], v["end_header"]
                    )
                elif v["type"] == "url":
                    source = v["source"]
                    value = utils.data_from_url(
                        source, v["start_header"], v["end_header"]
                    )
                elif v["data"] is not None:
                    source = None
                    value = v["data"]
                else:
                    print(f"No data specified for project, entry: {p}, {k}")
                    source, value = None, None
                res = {"source": source, "value": value}
                self.catalog[p["repo"]][k] = res

    def write_html(self):
        """
        Write HTML from the `catalog` attribute to template files.

        models_template.html is the template for the /models.html page.
        model_template.html is the template for the
            /projects/{project name}.html page.

        Data is written to the `Web/pages` directory
        """
        models_path = os.path.join(
            self.CURRENT_PATH, "../templates", "models_template.html"
        )
        model_path = os.path.join(
            self.CURRENT_PATH, "../templates", "model_template.html"
        )

        rendered = utils.render_template(models_path, catalog=self.catalog)
        pathout = os.path.join(self.pages_dir, "models.html")
        with open(pathout, "w") as out:
            out.write(rendered)

        for _, project in self.catalog.items():
            rendered = utils.render_template(model_path, project=project)
            pathout = os.path.join(
                self.pages_dir, f"projects/{project['name']['value']}.html"
            )
            with open(pathout, "w") as out:
                out.write(rendered)

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
            with open(output_path, "w") as f:
                f.write(cat_json)
        return cat_json


if __name__ == "__main__":
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
    cb.dump_catalog(os.path.join(cb.project_dir, "catalog.json"))
