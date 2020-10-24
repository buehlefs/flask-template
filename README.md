# A template project for flask apps

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## VSCode

For vscode install the python extension and add the poetry venv path to the folders the python extension searches vor venvs.

On linux:

```json
{
    "python.venvFolders": [
        "~/.cache/pypoetry/virtualenvs"
    ]
}
```

## Install for Development

Run `poetry install`


## Babel

```bash
# initial
poetry run pybabel extract -F babel.cfg -o messages.pot .
# create language
poetry run pybabel init -i messages.pot -d translations -l en
# compile translations to be used
poetry run pybabel compile -d translations
# extract updated strings
poetry run pybabel update -i messages.pot -d translations
```
