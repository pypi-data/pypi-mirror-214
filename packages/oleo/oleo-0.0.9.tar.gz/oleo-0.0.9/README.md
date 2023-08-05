# `oleo`

[![PyPI Version](https://img.shields.io/pypi/v/oleo.svg)](https://pypi.python.org/pypi/oleo)
[![Build Status](https://img.shields.io/travis/daquintero/oleo.svg)](https://travis-ci.com/daquintero/oleo)
[![Documentation Status](https://readthedocs.org/projects/oleo/badge/?version=latest)](https://oleo.readthedocs.io/en/latest/?version=latest)
[![Updates](https://pyup.io/repos/github/daquintero/oleo/shield.svg)](https://pyup.io/repos/github/daquintero/oleo/)

Interactive netlist visualisation tools compatible with GDSFactory

- Free software: MIT license
- Documentation: [https://oleo.readthedocs.io](https://oleo.readthedocs.io)

## Installation

To install use pip:

    $ pip install oleo

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/daquintero/oleo.git
    $ cd oleo
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix oleo
    $ jupyter nbextension enable --py --sys-prefix oleo

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite oleo

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
