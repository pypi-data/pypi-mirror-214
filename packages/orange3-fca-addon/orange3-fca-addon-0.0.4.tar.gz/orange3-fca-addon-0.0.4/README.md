## Orange-FCA

This repository contains an add-on for the Orange Datamining Framework which extends the functionality with multiple Formal Concept Analysis widgets.

### Requirements
- `Python 3.7+` or `3.10`

### Installation
In order to install local dependencies firstly initialize a local virtual environment (Example with Pipenv, otherwise follow normal pip installation).

- Pip
  - `pip install -r requirements.txt`
- Pipenv
  - `pipenv install` (or `pipenv install --dev`)

Then, we need to include the library into Orange:

- Pip (editable mode)
  - `pip install -e .`

- Pipenv
  - `pipenv install '-e .'`

### Usage

After the installation, the widgets from this add-on are registered with Orange. To run Orange from the terminal, use

- `python3 -m Orange.canvas`

The new widgets are in the toolbox bar under FCA Addon section.
