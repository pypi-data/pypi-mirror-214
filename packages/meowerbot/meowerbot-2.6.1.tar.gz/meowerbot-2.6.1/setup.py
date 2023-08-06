# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['MeowerBot', 'MeowerBot.cl', 'MeowerBot.ext']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0', 'websocket-client']

extras_require = \
{':python_version < "3.11"': ['backports-strenum>=1.2.4,<2.0.0']}

setup_kwargs = {
    'name': 'meowerbot',
    'version': '2.6.1',
    'description': 'A meower bot lib for py',
    'long_description': '# MeowerBot.py\n\nA bot lib for Meower\n\n\n## License\n\nsee [LICENSE](./LICENSE)\n\n\n## docs\n\nThe Docs are located [here](https://meowerbot-py.showierdata.tech/)\n\n\n## Quick Example\n\nlook at the [tests directory](./tests) for examples ',
    'author': 'showierdata9978',
    'author_email': '68120127+showierdata9978@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MeowerBots/MeowerBot.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
