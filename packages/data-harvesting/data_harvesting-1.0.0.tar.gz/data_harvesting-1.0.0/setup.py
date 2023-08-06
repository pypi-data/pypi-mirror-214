# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_harvesting',
 'data_harvesting.cli',
 'data_harvesting.data_enrichment.generate_queries',
 'data_harvesting.datacite',
 'data_harvesting.gitlab',
 'data_harvesting.oaipmh',
 'data_harvesting.schemas',
 'data_harvesting.schemas.mappings',
 'data_harvesting.sitemap',
 'data_harvesting.util']

package_data = \
{'': ['*'], 'data_harvesting': ['configs/*', 'data_enrichment/*']}

install_requires = \
['advertools>=0.13.2,<0.14.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'codemetapy>=2.3.3,<3.0.0',
 'extruct>=0.13.0,<0.14.0',
 'jq>=1.3.0,<2.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'oaiharvest>=3.0.0,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'progressbar2>=4.2.0,<5.0.0',
 'pyld>=2.0.3,<3.0.0',
 'rdflib>=6.2.0,<7.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.7.0,<0.8.0',
 'xmljson>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['hmc-unhide = data_harvesting.cli.cli:cli']}

setup_kwargs = {
    'name': 'data-harvesting',
    'version': '1.0.0',
    'description': 'Tools for mining, processing and visualizing metadata of data publications in the context of the Helmholtz metadata collaboration (HMC).',
    'long_description': "[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)\n# Data Harvesting\n\nThis repository contains harvesters, aggregators for linked Data and tools around them. \nThis software allows to harvest small subgraphs exposed by certain sources on the web and\nand enrich them such that they can be combined to a single larger linked data graph. \n\nThis software was written for and is mainly currently deployed as a part of the backend for the unified Helmholtz Information and Data Exchange (unHIDE) project by the Helmholtz Metadata Collaboration (HMC) to create\na knowledge graph for the Helmholtz association which allows to monitor, check, enrich metadata as well as\nidentify gabs and needs.\n\nContributions of any kind by you are always welcome!\n\n## Approach:\n\nWe establish certain data pipelines of certain data providers with linked metadata and complement it, by combining it with other sources. For the unhide project this data is annotated in schema.org semantics and serialized mainly in JSON-LD.\n\nData pipelines contain code to execute harvesting from a local to a global level. \nThey are exposed through a cmdline interface (cli) and thus easily integrated in a cron job and can therefore be used to stream data on a time interval bases into some data eco system\n\nData harvester pipelines so far:\n- gitlab pipeline: harvest all public projects in Helmholtz gitlab instances and extracts and complements codemeta.jsonld files. (todo: extend to github)\n- sitemap pipeline: extract JSON-LD metadata a data provider over its sitemap, which contains links to the data entries and when they have been last updated\n- oai pmh pipeline: extract metadata over oai-pmh endpoints from a data provider. it contains a list of entries and when they where last updated. This pipeline uses a converter from dublin core to schema.org, since many providers provide just dublin core so far.\n- datacite pipeline: extract JSON-LD metadata from datacite.org connected to a given organization identifier.\n- schoolix pipeline (todo): Extract links and related resources for a list of given PIDs of any kind\n\nBesides the harvesters there are aggregators which allow one to specify how linked data should be processed while tracking the provenance of the processing in a reversible way. This is done by storing graph updates, so called patches, for each subgraph. These updates can also be then applied directly to a graph database. Processes changes can be provided as SPARQL updates or through python function with a specific interface.\n\nAll harvesters and Aggregators read from a single config file (as example see [configs/config.yaml](https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting/-/blob/dev/data_harvesting/configs/config.yaml)), which contains als sources and specific operations. \n\n## Documentation:\n\nCurrently only in code documentation. In the future under the docs folder and hosted somewhere.\n\n## Installation\n\n```\ngit clone git@codebase.helmholtz.cloud:hmc/hmc-public/unhide/data_harvesting.git\ncd data_harvesting\npip install .\n```\nas a developer install with\n```\npip install -e .\n```\nYou can also setup the project using poetry instead of pip.\n```\npoetry install --with dev\n```\n\nThe individual pipelines have further dependencies outside of python.\n\nFor example the gitlab pipeline relies an codemeta-harvester (https://github.com/proycon/codemeta-harvester)\n\n## How to use this\n\nFor examples look at the `examples` folder. Also the tests in `tests` folder may provide some insight.\nAlso once installed there is a command line interface (CLI), 'hmc-unhide' for example one can execute the gitlab pipeline via:\n\n```\nhmc-unhide harvester run --name gitlab --out ~/work/data/gitlab_pipeline\n```\n\nfurther the cli exposes some other utility on the command line for example to convert linked data files \ninto different formats.\n\n## License\n\nThe software is distributed under the terms and conditions of the MIT license which is specified in the `LICENSE` file.\n## Acknowledgement\n\nThis project was supported by the Helmholtz Metadata Collaboration (HMC), an incubator-platform of the Helmholtz Association within the framework of the Information and Data Science strategic initiative.\n",
    'author': 'Jens Broeder',
    'author_email': 'j.broeder@fz-juelich.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
