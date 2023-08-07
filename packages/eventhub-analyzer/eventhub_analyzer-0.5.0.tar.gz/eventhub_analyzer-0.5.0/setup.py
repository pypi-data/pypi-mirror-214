# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventhub_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['azure-eventhub>=5.11.1,<6.0.0',
 'azure-storage-blob>=12.14.1,<13.0.0',
 'click>=8.1.3,<9.0.0',
 'jsonpickle>=3.0.1,<4.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'texttable>=1.6.7,<2.0.0']

entry_points = \
{'console_scripts': ['eventhub-analyzer = eventhub_analyzer.main:cli']}

setup_kwargs = {
    'name': 'eventhub-analyzer',
    'version': '0.5.0',
    'description': '',
    'long_description': "# Event Hub Analyzer\n\nEvent Hub Analyzer is a small command line tool that can be used\nto analyze certain aspects of Event Hubs.\n\n## Installation\n\n```\npip install eventhub-analyzer\n```\n\n## Checkpoints per partition\n\nFor every event hub, consumer group, the number of \nevents/sequence numbers between two invocations is retrieved and\nthe throughput per partition is calculated. This can be used to \ndetermine if the load is correctly distributed among partitions.\n\nWhen there are some partition that get little to no throughput while\nothers have large throughput, it is a sign that the partition key\nis not chosen optimally and that you should try to choose a property\nwith a higher cardinality as the partition key.\n\n### Usage\n\n```bash\neventhub-analyzer checkpoints -n CONTAINER_NAME -c CONNECTION_STRING\n```\n\nYou can also specify the settings via environment variables:\n\n```bash\nexport STORAGE_ACCOUNT_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=x;AccountKey=y;EndpointSuffix=core.windows.net'\nexport CONTAINER_NAME='event-hub-offsets'\neventhub-analyzer checkpoints\n```\n\n### Example output\n\n```\nEvent Hub: telemetry, Consumer Group: my-consumer\nEvent Hub   Consumer Group   Partition   Events per second\ntelemetry   my-consumer              0             158.034\ntelemetry   my-consumer              1             203.257\ntelemetry   my-consumer              2             148.103\ntelemetry   my-consumer              3               0.000\ntelemetry   my-consumer              4             201.780\ntelemetry   my-consumer              5             106.081\ntelemetry   my-consumer              6              72.307\ntelemetry   my-consumer              7             160.783\ntelemetry   my-consumer              8             118.351\n```\n\nAs you can see, partition 3 is not getting any events and\nthe number of events is not well distributed overall. There\nmight be some gains possible by choosing a different partition key\n(or by partitioning manually on the client).\n\n## Publishing\n\n```\npoetry build\npoetry publish\n```\n",
    'author': 'Stefan Hudelmaier',
    'author_email': 'stefan.hudelmaier@device-insight.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/deviceinsight/eventhub-analyzer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
