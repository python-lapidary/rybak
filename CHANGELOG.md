# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for multiple template roots. Breaking change: MakoAdapter now accepts `Iterable[Path]`.
- Raise error when a file is created more than once. Allow adjustment with a callback.

### Removed
- Support for python 3.8 .


## [0.4.0] - 2024-06-25

### Removed

- Removed deprecated `render` function.

### Fixed

- When rendering with `remove_stale`, do not try removing target root or non-empty directories.


# [0.3.0] - 2024-02-24

### Changed

- Re-licensed as BSD 3-Clause.
- Deprecated the `render` function in favour of the new `TreeTemplate.render`.

### Added

- Add parameter type to the TypeError thrown when the input is not Iterable.
- Accept a report callback, called for every written file.

### Fixed

- Create parent directories

# [0.2.1] - 2024-02-09

### Fixed

- Fix configuring JinjaAdapter when an instance of Environment is passed.

## [0.2.0] - 2024-02-09

### Changed

- Wrap render errors in `RenderError`.
- Rename engine adapters from ${engine}Renderer to ${engine}Adapter.
- Reorder `render()` parameters to follow `source, target, options`.
- Rename parameter `excluded` to `exclude` and set default to `__pycache__`.

### Added

- Add `remove_suffixes` and `exclude_extend` optional parameters to `render()`.

### Removed

- Remove support for tornado.
- Remove `template_root` parameter from `redner()` - it's taken from the `adapter`.

### Fixed

- Fix template file name resolution for Jinja on Windows.
- Don't try rendering file or directory if its name rendered empty.

## [0.1.0] - 2023-12-27

_The first release._

[unreleased]: https://github.com/python-lapidary/rybak/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/python-lapidary/rybak/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/python-lapidary/rybak/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/python-lapidary/rybak/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/python-lapidary/rybak/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/python-lapidary/rybak/releases/tag/v0.1.0
