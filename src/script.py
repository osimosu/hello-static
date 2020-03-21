from json import load
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

template_env = Environment(loader=FileSystemLoader(searchpath=Path('src')))
template = template_env.get_template('layout.html')

with open(Path('src/article.md')) as markdown_file:
    article = markdown(
        markdown_file.read(),
        extras=['fenced-code-blocks', 'code-friendly']
    )

with open(Path('config.json')) as config_file:
    config = load(config_file)

with open(Path('site/index.html'), 'w') as output_file:
    output_file.write(
        template.render(
            title=config['title'],
            description=config['description'],
            article=article
        )
    )
