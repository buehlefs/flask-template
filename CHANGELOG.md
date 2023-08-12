# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added sphinx setting for changing the html theme in `pyproject.toml`

### Updated

- Updated alembic/flask-migrate config to work with updated dependencies again
- Updated dev dependencies specification to use new group key (see <https://python-poetry.org/docs/managing-dependencies/#dependency-groups>)
- Updated depencencies (the lockfile now uses urrlib3 `>=2.0`, pin urrllib3 to a lower version if required)

### Fixed

- Joining of command line arguments if running under windows (see also <https://learn.microsoft.com/de-de/archive/blogs/twistylittlepassagesallalike/everyone-quotes-command-line-arguments-the-wrong-way>)\
  ⚠️ This does **not** properly escape meta-characters recognized by CMD.exe! (see the linked blog post for more information)
- Documentation paths in invoke tasks were outdated (documentation output is directly in the `_build` folder)


## [v0.4.1]

### Updated

- Updated SQLAlchemy models to use new `2.0` style (see <https://docs.sqlalchemy.org/en/20/changelog/migration_14.html>)

### Notable Dependency Updates

- `SQLAlchemy`: updated to version 2.0 [Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html)
- `Sphinx` is now version 6 by default
- `myst-parser` updated to support newest sphinx


## [v0.4.0]

### Added

- Added SQLAlchemy to the top level dependencies to fix it to version `^1.4`

### Notable Dependency Updates

- Updated **all** dependencies to newer versions. Please check the changelogs of the updated Packages!
- `Python` the minimum supported python version is now `3.8.1`
- `Flask-SQLAlchemy` & `Flask-Migrate` changes to support SQLAlchemy `2.0` (many of the changes, e.g., for session handling, can break code in subtle ways so beware and read the changelogs!)
- `Flask-Babel` with incompatible changes (see changes in `babel.py`)
- `Flask-Smorest` small changes, but transitive dependencies also changed: `Apispec` and `marshmallow`
- `Sphinx` is now version 5 by default
- `invoke` update to version 2 for python 3.11 support

### Removed

- `recommonmark` dev dependency (package is no longer maintained; use the MyST parser instead)


## [v0.3.0]

### Added

- Updated redoc library version used in documentation to be compatible with used OpenAPI version
- Update config handling to handle deprecation of FLASK_ENV gracefully (this may impact how test config is loaded)
- Update flask-smorest to version `>0.39.0` to be compatible with flask `>2.2`
- Update flask-smorest to version `>0.31.1` to enable rapidoc OpenAPI documentation renderer
- Default settings for sorting imports with isort (in `pyproject.toml`)
- Add [MyST](https://myst-parser.readthedocs.io/en/latest/) markdown parser as default for documentation to support more reStructuredText features in markdown
- Add default environment variables in `.flaskenv`
- Add `tomli` as the default toml configuration parser
- Add invoke to automate some cli tasks
- Add invoke task to update doc dependencies
- Add invoke task to create a licenses page
- Add route for licenses

### Deprecated

- Recommonmark markdown parser configuration for documentation (use the MyST parser instead; will be removed in next release)

### Removed

- `tomlkit` dependency


## [v0.2.0]

### Changed

- License changed from MIT to [Unlicense](https://unlicense.org). This should make it easier to use the template for other projects.

### Added

- Build instructions for sphinx documentation
- Dataclass example for DB Models
- Optional parameter for optional jwt checking
- Minor additions to the documentation (and to code comments)

### Notable Dependency Updates

- flask-smorest: [Changelog](https://github.com/marshmallow-code/flask-smorest/blob/master/CHANGELOG.rst) All `@response` decorators have a new signature, other incompatible changes
- flask-sqlalchemy: [Changelog](https://github.com/pallets/flask-sqlalchemy/blob/master/CHANGES.rst) See also SQLAlchemy 1.4 [migration guide](https://docs.sqlalchemy.org/en/14/changelog/migration_14.html) (but SQLAlchemy 1.3 is still supported)
- flask-migrate: [Changelog](https://github.com/miguelgrinberg/Flask-Migrate/blob/main/CHANGES.md)
- flask-jwt-extended: [Upgrade Guide](https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/) Major breaking changes! Security Relevant! (Also see changes in `flask_template/api/jwt.py` and `flask_template/api/util.py`)
- Sphinx: [Changelog](https://www.sphinx-doc.org/en/master/changes.html)

### Removed

- Outdated type stubs for old dependencies
- Some unused imports


## [v0.1.0]

### Added
- Add inital flask template with documentation


[unreleased]: https://github.com/buehlefs/flask-template/compare/v0.4.1...HEAD
[v0.4.1]: https://github.com/buehlefs/flask-template/releases/tag/v0.4.1
[v0.4.0]: https://github.com/buehlefs/flask-template/releases/tag/v0.4.0
[v0.3.0]: https://github.com/buehlefs/flask-template/releases/tag/v0.3.0
[v0.2.0]: https://github.com/buehlefs/flask-template/releases/tag/v0.2.0
[v0.1.0]: https://github.com/buehlefs/flask-template/releases/tag/v0.1.0
