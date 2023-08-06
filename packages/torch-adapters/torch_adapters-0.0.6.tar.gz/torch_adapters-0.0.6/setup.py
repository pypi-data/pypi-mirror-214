# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['torch_adapters', 'torch_adapters.adapters']

package_data = \
{'': ['*']}

install_requires = \
['torch>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'torch-adapters',
    'version': '0.0.6',
    'description': 'Small Library of Torch Adaptation modules',
    'long_description': '# Torch Adapters\n\n# Introduction\n\nSmall Library of Torch Adaptation modules\n\n### Supported Methods\n\n- [X] LoRA\n- [X] Prompt Tuning\n- [X] Bottleneck Adapter\n- [X] Prefix Tuning\n- [ ] P-Tuning\n\n# Installation\n\nYou can install torch-adapters using:\n\n    $ pip install torch-adapters\n\n# Usage\n\n```python\nfrom torch_adapters.utils import add_lora\n\n# Add lora to the model\nadd_lora(model, ["key", "value"], {"alpha": 8, "r": 8})\n```\n\n',
    'author': 'ma2za',
    'author_email': 'mazzapaolo2019@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ma2za/torch-adapters',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
