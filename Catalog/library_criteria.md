
# PSL Project Criteria

## Summary

1. Models must be transparent.
1. Models should adopt organizational and interface recommendations for community and interoperability.

## Introduction

Open-source modeling ensures that model results are reproducible, that experts around the world can collaborate to make models better, and that users can explore the parameter space for themselves. These outcomes systematically improve public policy decisionmaking.

We have developed the criteria in this document to facilitate the growth of an open source public policy modeling ecosystem.

## Mandatory Criteria for Transparency and Quality

Models must meet the following requirements for acceptance into the catalog:

1. Release under an OSI-approved open source license or the Creative Commons Public Domain Dedication (CC0).
1. Make data publicly available, unless release is restricted by a third party.
1. For any data that should not be disclosed, provide:
	- A complete descriptive list of all data variables;
	- Descriptive statistics for all data variables for such data (including averages, standard deviations, number of observations, and correlations to other variables), to the extent that the descriptive statistics do not violate the rule against disclosure;
	- Contact information for the individual or entity who has unrestricted access to the data.
1. Include unit tests and ensure that they sources code passes the tests.
1. For at least one test, generate key outputs from source materials; the test must be run with every new version, and the outputs of the test must be checked into the repository.
1. Report names and contact information for at least one maintainer.
1. Have a suggested citation.
1. Have a project overview.
1. Have installation instructions.
1. Version control in [github.com/PSLmodels](http://github.com/pslmodels), either as the primary location or as a mirror.
1. Adopt a consistent versioning scheme.
1. Include a `PSL_catalog.json` configuration file in the project's repository for cataloging these criteria. Specific instructions for creating this file can be found in the [Catalog-Builder Documentation](https://github.com/PSLmodels/PSL-Infrastructure/tree/master/Tools/Catalog-Builder#how-to-add-projects-to-the-catalog).


## Recommended Community Criteria

We also encourage, but do not require, projects to adopt the following practices:

1. Report code coverage.
1. Use [semantic versioning](https://semver.org/).
1. Display a public roadmap.
1. Display contributor documentation and guidelines.
1. Hold regular office hours, webinars, or standing meetings.
1. List technical contributors.
1. List funders.
1. List user citations and case studies.
1. Include subject matter repository topics.
1. Include a disclaimer.
1. Track issues publicly (e.g. on GitHub).
1. Show a changelog.
1. Be written in an open source language.
2. Add a "psl-cataloged" tag to the About section of the project's GitHub repository.
3. Follow a standard contributor workflow, such as [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow).
4. Include continuous integration tests to ensure that tests are passing for proposed changes in pull requests and to document publicly that all unit tests are passing.
5. Adopt a consistent code formatting scheme, perhaps through an automated code formatter like [Black](https://black.readthedocs.io/en/stable/).

## Optional Additional Practices

Projects may also consider the following:

1. Have a Stack Overflow channel.
1. Include a "News" translation of the changelog for users.
1. Include criteria for participating in cross-model PSL initiatives.
1. Include a link to a webapp version.
1. Include a list of consultants.
