# Page Builder

This directory contains Page-Builder, which will automatically generate select
web pages for PSL.

## Running the package

```bash
cd Tools/Page-Builder/pagebuilder
python pagebuilder.py
```

## Run tests

```bash
pytest
```

## How to add pages to the project

To add a page, first append the page metadata to `pages.json` with the following
format:

```bash
{
    "Page Title": {
        "template": either a path to the HTML template the page will use or null. If null, defaults to "../templates/page_template.html",
        "content": path to a markdown file with the content that will fill the template,
        "pathout": path to where the final file should be saved
    }
}
```

All three of the attributes are required to be included in the JSON file.

In the HTML template, the only two currently available variables are `title` and `content`.
`title` refers to the title of the HTML document and will be set to whatever you use
as the page title in the JSON file. `content` refers to the actual content that will
be rendered in the HTML file. Ideally in the future we will be able to expand
the capabilities of this package to take an arbitrary number of variables and render
the template accordingly.