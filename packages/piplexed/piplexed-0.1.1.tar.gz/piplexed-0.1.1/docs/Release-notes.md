# Release Notes

## 0.1.1

### Fixed

- Github repo link in `pyproject.toml` was wrong so links on PyPI returned a **404** error.


## 0.1.0

### Fixed

- If a non-PyPI package (for example a local wheel) is installed with pipx, a `NoSuchProjectError` results due it not being on PyPI. This has been resolved by using the pipx metadata json file to determine if the package was installed from a non-PyPi source and not request it's details from PyPI
- Various linitng and mypy errors have been squashed.



### Added

- A user cache directory has been added using [platformdirs](https://github.com/platformdirs/platformdirs) to cache PyPI responses
- Added [nox](https://github.com/wntrblm/nox) as test and lint runner
- Added github actions for linting and tests

### Changed

- `remove_expired_responses()` is being depracted in `requests-cache` this has been replaced with `cache.delete(expired=True)`



##  0.0.2

🔼 Upgrade pypi-simple to 1.1.0 for PEP 700 support.

