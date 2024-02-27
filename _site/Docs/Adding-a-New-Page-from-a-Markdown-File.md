# Adding a New Page from a Markdown File

This guide outlines the steps to add a new page to the website by converting a markdown file into an HTML page and updating the navigation bar to include this new page.

## The Page Builder

The bash script `make_pages.sh` located in `./Tools/Page-Builder/` is used to automate the conversion of markdown files to HTML pages.

### Adding Your Page to the Script

1. Navigate to `./Tools/Page-Builder/`.

2. Edit `make_pages.sh`.

3. At the bottom of the script file, add the following line:

    ```bash
    py ./page_builder.py <path to your markdown file> <path for output HTML file>
    ```

    Replace `<path to your markdown file>` with the relative path to your markdown file and `<path for output HTML file>` with the desired output path for the HTML file.

## Add the Page to the Navbar

After adding your markdown file to the bash script, you'll need to add a link to this page in the website's navigation bar.

1. Navigate to `./layout/` and edit `navbar.html`.

2. Find the appropriate section where you want to add your new page link. If it's part of a dropdown menu, look for the corresponding `<div>` or `<ul>` tag.

3. Insert an `<a>` tag in the desired location with the following format:

    ```html
    <a class="dropdown-item" href="../<path to your HTML page>">
        Page Name
    </a>
    ```

    Replace `../<path to your HTML page>` with the relative path to your new HTML page and Page Name with the name you want to appear in the navbar.

4. After adding the new user, commit your changes and push them to the repository.

5. The website will automatically update with the new user's information either when the GitHub action is triggered manually or runs on its scheduled daily update.

