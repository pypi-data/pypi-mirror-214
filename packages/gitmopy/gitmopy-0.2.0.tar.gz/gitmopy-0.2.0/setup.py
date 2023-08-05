# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitmopy']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.31,<4.0.0',
 'emoji>=2.5.0,<3.0.0',
 'inquirerpy>=0.3.4,<0.4.0',
 'pyyaml>=6.0,<7.0',
 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['gitmopy = gitmopy.cli:app']}

setup_kwargs = {
    'name': 'gitmopy',
    'version': '0.2.0',
    'description': 'A python command-line for gitmoji',
    'long_description': "# gitmopy\n\nAn interactive Python implementation of the Gitmoji standard: https://gitmoji.dev/\n\n```\npip install gitmopy\n```\n\n![demo-gitmopy](./assets/demo-gitmopy.gif)\n\n```text\n$ gitmopy info\n\ngitmopy info:\n  version : 0.1.0\n  app path: /Users/victor/.gitmopy\n  history : /Users/victor/.gitmopy/history.json\n  config  : /Users/victor/.gitmopy/config.yaml\n\nCurrent configuration:\n  skip_scope      : False\n  skip_message    : False\n  capitalize_title: True\n  enable_history  : True\n```\n\nUpdate configuration with\n\n```text\n$ gitmopy config\n$ gitmopy config\n❓ Configure gitmopy locally. Use 'space' to (de-)select, 'enter' to validate.\n❯ ○ Skip commit scope\n  ○ Skip commit message\n  ◉ Capitalize commit title\n  ◉ Remember commit history for auto-complete and emoji sorting\n\nConfig will be saved in /Users/victor/.gitmopy/config.yaml.\n```\n\nGet help with\n\n```text\n$ gitmopy --help\n\n Usage: gitmopy [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ──────────────────────────────────────────────────────────────────╮\n│ --install-completion          Install completion for the current shell.    │\n│ --show-completion             Show completion for the current shell, to    │\n│                               copy it or customize the installation.       │\n│ --help                        Show this message and exit.                  │\n╰────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ─────────────────────────────────────────────────────────────────╮\n│ commit  Commit staged files. Use --add to add all unstaged files if none   │\n│         is already staged                                                  │\n│ config  Configure gitmopy                                                  │\n│ info    Print gitmopy info                                                 │\n╰────────────────────────────────────────────────────────────────────────────╯\n\n\n$ gitmopy commit --help\n\n Usage: gitmopy commit [OPTIONS]\n\n Commit staged files. Use --add to add all unstaged files if none is already\n staged\n\n╭─ Options ──────────────────────────────────────────────────────────────────╮\n│ --repo                 TEXT  Path to the git repository [default: .]       │\n│ --add     --no-add           Whether or not to add all unstaged files if   │\n│                              none is already staged                        │\n│                              [default: no-add]                             │\n│ --push    --no-push          Whether to `git push` after commit. Disabled  │\n│                              by default.                                   │\n│                              [default: no-push]                            │\n│ --dry     --no-dry           Whether or not to actually commit.            │\n│                              [default: no-dry]                             │\n│ --help                       Show this message and exit.                   │\n╰────────────────────────────────────────────────────────────────────────────╯\n```\n",
    'author': 'vict0rsch',
    'author_email': 'vsch@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
