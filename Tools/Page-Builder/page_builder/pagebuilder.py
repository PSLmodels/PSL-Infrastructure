import markdown
import json
from bs4 import BeautifulSoup
from jinja2 import Template


class PageBuilder():
    """
    Receives a path to a JSON file containing metadata for a list of web pages
    to be built. The metadata contains information on where the final HTML
    file should be saved, which HTML template to use, and where the markdown
    content for that page can be found.

    Page metadata schema:
    {
        'Page Title': {
            'template': either a path to the HTML template or null. If null,
                        defaults to '../templates/page_template.html',
            'content': path to a markdown file with the content to be rendered
                       to HTML,
            'pathout': path to where the final file should be saved
        }
    }
    """
    def __init__(self, pages):
        """
        This class is used to create generic web pages for PSL
        Parameters
        ----------
        pages: dictionary containing information on all the pages to be created
        Returns
        -------
        None
        """
        self.pages = pages
        self.required_attributes = {'template', 'content', 'pathout'}

    def build_pages(self):
        """
        Method to loop through all pages in JSON metadata and output rendered
        HTML files
        """
        for page in self.pages:
            attributes = set(self.pages[page].keys())
            assert self.required_attributes.issubset(attributes)
            title = page
            pathout = self.pages[page]['pathout']
            content = self.pages[page]['content']
            template = self.pages[page]['template']
            # use default template if template is null
            if not template:
                template = '../templates/page_template.html'

            # read and convert markdown content to HTML
            with open(content, 'r') as f:
                md_text = f.read()
            if page == "Homepage":
                html_text = markdown.markdown(md_text)
                soup = BeautifulSoup(html_text, 'lxml')
                html_text = soup.p
            else:
                html_text = markdown.markdown(md_text)
            self.write_page(pathout, template,
                            title=title, content=html_text)

    def write_page(self, pathout, template_path, **kwargs):
        """
        Render the HTML template with the markdown text
        Parameters
        ----------
        pathout: path where the HTML file will be saved
        template_path: path for the HTML template
        Returns
        -------
        None
        """
        # read and render HTML template
        with open(template_path, "r") as f:
            template_str = f.read()
        template = Template(template_str)
        rendered = template.render(**kwargs)
        with open(pathout, 'w') as out:
            out.write(rendered)


if __name__ == '__main__':
    with open('pages.json') as f:
        pages = json.load(f)
    pb = PageBuilder(pages)
    pb.build_pages()
