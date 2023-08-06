# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spytula', 'spytula.mixins']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0', 'pytest>=7.3.2,<8.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'spytula',
    'version': '0.0.0',
    'description': '',
    'long_description': '# Spytula\n\nSpytula is a Python library that provides a simple and convenient way to build JSON and YAML data structures using a builder pattern.\n\n## Installation\n\nUse pip to install the Spytula library:\n\n```bash\npip install spytula\n```\n\n## Usage    \n\nImport the `SpytulaBuilder` class from the `spytula.builder` module:\n\n```python\nfrom spytula.builder import SpytulaBuilder\n\n# Create an instance of SpytulaBuilder\nbuilder = SpytulaBuilder()\n\n# Add attributes to the JSON structure\nbuilder.attribute(\'name\', \'Ramen\')\nbuilder.attribute(\'origin\', \'Japan\')\n\n# Create a list of ingredients\nfor builder.each(\'ingredients\') as add_ingredient:    \n    for ingredient in [\'Noodles\', \'Pork\', \'Eggs\', \'Miso\']:\n        with add_ingredient() as ingredient_builder:\n            ingredient_builder.attribute(\'name\', ingredient)\n\n# Add optional attributes conditionally\nbuilder.when(\'spiciness\', \'Medium\', True)\nbuilder.when(\'extra_toppings\', [\'Green Onions\', \'Nori\', \'Bamboo Shoots\'], True)\n\n# Configure the key to use camelcase\nbuilder.key_format(camelize={\'uppercase_first_letter\': False})\n\n# Convert the JSON structure to JSON-formatted string\njson_output = builder.to_json(indent=4)\n\n# Print the JSON output\nprint(json_output)\n```\n\nThis will output:\n\n```json\n{\n    "name": "Ramen",\n    "origin": "Japan",\n    "ingredients": [\n        { "name": "Noodles" },\n        { "name": "Pork" },\n        { "name": "Eggs" },\n        { "name": "Miso" }\n    ],\n    "spiciness": "Medium",\n    "extraToppings": [\n        "Green Onions",\n        "Nori",\n        "Bamboo Shoots"\n    ]\n}\n\n```\n\nIn this example, we create a `SpytulaBuilder` instance and add attributes like name and origin to represent `Ramen`. We use the `nodes()` context manager to create a list of ingredients and add them to the JSON structure. Optional attributes like spiciness and toppings are added conditionally using the `when()` method. Finally, we convert the JSON structure to a JSON-formatted string using `to_json()` with an indentation of 4 spaces.\n',
    'author': 'ICIJ',
    'author_email': 'engineering@icij.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
