from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import frontmatter
from datetime import date
import humanize
from pathlib import Path
import shutil, os
import markdown as md
from pygments.formatters import HtmlFormatter
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.wikilinks import WikiLinkExtension
"""
/posts/something.md  -> /BUILT/posts/something.html (rendered)
/includes/x.css -> /BUILT/includes/x.css (copied)
/templates/x.html -> /BUILT/pages/x.html (rendered, for those listed in PAGES_TO_RENDER and handled in a function below or something)
/templates/y.html -> nowhere (used as base templates for inheritance, for those not listed in PAGES_TO_RENDER)
"""

# at this scale, we can afford to just wipe the dired and start fresh to save the logic about caching, invalidation, etc.
shutil.rmtree('built', ignore_errors=True)
os.mkdir('built')

# copy includes ala collect_static
shutil.copytree('includes', 'built/includes', dirs_exist_ok=True)

# RENDER posts/postX.md to /built/posts/postX.html using templates/base.html /post.html
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape()
)

for mdfile in Path('posts').glob('*.md'):
    name = mdfile.stem
    with open(mdfile) as f:
        post = frontmatter.load(f)
    matter = post.to_dict()

    date = matter.get('date')
    if date:
        date_out = humanize.naturalday(date,
            f"%A, {humanize.ordinal(date.day)} %B %Y"
        )
        matter['date'] = date_out

    # add the language name to the top-right of code blocks
    class CustomHtmlFormatter(HtmlFormatter):
        def __init__(self, lang_str='', **options):
            super().__init__(**options)
            self.lang_str = lang_str.split('-', maxsplit=1)[-1]

        def _wrap_code(self, source):
            if self.lang_str != 'text':
                yield 0, f'<div class="lang">{self.lang_str}</div>'
            yield from source

    matter['content'] = md.markdown(
        matter['content'],
        extensions=[
            'fenced_code', 
            'tables',
            'sane_lists',
            WikiLinkExtension(base_url='', end_url='.html'),
            CodeHiliteExtension(pygments_formatter=CustomHtmlFormatter)
        ]
    )

    template = env.get_template('post.html')
    out = template.render(**matter)

    with open(f'built/{name}.html', 'w') as f:
        f.write(out)


# RENDER about

template = env.get_template('about.html')
out = template.render(
    about_active=True,
    title='About'
)
with open('built/about.html', 'w') as f:
    f.write(out)

# RENDER all

template = env.get_template('all.html')

all_posts = []

for mdfile in Path('posts').glob('*.md'):
    with open(mdfile) as f:
        front = frontmatter.load(mdfile).to_dict()
        fn = f"{mdfile.stem}.html"
        front.update({'filename': fn})
        all_posts.append(front)

out = template.render(
    all_active=True,
    all_posts=all_posts,
    title='About'
)

with open('built/all.html', 'w') as f:
    f.write(out)
