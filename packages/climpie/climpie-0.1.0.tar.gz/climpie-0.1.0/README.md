# Climpie

<!---
Can use start-after and end-before directives in docs, see
https://myst-parser.readthedocs.io/en/latest/syntax/organising_content.html#inserting-other-documents-directly-into-the-current-document
-->

<!--- sec-begin-description -->

Tools for calculating entities' emissions budgets and associated emissions pathways.


[#5 badges here]


<!--- sec-end-description -->

Full documentation can be found at:
[climpie.readthedocs.io](https://climpie.readthedocs.io/en/latest/).
We recommend reading the docs there because the internal documentation links
don't render correctly on GitLab's viewer.

## Installation

<!--- sec-begin-installation -->

Climpie can be installed with conda or pip:

```bash
pip install climpie
conda install -c conda-forge climpie
```

Additional dependencies can be installed using

```bash
# To add plotting dependencies
pip install climpie[plots]
# To add notebook dependencies
pip install climpie[notebooks]

# If you are installing with conda, we recommend
# installing the extras by hand because there is no stable
# solution yet (issue here: https://github.com/conda/conda/issues/7502)
```

<!--- sec-end-installation -->

### For developers

<!--- sec-begin-installation-dev -->

For development, we rely on [poetry](https://python-poetry.org) for all our
dependency management. To get started, you will need to make sure that poetry
is installed
([instructions here](https://python-poetry.org/docs/#installing-with-the-official-installer),
we found that pipx and pip worked better to install on a Mac).

For all of work, we use our `Makefile`.
You can read the instructions out and run the commands by hand if you wish,
but we generally discourage this because it can be error prone.
In order to create your environment, run `make virtual-environment`.

If there are any issues, the messages from the `Makefile` should guide you
through. If not, please raise an issue in the [issue tracker][issue_tracker].

For the rest of our developer docs, please see [](development-reference).

[issue_tracker]: https://gitlab.com/climate-resource/climpie/issues

<!--- sec-end-installation-dev -->
