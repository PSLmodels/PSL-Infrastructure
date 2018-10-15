import markdown
import utils


def write_page(md_path, template_path, pathout):
    """
    """
    with open(md_path, 'r') as f:
        md_txt = f.read()
    html = markdown.markdown(md_txt)
    rendered = utils.render_template(template_path, md_txt=html)
    with open(pathout, 'w') as out:
        out.write(rendered)


def main():
    # path to folder with all of the final files
    pathout_base = '../../Web/pages/{}.html'
    # list of the pages created by this script
    pages = ['about', 'criteria']

    # paths to markdown files to render
    md_path_about = '../../../../README.md'
    md_path_criteria = '../../../Criteria/library_criteria.md'
    md_paths = [md_path_about, md_path_criteria]

    for page, md_path in zip(pages, md_paths):
        pathout = pathout_base.format(page)
        template_path = f'../templates/{page}_template.html'
        write_page(md_path, template_path, pathout)


if __name__ == '__main__':
    main()
