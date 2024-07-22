# A template project for flask apps

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license](https://img.shields.io/github/license/buehlefs/flask-template)](https://github.com/buehlefs/flask-template/blob/main/LICENSE)
![Python: >= 3.9](https://img.shields.io/badge/python-^3.9-blue)

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

Before the first start, be sure to create a database: See [SQLAchemy](#sqlalchemy)

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

### Using the Template

To use this template for your own project follow these steps:

 1. Create a new empty git repository (optional)
 2. Copy the content from this template repository into the new repository (use the "download as zip" function from GitHub)
 3. Commit the changes
 4. Install the dependencies (`poetry install`)
 5. Rename the template project:
    ```bash
    poetry run invoke rename-project --name="<new_project_name_here>"
    ```
    :warning: The new project name should be lower case and use `_` between words (i.e. `snake_case`).

    OR: Manually search and replace all occurrences of `flask_template` and variations.
 6. Review and commit all changes
 7. Update (or remove) the changelog to fit your project
 8. Change the license and the license link in this file (line 4) to fit your project
 9. Add a link to the `buehlefs/flask-template` repository to this file (optional)
10. Remove the `Using the Template` paragraph from this file (optional)
11. Commit all changes
12. Start coding (follow [Development](#development) to get started)

This template is updated from time to time. Major changes will be highlighted in the changelog.
Viewing the changes made to the code in the template repository can be helpful when updating your project.


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

Before the first database migration is created, or when DB Models are upodated in preparation for a new migration use the following commands to create the database directly from the DB Models:

```bash
# create dev db (this will NOT run migrations!)
poetry run flask create-db
# drop dev db
poetry run flask drop-db
```

To create the database from existing migrations use the following command:

```bash
poetry run flask db upgrade
```


## Migrations

Database migrations can be used to upgrade existing databases to new schemas without loosing data.
Migration scripts are placed in `migrations/versions` by default.
Use the following commands to create and use migrations:

```bash
# create a new migration after changes in the db (Always manually review the created migration!)
poetry run flask db migrate -m "Initial migration."
# upgrade db to the newest migration
poetry run flask db upgrade
# help (and list available commands)
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

---

## Projects using this Template

 *  <https://github.com/UST-QuAntiL/qhana-plugin-runner>
 *  <https://github.com/UST-QuAntiL/qhana-plugin-registry>
 *  <https://github.com/qunicorn/qunicorn-core>
 *  <https://github.com/Muster-Suchen-und-Erkennen/muse-for-anything>

:information_source: Feel free to creat an issue or a PR if you want your project to be listed here.
