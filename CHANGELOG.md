# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [v0.2.0]

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
[v0.2.0]: https://github.com/buehlefs/flask-template/resleases/tag/v0.2.0
[v0.1.0]: https://github.com/buehlefs/flask-template/resleases/tag/v0.1.0
