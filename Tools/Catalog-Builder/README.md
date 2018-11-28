This directory will contain the Catalog-Builder, which will automatically generate the PSL Catalog by relying on PSL interoperability guidlines.

How to run this package
------------------------
1. Set-up environment
```
cd Tools/Catalog-Builder
pip install -r requirements.txt
pip install -e .
```

2. Run package

`python catalog_builder/catalog.py`

The results are written to the `PSL/Catalog` directory. The `Catalog/index.html` file contains a list of the projects and an overview of they do. A card for each project is written to the `PSL/Catalog` directory and named according to the project's name. These files can be viewed locally by opening them in the web browser. Most browsers have a "File" option in the menu bar that can be used to open a local HTML file.

How to run tests
------------------

`py.test tests/test_catalog.py`

How to add projects to the catalog
---------------------------------
1. Append the project to the [`register.json`](../../Catalog/register.json) file with the format:
```
{
    "org": the project's github organization name,
    "repo": the project's github repository name,
    "branch": master
}
```

Note: We can add support for other version control repositories upon request.

2. Create a `PSL_catalog.json` file according to the schema below

Catalog configuration file: `PSL_catalog.json`
-----------------------------------------------
The purpose of the project's `PSL_catalog.json` file is to help the catalog builder locate information about the project. This information will be stored in the PSL catalog and rendered on the project's PSL page. The basic layout of this file looks like this:

```
{
    'project_one_line': {
        'start_header': header signalling section start for pulling data
        'end_header': header signalling section to stop pulling data
        'type': 'github_file' or 'html', more can be added as necessary
        'data': null or HTML string to be displayed in section
        'source': information required to construct location of data
    },
    'project_overview' : {
        'start_header': ...
        'end_header': ...
        'type': ...
        'data': ...
        'source': ...
    },
    # other project attributes are listed out here
    ...
}
```

Currently, data for each project attribute can be specified on github or directly in the "data" attribute of the `PSL_catalog.json` file. If the data is specified on github, the attribute "type" should be set to "github_file." If the data is set directly in the `PSL_catalog.json` file, the "type" should be set to "html." Here are more in depth descriptions for how to fill out the catalog in both of these cases:

- "type" is "github_file"
  - "source" is the name of the file in the project's GitHub repository. It should be a markdown file.
  - "start_header" and "end_header" are the headers in the markdown file. Data between those headers will be parsed and rendered to HTML.
    - If neither header is specified, the entire document will be parsed.
    - If "start_header" is speecified and "end_header" is not specified, then data from "start_header" to the end of the file will be parsed.
    - If "end_header" is specified and "start_header" is not specified, then data from the beginning of the file to "end_header" is parsed.
    - If the parser cannot find these headers, then an error will be raised.
  - "data" is ignored in this case.
- "type" is "html"
  - The "data" attribute should be either a plain-text string or an HTML string.
  - "source" can optionally be set to a webpage where this data can be verified or more information about it can be found.
  - "start_header" and "end_header" are ignored in this case.

Attributes that MUST be included:
  - `project_one_line`: NA
  - `project_overview`: Project Overview,
  - `key_features`: Key Features
  - `citation`: Citation,
  - `license`: License,
  - `user_documentation`: User Documentation,
  - `user_changelog_recent`: User Changelog Recent,
  - `user_changelog`: User Changelog,
  - `dev_changelog`: Developer Changelog,
  - `disclaimer`: Disclaimer,
  - `user_case_studies`: User Case Studies,
  - `project_roadmap`: Project Roadmap,
  - `contributor_overview`: Contributor Overview,
  - `contributor_guide`: Contributor Guide,
  - `governance_overview`: Governance Overview,
  - `public_funding`: Public Funding,
  - `link_to_webapp`: Link to webapp,
  - `public_issue_tracker`: Public Issue Tracker,
  - `public_qanda`: Public Q & A
  - `core_maintainers`: Core Maintainers
  - `unit_test`: Unit Tests
  - `integration_test`: Integration Tests

See examples here:
- [`OG-USA/PSL_catalog.json`][]
- [`Tax-Calculator/PSL_catalog.json`][]




[`OG-USA/PSL_catalog.json`]: https://github.com/open-source-economics/OG-USA/blob/master/PSL_catalog.json
[`Tax-Calculator/PSL_catalog.json`]: https://github.com/open-source-economics/Tax-Calculator/blob/master/PSL_catalog.json
