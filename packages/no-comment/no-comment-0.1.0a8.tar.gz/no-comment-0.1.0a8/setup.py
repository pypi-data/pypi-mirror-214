# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['no_comment',
 'no_comment.application',
 'no_comment.application.use_cases',
 'no_comment.configuration',
 'no_comment.domain',
 'no_comment.domain.commenting',
 'no_comment.infrastructure',
 'no_comment.infrastructure.file_system',
 'no_comment.infrastructure.flask',
 'no_comment.interfaces',
 'no_comment.interfaces.to_http',
 'no_comment.interfaces.to_http.as_html']

package_data = \
{'': ['*'],
 'no_comment.infrastructure.flask': ['static/css/*',
                                     'static/img/*',
                                     'static/js/*'],
 'no_comment.interfaces.to_http.as_html': ['templates/*', 'templates/mixins/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'bl3d>=0.3.0,<0.4.0',
 'jinja2-fragments>=0.3.0,<0.4.0',
 'pypugjs>=5.9.12,<6.0.0']

setup_kwargs = {
    'name': 'no-comment',
    'version': '0.1.0a8',
    'description': 'Comment any resource on the web!',
    'long_description': '# No Comment\n\nComment any resource on the web!\n',
    'author': 'Tanguy Le Carrour',
    'author_email': 'tanguy@bioneland.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
