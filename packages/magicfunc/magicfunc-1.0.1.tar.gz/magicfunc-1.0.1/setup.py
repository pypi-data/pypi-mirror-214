# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magicfunc']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.6,<0.28.0']

setup_kwargs = {
    'name': 'magicfunc',
    'version': '1.0.1',
    'description': 'magicfunc is a Python library that uses LLM to generate function bodies for function signatures and dynamically proxies them at runtime.',
    'long_description': '# magicfunc\n\nmagicfunc is a Python library that uses LLM to generate function bodies for function signatures and dynamically proxies them at runtime.\n\n[中文文档](README_zh.md)\n\n## Installation\n\nYou can install magicfunc using pip:\n\n```bash\npip install magicfunc\n```\n\n## Usage\n\nTo use magicfunc, you need to define a function signature and pass it to the `magicfunc.magic` decorator. magicfunc will then generate a function body using LLM and dynamically proxy it at runtime.\n\n```python\nimport magicfunc\n\n@magicfunc.magic\ndef add(x: int, y: int) -> int:\n    """\n    Add two integers together.\n    """\n```\n\nYou can then call the function as you would any other function:\n\n```python\nresult = add(2, 3)\nprint(result) # Output: 5\n```\n\nmagicfunc will generate a function body that adds the two integers together and returns the result.\n\n## Configuration\n\nmagicfunc can be configured using these variables:\n\n- `DEFAULT_PROVIDER`: The default provider for generate function body.\n\n## Contributing\n\nIf you find a bug or have a feature request, please open an issue on GitHub. If you would like to contribute code, please fork the repository and submit a pull request.\n\n## License\n\nmagicfunc is licensed under the MIT License. See the LICENSE file for more information.',
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
