# Changelog

# [Unreleased]

### Changed

- Re-licensed as BSD 3-Clause.
- Deprecated the `render` function in favour of the new `TreeTemplate.render`.

### Added

- Add parameter type to the TypeError thrown when the input is not Iterable.
- Accept a report callback, called for every written file.

### Fixed

- Create parent directories

# 0.2.1 - 2024-02-09

### Fixed

- Fix configuring JinjaAdapter when an instance of Environment is passed.

## 0.2.0 - 2024-02-09

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

## 0.1.0 - 2023-12-27

_The first release._
