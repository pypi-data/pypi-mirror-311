# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuflow_temporal_common']

package_data = \
{'': ['*']}

install_requires = \
['kuflow-rest>=3.0.0,<4.0.0', 'temporalio>=1.6.0,<1.7.0']

setup_kwargs = {
    'name': 'kuflow-temporal-common',
    'version': '3.0.0',
    'description': 'KuFlow utilities to use Temporal.io',
    'long_description': '[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/kuflow/kuflow-sdk-python/blob/master/LICENSE)\n[![Python](https://img.shields.io/pypi/pyversions/kuflow-temporal-common.svg)](https://pypi.org/project/kuflow-temporal-common)\n[![PyPI](https://img.shields.io/pypi/v/kuflow-temporal-common.svg)](https://pypi.org/project/kuflow-temporal-common)\n\n# KuFlow Temporal Common\n\nKuFlow utilities to use with Temporal.\n\n## Documentation\n\nMore detailed docs are available in the [documentation pages](https://docs.kuflow.com/developers/).\n\n## Contributing\n\nWe are happy to receive your help and comments, together we will dance a wonderful KuFlow. Please review our [contribution guide](CONTRIBUTING.md).\n\n## License\n\n[MIT License](https://github.com/kuflow/kuflow-sdk-python/blob/master/LICENSE)\n',
    'author': 'KuFlow S.L.',
    'author_email': 'kuflow@kuflow.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kuflow.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
