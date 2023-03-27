# A template project for flask apps

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license](https://img.shields.io/github/license/buehlefs/flask-template)](https://github.com/buehlefs/flask-template/blob/main/LICENSE)
![Python: >= 3.8](https://img.shields.io/badge/python-^3.8-blue)

This package uses Poetry `>=1.2` ([documentation](https://python-poetry.org/docs/)).

## VSCode

For vscode install the python extension.
Add the poetry venv path to the folders the python extension searches for venvs if the virtualenvs of poetry are not automatically discovered.

On linux:

```json
{
    "python.venvFolders": [
        "~/.cache/pypoetry/virtualenvs"
    ]
}
```

## Development

Run `poetry install` to install dependencies.

The flask dev server loads environment variables from `.flaskenv` and `.env`.
To override any variable create a `.env` file.
Environment variables in `.env` take precedence over `.flaskenv`.
See the content of the `.flaskenv` file for the default environment variables.

Run the development server with

```bash
poetry run flask run
```

### Trying out the Template

For a list of all dependencies with their license open <http://localhost:5000/licenses/>.

#### The API:

<http://localhost:5000/api/>

#### OpenAPI Documentation:

Configured in `flask_template/util/config/smorest_config.py`.

   * Redoc (view only): <http://localhost:5000/api/redoc>
   * Rapidoc: <http://localhost:5000/api/rapidoc>
   * Swagger-UI: <http://localhost:5000/api/swagger-ui>
   * OpenAPI Spec (JSON): <http://localhost:5000/api/api-spec.json>

#### Debug pages:

  * Index: <http://localhost:5000/debug/>
  * Registered Routes: <http://localhost:5000/debug/routes>\
    Useful for looking up which endpoint is served under a route or what routes are available.



## What this Template contains

This template uses the following libraries to build a rest app with a database on top of flask.

 *  Flask ([documentation](https://flask.palletsprojects.com/en/2.0.x/))
 *  Flask-Cors ([documentation](https://flask-cors.readthedocs.io/en/latest/))\
    Used to provide cors headers.\
    Can be configured or removed in `flask_template/__init__.py`.
 *  flask-babel ([documentation](https://flask-babel.tkte.ch), [babel documentation](http://babel.pocoo.org/en/latest/))\
    Used to provide translations.\
    Can be configured in `flask_template/babel.py` and `babel.cfg`.\
    Translation files and Folders: `translations` (and `messages.pot` currently in .gitignore)
 *  Flask-SQLAlchemy ([documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/14/))\
    ORM Mapper for many SQL databases.\
    Models: `flask_template/db/models`\
    Config: `flask_template/util/config/sqlalchemy_config.py` and `flask_template/db/db.py`
 *  Flask-Migrate ([documentation](https://flask-migrate.readthedocs.io/en/latest/), [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/index.html))\
    Provides automatic migration support based on alembic.\
    Migrations: `migrations`
 *  flask-smorest ([documentation](https://flask-smorest.readthedocs.io/en/latest/), [marshmallow documentation](https://marshmallow.readthedocs.io/en/stable/), [apispec documentation](https://apispec.readthedocs.io/en/latest/), [OpenAPI spec](http://spec.openapis.org/oas/v3.0.2))\
    Provides the API code and generates documentation in form of a OpenAPI specification.\
    API: `flask_template/api`\
    API Models: `flask_template/api/v1_api/models`\
    Config: `flask_template/util/config/smorest_config.py` and `flask_template/api/__init__.py`
 *  Flask-JWT-Extended ([documentation](https://flask-jwt-extended.readthedocs.io/en/stable/))\
    Provides authentication with JWT tokens.\
    Config: `flask_template/util/config/smorest_config.py` and `flask_template/api/jwt.py`
 *  Sphinx ([documentation](https://www.sphinx-doc.org/en/master/index.html))\
    The documentation generator.\
    Config: `pyproject.toml` and `docs/conf.py` (toml config input is manually configured in `conf.py`)
 *  sphinxcontrib-redoc ([documantation](https://sphinxcontrib-redoc.readthedocs.io/en/stable/))
    Renders the OpenAPI spec with redoc in sphinx html output.
    Config: `docs/conf.py` (API title is read from spec)
 *  invoke ([documentation](http://www.pyinvoke.org))\
    tool for scripting cli tasks in python
    Tasks: `tasks.py`

Additional files and folders:

 *  `default.nix` and `shell.nix`\
    For use with the [nix](https://nixos.org) ecosystem.
 *  `pyproject.toml`\
    Poetry package config and config for the [black](https://github.com/psf/black) formatter.
 *  `.flaskenv`\
    Environment variables loaded by the `flask` command and the flask dev server.
 *  `.flake8`\
    Config for the [flake8](https://flake8.pycqa.org/en/latest/) linter
 *  `.editorconfig`
 *  `tests`\
    Reserved for unit tests, this template has no unit tests.
 *  `instance` (in .gitignore)
 *  `flask_template/templates` and `flask_template/static`\
    Templates and static files of the flask app
 *  `docs`\
    Folder containing a sphinx documentation
 *  `typings`\
    Python typing stubs for libraries that have no type information.
    Mostly generated with the pylance extension of vscode.
 *  `tasks.py`\
    Tasks that can be executed with `invoke` (see [invoke tasks](#invoke-tasks))


Library alternatives or recommendations:

 *  Rest API: flask-restx ([documentation](https://flask-restx.readthedocs.io/en/latest/))
 *  For including single page applications: flask-static-digest ([documentation](https://github.com/nickjj/flask-static-digest))
 *  For scripting tasks: invoke ([documentation](http://www.pyinvoke.org))
 *  For hashing passwords: flask-bcrypt ([documentation](https://flask-bcrypt.readthedocs.io/en/latest/))
 *  For Background Task Scheduling: [Celery](https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html) (See also [Integrating Celery with Flask](https://flask.palletsprojects.com/en/2.0.x/patterns/celery/))
 

## Poetry Commands

```bash
# install dependencies from lock file in a virtualenv
poetry install

# open a shell in the virtualenv
poetry shell

# update dependencies
poetry update
poetry run invoke update-dependencies # to update other dependencies in the repository

# run a command in the virtualenv (replace cmd with the command to run without quotes)
poetry run cmd
```

## Invoke Tasks

[Invoke](http://www.pyinvoke.org) is a python tool for scripting cli commands.
It allows to define complex commands in simple python functions in the `tasks.py` file.

:warning: Make sure to update the module name in `tasks.py` after renaming the `flask_template` module!

```bash
# list available commands
poetry run invoke --list

# update dependencies (requirements.txt in ./docs and licenses template)
poetry run invoke update-dependencies

# Compile the documentation
poetry run invoke doc

# Open the documentation in the default browser
poetry run invoke browse-doc
```


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

## SQLAlchemy

```bash
# create dev db (this will NOT run migrations!)
poetry run flask create-db
# drop dev db
poetry run flask drop-db
```

## Migrations

```bash
# create a new migration after changes in the db (Always manually review the created migration!)
poetry run flask db migrate -m "Initial migration."
# upgrade db to the newest migration
poetry run flask db upgrade
# help
poetry run flask db --help
```

## Compiling the Documentation

```bash
# compile documentation
poetry run invoke doc

# Open the documentation in the default browser
poetry run invoke browse-doc

# Find reference targets defined in the documentation
poetry run invoke doc-index --filter=searchtext

# export/update requirements.txt from poetry dependencies (for readthedocs build)
poetry run invoke update-dependencies
```
