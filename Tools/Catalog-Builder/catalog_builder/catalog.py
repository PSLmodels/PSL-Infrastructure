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

    Catalog configuration file (PSL_catalog.json) schema:

    {
        'attribute': {
            'start_header': header signalling section start for pulling data
            'end_header': header signalling section to stop pulling data
            'type': 'github_file' or 'html', more can be added as necessary
            'data': null or HTML string to be displayed in section
            'source': information required to construct location of data
        }
    }
        Allowed attributes:
            - project_one_line: NA
            - key_features: Key Features,
            - project_overview: Project Overview,
            - citation: Citation,
            - license: License,
            - user_documentation: User Documentation,
            - user_changelog_recent: User Changelog Recent,
            - user_changelog: User Changelog,
            - dev_changelog: Developer Changelog,
            - disclaimer: Disclaimer,
            - user_case_studies: User Case Studies,
            - project_roadmap: Project Roadmap,
            - contributor_overview: Contributor Overview,
            - contributor_guide: Contributor Guide,
            - governance_overview: Governance Overview,
            - public_funding: Public Funding,
            - link_to_webapp: Link to webapp,
            - public_issue_tracker: Public Issue Tracker,
            - public_qanda: Public Q & A

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

    def __init__(self, projects=None, index_dir=None, card_dir=None):
        if projects is None:
            p = os.path.join(
                self.CURRENT_PATH, "../register.json"
            )
            with open(p, "r") as f:
                self.projects = json.loads(f.read())
        else:
            self.projects = projects

        self.index_dir = index_dir or os.path.join(
            self.CURRENT_PATH, "../../../Catalog/"
        )

        self.card_dir = card_dir or os.path.join(
            self.CURRENT_PATH, "../../../Catalog/"
        )

        self.catalog = defaultdict(dict)

    def load_catalog(self):
        """
        Read meta data from `project_dir` and collect the specified data
        accordingly. The data is retrieved using the raw GitHub links and
        parsed via the `parse_section` function. The parsed data is saved
        to the `catalog` attribute.
        """
        for project in sorted(self.projects, key=lambda x: x['repo']):
            cat_meta = utils._get_from_github_api(
                project["org"],
                project["repo"],
                project["branch"],
                "PSL_catalog.json",
            )
            cat_meta = json.loads(cat_meta)
            self.catalog[project["repo"]]["name"] = {
                "value": project["repo"],
                "source": "",
            }
            for attr, config in cat_meta.items():
                if config["type"] == "github_file":
                    value = utils.get_from_github_api(project, config)
                    source = (
                        f"https://github.com/{project['org']}/"
                        f"{project['repo']}/blob/{project['branch']}/"
                        f"{config['source']}"
                    )

                elif config["type"] == "html":
                    source = config["source"]
                    value = config["data"]
                else:
                    msg = (
                        f"MISSING DATA: {project['repo']}, entry: "
                        f"{attr}, {config}"
                    )
                    print(msg)
                    source, value = None, None
                res = {"source": source, "value": value}
                self.catalog[project["repo"]][attr] = res

    def write_pages(self):
        """
        Write HTML from the `catalog` attribute to template files.

        models_template.html is the template for the /catalog.html page.
        model_template.html is the template for the
            /projects/{project name}.html page.

        Data is written to the `Web/pages` directory
        """
        models_path = os.path.join(
            self.CURRENT_PATH, "../templates", "catalog_template.html"
        )
        model_path = os.path.join(
            self.CURRENT_PATH, "../templates", "card_template.html"
        )

        rendered = utils.render_template(models_path, catalog=self.catalog)
        pathout = os.path.join(self.index_dir, "index.html")
        with open(pathout, "w") as out:
            out.write(rendered)

        for _, project in self.catalog.items():
            rendered = utils.render_template(
                model_path, project=project, namemap=utils.namemap
            )
            pathout = os.path.join(
                self.card_dir, f"{project['name']['value']}.html"
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
        cat_json = json.dumps(self.catalog, indent=4)
        if output_path is not None:
            with open(output_path, "w") as f:
                f.write(cat_json)
        return cat_json


if __name__ == "__main__":
    cb = CatalogBuilder()
    cb.load_catalog()
    cb.write_pages()
    cb.dump_catalog(os.path.join(cb.card_dir, "catalog.json"))
