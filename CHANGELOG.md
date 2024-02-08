# Changelog

## [Unreleased]

### Changed

- Wrap render errors in `RenderError`.
- Renamed engine adapters from ${engine}Renderer to ${engine}Adapter.

### Added

- Add `remove_suffixes` optional parameter to `render()`.

### Fixed

- Fix template file name resolution for Jinja on Windows. 
- Don't try rendering file or directory if its name rendered empty.

## 0.1.0 - 2023-12-27

_The first release._