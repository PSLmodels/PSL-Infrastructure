This directory will contain the Catalog-Builder, which will automatically generate the PSL Catalog by relying on PSL interoperability guidlines.

How to run this package
------------------------
1. Set-up environment
```
cd Core/Tools/Catalog-Builder
pip install -r requirements.txt
pip install -e .
```

2. Run package

`python catalog.py`

How to run tests
------------------

`py.test tests/test_catalog.py`

How to add projects to this repo
---------------------------------
1. Append the project to the [`register.json`](../../../Catalog/register.json) file with the format:
```
{
    "org": the project's github organization name,
    "repo": the project's github repository name,
    "branch": master
}
```

Note: We can add support for other version control repositories upon request.

2. Create a `psl-catalog.json` file with the following format:
```
{
    'attribute': {
        'start_header': header signalling section start for pulling data
        'end_header': header signalling section to stop pulling data
        'type': 'github_file' or 'html', more can be added as necessary
        'data': null or HTML string to be displayed in section
        'source': information required to construct location of data
    }
}
```

Different values should be set based on what type of data is being parsed:
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

Allowed attributes and their display names:
  - `project_one_line`: NA
  - `key_features`: Key Features,
  - `project_overview`: Project Overview,
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

See examples here:
- [`TestProject/psl_catalog.json`][]
- [`Tax-Calculator/psl_catalog.json`][]




[`TestProject/psl_catalog.json`]: catalog_builder/tests/TestProject/psl_catalog.json
[`Tax-Calculator/psl_catalog.json`]: https://github.com/hdoupe/Tax-Calculator/blob/psl-catalog/psl_catalog.json