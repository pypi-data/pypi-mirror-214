# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ready_logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ready-logger',
    'version': '1.0.0',
    'description': 'Easily configure Python loggers.',
    'long_description': '## Easily configure Python loggers\n\n### Install\n`pip install ready_logger`\n\n\n### Usage\nThere is one function: `get_logger`\n```py\nfrom ready_logger import get_logger\n```\n\n#### Signature\n```py\ndef get_logger(\n    name: Optional[str] = None,\n    level: Optional[Union[str, int]] = None,\n    show_file_path: Optional[bool] = None,\n    file_dir: Optional[Union[str, Path]] = None,\n    max_bytes: Optional[int] = 20_000_000,\n    backup_count: Optional[int] = 2,\n) -> Logger:\n    """Create a new logger or return an existing logger with the given name.\n\n    All arguments besides for `name` can be set via environment variables in the form `{LOGGER NAME}_{VARIABLE NAME}` or `READY_LOGGER_{VARIABLE NAME}`.\n    Variables including logger name will be chosen before `READY_LOGGER_` variables. Variables can be uppercase or lowercase.\n\n    Args:\n        name (Optional[str], optional): Name for the logger. Defaults to None.\n        level (Optional[Union[str, int]], optional): Logging level -- CRITICAL: 50, ERROR: 40, WARNING: 30, INFO: 20, DEBUG: 10.\n        show_file_path (Optional[bool], optional): Show absolute file path in log string prefix rather than just filename. Defaults to True if level is DEBUG, else False.\n        file_dir (Optional[Union[str, Path]], optional): Directory where log files should be written.\n        max_bytes (int): Max number of bytes to store in one log file.\n        backup_count (int): Number of log rotations to keep.\n\n    Returns:\n        Logger: The configured logger.\n    """\n```\n',
    'author': 'Dan Kelleher',
    'author_email': 'kelleherjdan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/djkelleher/ready-logger',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
