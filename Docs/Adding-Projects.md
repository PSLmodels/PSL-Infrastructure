# Adding Projects to the Catalog

This guide outlines the steps to add a project to either the main catalog or the incubating catalog.

## Main Catalog

### Step 1: Update the Register

Navigate to the `./Catalog/register.json` file and add a new entry for the repository. Use the following format:

```json
{
  "org": "GitHubOrgOrUsername",
  "repo": "RepositoryName",
  "branch": "master or specific branch name"
}
```

Replace `GitHubOrgOrUsername`, `RepositoryName`, and `main or specific branch name` with the appropriate values for the project.

### Step 2: Add `PSL_catalog.json` to the Project's Repository

Ensure that the repository has a file named `PSL_catalog.json` in its root directory. The file should follow this format:

```json
{
  "name": "Project name",
  "img": "Project logo URL",
  "banner_title": "Banner title for the Project",
  "banner_subtitle": "A short description or subtitle for the banner.",
  "detailed_description": "A detailed description of the project...",
  "policy_area": "Policy Reform, Tax Analysis, etc.",
  "geography": "Applicable geographic regions",
  "language": "Programming language(s) used",
  "maintainers": [
    {
      "name": "Maintainer's Name",
      "image": "Maintainer's Image URL",
      "link": "Maintainer's Contact Link"
    }
  ],
  "links": {
    "code_repository": "URL to the code repository",
    "user_documentation": "URL to the user documentation",
    "contributor_documentation": "URL to the contributor documentation",
    "webapp": "URL to any associated web application",
    "recent_changes": "URL to the changelog or recent changes"
  }
}
```

Fill in each field with the relevant information about the project. Note, values for `policy_area`, `geography`, and `language` should take the format of a comma-separated list.

### Step 3: Trigger the GitHub Action

The website will be updated with the new pages when the GitHub action is triggered, either on the daily schedule or manually.

## Incubating Catalog

The process for adding projects to the incubating catalog is similar:

### Step 1: Update the Incubating Register

Navigate to the `./Incubating/register.json` file and add the project using the same format as for the main catalog.

### Step 2: Add `PSL_catalog.json` to the Incubating Project's Repository

Ensure the project's repository contains `PSL_catalog.json` with the necessary information, following the same structure as outlined above.

### Step 3: Trigger the GitHub Action

As with the main catalog, the incubating catalog will be updated upon triggering the GitHub action.
