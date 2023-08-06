# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_tags_getter',
 'docker_tags_getter.api',
 'docker_tags_getter.api.v2',
 'docker_tags_getter.cli',
 'docker_tags_getter.config',
 'docker_tags_getter.fetcher',
 'docker_tags_getter.filters']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.31.0,<3.0.0', 'rich>=13.4.2,<14.0.0', 'typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['dtg = docker_tags_getter.main:main']}

setup_kwargs = {
    'name': 'docker-tags-getter',
    'version': '0.3.3',
    'description': 'docker_tags_getter will help you to get tags from your docker repository.',
    'long_description': 'docker_tags_getter\n==================\n\ndocker_tags_getter is the application that will help you to get tags from yours docker repository.\n\nAuthor\n======\n\nKostiantyn Klochko (c) 2023\n\nLicense\n=======\n\nUnder the GNU Lesser General Public License v3.0 or later.\n\n',
    'author': 'Kostiantyn Klochko',
    'author_email': 'kostya_klochko@ukr.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/KKlochko/docker_tags_getter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
