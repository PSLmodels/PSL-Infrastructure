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