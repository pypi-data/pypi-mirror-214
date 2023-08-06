# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temporian',
 'temporian.core',
 'temporian.core.data',
 'temporian.core.data.dtypes',
 'temporian.core.data.test',
 'temporian.core.operators',
 'temporian.core.operators.binary',
 'temporian.core.operators.calendar',
 'temporian.core.operators.scalar',
 'temporian.core.operators.test',
 'temporian.core.operators.unary',
 'temporian.core.operators.window',
 'temporian.core.serialization',
 'temporian.core.test',
 'temporian.implementation',
 'temporian.implementation.numpy',
 'temporian.implementation.numpy.data',
 'temporian.implementation.numpy.data.test',
 'temporian.implementation.numpy.operators',
 'temporian.implementation.numpy.operators.binary',
 'temporian.implementation.numpy.operators.calendar',
 'temporian.implementation.numpy.operators.scalar',
 'temporian.implementation.numpy.operators.test',
 'temporian.implementation.numpy.operators.window',
 'temporian.implementation.numpy.test',
 'temporian.implementation.numpy_cc',
 'temporian.implementation.numpy_cc.operators',
 'temporian.io',
 'temporian.io.test',
 'temporian.proto',
 'temporian.test',
 'temporian.utils',
 'temporian.utils.test']

package_data = \
{'': ['*'],
 'temporian.test': ['test_data/*', 'test_data/io/*', 'test_data/prototype/*']}

install_requires = \
['absl-py>=1.3.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'protobuf>=4.21.12,<5.0.0']

setup_kwargs = {
    'name': 'temporian',
    'version': '0.1.1',
    'description': 'Temporian is a Python package for feature engineering of temporal data, focusing on preventing common modeling errors and providing a simple and powerful API, a first-class iterative development experience, and efficient and well-tested implementations of common and not-so-common temporal data preprocessing functions.',
    'long_description': '<img src="https://github.com/google/temporian/blob/main/docs/src/assets/banner.png?raw=true" width="100%" alt="Temporian logo">\n\n![tests](https://github.com/google/temporian/actions/workflows/test.yaml/badge.svg) ![formatting](https://github.com/google/temporian/actions/workflows/formatting.yaml/badge.svg) [![docs](https://readthedocs.org/projects/temporian/badge/?version=latest)](https://temporian.readthedocs.io/en/latest/?badge=latest)\n\n**Temporian** is a Python package for **feature engineering of temporal data**, focusing on **preventing common modeling errors** and providing a **simple and powerful API**, a first-class **iterative development** experience, and **efficient and well-tested implementations** of common and not-so-common temporal data preprocessing functions.\n\n## Installation\n\nTemporian is available on PyPI. To install it, run:\n\n```shell\npip install temporian\n```\n\n## Getting Started\n\nThis is how a minimal end-to-end example looks like:\n\n```python\nimport temporian as tp\n\n# Load data and create input node.\nevset = tp.from_csv("temporal_data.csv", timestamp_column="date")\nsource = evset.node()\n\n# Apply operators to create a processing graph.\nsma = tp.simple_moving_average(source, window_length=tp.duration.days(7))\n\n# Run the graph.\nresult_evset = sma.evaluate({source: evset})\n\n# Show output.\nprint(result_evset)\nresult_evset.plot()\n```\n\nThis is an example `temporal_data.csv` to use with the code above:\n\n```\ndate,feature_1,feature_2\n2023-01-01,10.0,3.0\n2023-01-02,20.0,4.0\n2023-02-01,30.0,5.0\n```\n\nCheck the [Getting Started tutorial](https://temporian.readthedocs.io/en/stable/tutorials/getting_started/) to try it out!\n\n## Key features\n\nThese are what set Temporian apart.\n\n- **Simple and powerful API**: Temporian exports high level operations making processing complex programs short and ready to read.\n- **Flexible data model**: Temporian models temporal data as a sequence of events, supporting non-uniform sampling timestamps seamlessly.\n- **Prevents modeling errors**: Temporian programs are guaranteed not to have future leakage unless explicitly specified, ensuring that models are not trained on future data.\n- **Iterative development**: Temporian can be used to develop preprocessing pipelines in Colab or local notebooks, allowing users to visualize results each step of the way to identify and correct errors early on.\n- **Efficient and well-tested implementations**: Temporian contains efficient and well-tested implementations of a variety of temporal data processing functions. For instance, our implementation of window operators is **x2000** faster than the same function implemented with NumPy.\n- **Wide range of preprocessing functions**: Temporian contains a wide range of preprocessing functions, including moving window operations, lagging, calendar features, arithmetic operations, index manipulation and propagation, resampling, and more. For a full list of the available operators, see the [operators documentation](https://temporian.readthedocs.io/en/stable/reference/).\n\n## Documentation\n\nThe official documentation is available at [temporian.readthedocs.io](https://temporian.readthedocs.io/en/stable/).\n\n## Contributing\n\nContributions to Temporian are welcome! Check out the [contributing guide](CONTRIBUTING.md) to get started.\n\n## Credits\n\nThis project is a collaboration between Google and [Tryolabs](https://tryolabs.com/).\n',
    'author': 'Mathieu Guillame-Bert, Braulio Ríos, Guillermo Etchebarne, Ian Spektor, Richard Stotz',
    'author_email': 'gbm@google.com',
    'maintainer': 'Mathieu Guillame-Bert',
    'maintainer_email': 'gbm@google.com',
    'url': 'https://github.com/google/temporian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}
from config.build import *
build(setup_kwargs)

setup(**setup_kwargs)
