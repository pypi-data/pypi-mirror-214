# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['b']

package_data = \
{'': ['*'], 'b': ['schema/*', 'templates/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'appdirs>=1.4.4,<2.0.0',
 'mercurial>=6.0,<7.0',
 'rich-argparse>=1.1.0,<2.0.0',
 'rich>=13.3.5,<14.0.0']

entry_points = \
{'console_scripts': ['b = b.command:run']}

setup_kwargs = {
    'name': 'b-bugtracker',
    'version': '3.0.0',
    'description': 'A simple, distributed bug tracker.',
    'long_description': "b, A distributed bug tracker\n========================================================================================================================\nThis version of `b` was forked from [foss.heptapod.net](https://foss.heptapod.net/mercurial/b).  Originally with only minor modifications, but now it's likely safer to say that this tool simply took inspiration from B.\n\nSo, with that stated, full credit for the inspiration for this tool goes to Michael Diamond.  Thank you for taking the time and investing the effort to create `b`, without which this tool I love wouldn't likely exist.\n\nThe original purpose of B was to serve as a low-feature stand-in for a real, convoluted bug tracking system.  I loved that concept, but have taken the tool much further; much beyond the original, modest scope to the point of adding many features and capabilities to rival those of a fully fledged bug tracking system, but still in a distributed package.\n\n- Now a standalone command-line tool with no dependency upon Mercurial allowing it to be used with any VCS.\n    - See the available [commands](https://jwjulien.github.io/b/commands/index) for more info.\n- Supports Rich output to make interacting a bit more friendly.\n- Supports bug templates to offer a better starting point for new bugs.\n    - Also supports customization at the project level - see [templates](https://jwjulien.github.io/b/commands/templates) for more info.\n- Handles it's own configuration, outside of Mercurial, in support of independence.\n    - See [config command](https://jwjulien.github.io/b/commands/config) for more info about the available configuration options and config file location.\n\nSee the [installation](https://jwjulien.github.io/b/installation) and [getting started](https://jwjulien.github.io/b/getting_started) guides for help with installing and using `b` on your project.\n\n\n\n\nIntroduction\n------------------------------------------------------------------------------------------------------------------------\n`b` is a tool for tracking bugs and open issues that works with any distributed version control system.  Bugs are tracked as YAML files (i.e., nearly plain text) directly in the `.bugs` directory of the project.  That means that when a user adds a new bug they will need to add it into the VCS and commit it.  Then, all changes made to the bug during the process of diagnosis and resolution will be tracked.\n\nThe use of YAML files means that bugs can be opened directly in an editor and manually edited.  In fact, `b` itself does not the ability to set many of the attributes in the bug files from the command line.  It is expected that users will manually open bugs (optionally using the `edit` command) and edit their contents directly.  For more info about the format of these YAML files and the supporting schema, have a look at [the bug file format](https://jwjulien.github.io/b/bugs).\n\n\n\n\nSome Suggested Use Cases\n------------------------------------------------------------------------------------------------------------------------\nSmall scripts and tasks deserve version control, even if they're never going to be distributed elsewhere.  This is easy with Mercurial.  With `b` installed you get a fully functional bug tracker along with your VCS, no additional setup required! As soon as you install `b`, every repository on your machine now has issue tracking functionality ready to use.\n\nWorking on a project with a few other team members is ideal for `b`, it's powerful enough to let everyone track what they need to do, and allow everyone to contribute what they can to any of the bugs on file.  They can search titles for matching bugs, and even grep through the details directory to find details matching what they're looking for.\n",
    'author': 'Michael Diamond',
    'author_email': 'michael@digitalgemstones.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://jwjulien.github.io/b',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
