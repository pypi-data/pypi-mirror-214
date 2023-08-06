# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_business_metrics',
 'django_business_metrics._internal',
 'django_business_metrics.v0']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3', 'prometheus-client>=0.13.0']

extras_require = \
{'dev': ['black>=22.6.0',
         'django-stubs>=1.12.0',
         'mypy>=0.971',
         'nox>=2023',
         'pytest>=6',
         'pytest-django',
         'ruff>=0.0.272']}

setup_kwargs = {
    'name': 'django-business-metrics',
    'version': '1.0.0',
    'description': 'Django Prometheus business metrics',
    'long_description': "# Django Prometheus business metrics\n\nThis Django app provides a Prometheus metrics endpoint serving so-called business metrics. These are metrics that are calculated when Prometheus hits the metrics endpoint.\n\n## Usage\n\n> This project uses [ApiVer](https://www.youtube.com/watch?v=FgcoAKchPjk).\n> Always import from `django_business_metrics.v0` namespace and not from `django_business_metrics`.\n\n\n1. Create a `BusinessMetricsManager` object and register some metrics:\n\n    ```\n    # project/business_metrics.py\n\n    from django_business_metrics.v0 import BusinessMetricsManager, users\n\n    metrics_manager = BusinessMetricsManager()\n\n    # Add a pre-defined metric\n    metrics_manager.add(users)\n\n    # Add some custom metrics\n    @metrics_manager.metric(name='name', documentation='documentation')\n    def my_metric():\n        return 10\n    ```\n\n2. Register a Prometheus endpoint:\n\n\n    ```\n    # project/urls.py\n\n    ...\n    from .business_metrics import metrics_manager\n\n    ...\n    urlpatterns = [\n        ...\n        path('business-metrics', metrics_manager.view),\n        ...\n    ]\n    ```\n\n3. Setup your Prometheus agent to scrape metrics from `/business-metrics` endpoint.\n\n\n## Development\n\n```\npoetry install\n```\n\nBefore committing make sure to run:\n\n```\nnox -s format test\n```",
    'author': 'Reef Technologies',
    'author_email': 'vykintas.baltrusaitis@reef.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
