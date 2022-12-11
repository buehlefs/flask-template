# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

- Recommonmark markdown parser configuration for documentation (use the MyST parser instead)

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

[unreleased]: https://github.com/buehlefs/flask-template/compare/v0.2.0...HEAD
[v0.2.0]: https://github.com/buehlefs/flask-template/releases/tag/v0.2.0
[v0.1.0]: https://github.com/buehlefs/flask-template/releases/tag/v0.1.0
