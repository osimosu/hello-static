import http.server
import os
import socketserver
from functools import partial
from json import load
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

template_env = Environment(loader=FileSystemLoader(searchpath=Path('template')))
template = template_env.get_template('layout.html')

with open(Path('content/article.md')) as markdown_file:
    markdown_content = markdown(
        markdown_file.read(),
        extras=['metadata', 'fenced-code-blocks', 'code-friendly']
    )

with open(Path('config.json')) as config_file:
    config = load(config_file)

if not os.path.exists(Path('site')):
    os.makedirs(Path('site'))

with open(Path('site/index.html'), 'w') as output_file:
    output_file.write(
        template.render(
            title=config['title'],
            description=config['description'],
            article={
                'title': markdown_content.metadata['title'],
                'date': markdown_content.metadata['date'],
                'content': markdown_content
            }
        )
    )

PORT = 9000
Handler = partial(http.server.SimpleHTTPRequestHandler, directory='site')

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
