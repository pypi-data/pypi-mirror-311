# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_down']

package_data = \
{'': ['*']}

install_requires = \
['dash-extensions>=1.0.19',
 'dash-iconify>=0.1.2,<0.2.0',
 'dash-mantine-components>=0.14.11',
 'dash>=2.18.2',
 'dataclass-wizard>=0.30.1,<0.31.0',
 'mistune==2.0.4',
 'python-box>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'dash-down',
    'version': '0.1.4',
    'description': '',
    'long_description': '[![Unit tests](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml/badge.svg)](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml)\n[![codecov](https://codecov.io/gh/emilhe/dash-down/branch/main/graph/badge.svg?token=kZXx2N1QGY)](https://codecov.io/gh/emilhe/dash-down)\n\nThe `dash-down` package provides tools to render markdown files into Plotly Dash component trees. Besides standard markdown syntax, a custom interpretation of the [directive syntax extension](https://mistune.readthedocs.io/en/latest/directives.html) makes it possible to embed Dash code blocks and/or applications (including callbacks). For a live demo, please take look at the [`dash-extensions` documentation](https://www.dash-extensions.com/sections/installation).\n\n## Getting started\n\nMake sure that you have setup [poetry](https://python-poetry.org/). Then run\n\n    poetry install\n\nto install dependencies.\n\n#### Running the example\n\n    poetry run python example.py\n\n#### Running the tests\n\n    poetry run pytest\n\n## Custom content\n\nCustom content is rendered via the markdown [directive syntax extension](https://mistune.readthedocs.io/en/latest/directives.html). A directive has the following syntax,\n\n    .. directive-name:: directive value\n       :option-key: option value\n       :option-key: option value\n    \n       full featured markdown text here\n\nwhere the `directive-name` is mandatory, while the `value`, the `options` (specified as key value pairs), and the `text` are optional. \n\n#### What directives are bundled?\n\nCurrently, the bundled directives are\n\n* **api-doc** - a directive for rendering api documentation for a component\n* **dash-proxy** - a directive for rendering dash apps (including interactivity)\n\n#### How to create custom directives?\n\nThe easiest way to create a custom directive is to create a function with the following signature,\n\n```python\nfrom box import Box\nfrom dash_extensions.enrich import DashBlueprint\n\ndef directive_name(value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):\n    """\n    :param value: the directive value (optional)\n    :param text: the markdown text (optional)\n    :param options: a Box object containing all key value pairs (optional)\n    :param blueprint: the DashBlueprint of the resulting Dash component tree, used e.g. for callback registration\n    :return: a Dash component\n    """\n    ...\n```\n\nSay, we want to make a new directive that yields a plot of the `iris` dataset. The code would then be along the lines of,\n\n```python\nimport plotly.express as px\nfrom box import Box\nfrom dash_extensions.enrich import dcc, DashBlueprint\n\ndef graph(value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):\n    df = getattr(px.data, options.dataset)()\n    fig = px.scatter(df, x=options.x, y=options.y)\n    return dcc.Graph(figure=fig)\n```\n\nWith this directive defined, it is now possible to create a graph similar to [the one in the Dash docs](https://dash.plotly.com/dash-core-components/graph) with the following syntax,\n\n    .. graph::\n       :dataset: iris\n       :x: sepal_width\n       :y: sepal_length\n\nTo render a markdown file using the new, shiny directive, the syntax would be,\n\n```python\nfrom dash_extensions.enrich import DashProxy\nfrom dash_down.express import md_to_blueprint_dmc, GITHUB_MARKDOWN_CSS_LIGHT\n\n...\n\nblueprint = md_to_blueprint_html(\'path_to_your_md_file\', directives=[graph])\napp = DashProxy(blueprint=blueprint, external_stylesheets=[GITHUB_MARKDOWN_CSS_LIGHT])\n\nif __name__ == \'__main__\':\n    app.run_server()\n```\n\nA working example is bundled in the repo (see `example_custom_directive.py`).\n\n#### How to customize the layout of the rendered blueprint?\n\nThe layout of the blueprint returned by the renderer can be customized by passing a custom app shell via the `shell` keyword of the `md_to_blueprint_html` function. A working example is bundled in the repo (see `example_code_renderer.py`).\n\nPer default, the app shell is a `Div` element with `className="markdown-body"`. This class makes it possible to use GitHub CSS for styling.\n\n#### How to customize the way code is rendered with the DashProxyDirective?\n\nThe layout of the Dash apps rendered via the `DashProxyDirective` can be customized via the `dash_proxy_shell` keyword of the `md_to_blueprint_html` function. A working example is bundled in the repo (see `example_code_renderer.py`).\n\nPer default, the app shell `Div` element with the code rendered as the first child and the resulting app rendered as the second.\n\n#### How to customize the markdown rendering itself?\n\nMake a subclass of `DashMantineRenderer` (or `DashHtmlRenderer`, if you prefer to start from raw HTML) and override the render function(s) for any element that you want to change. A good place to start would be to look at the `DashMantineRenderer` class itself for inspiration.\n',
    'author': 'emher',
    'author_email': 'emil.h.eriksen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/emilhe/dash-down',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
