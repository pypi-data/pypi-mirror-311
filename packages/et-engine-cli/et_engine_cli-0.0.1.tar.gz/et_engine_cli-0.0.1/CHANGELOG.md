# Change Log

## [0.0.1] - 2024-11-26

New features for interacting with Batch objects, plus other minor features and bug fixes.

### Added

- `batches` command group
- `delete` methods for all command groups (`filesystems`, `tools`, and `batches`)

### Changed

- Updated docs structure to include batches and simplify the some redundant links

### Fixed

- Bug that caused an error on `et filesystems list`
- Syntax errors preventing `et filesystems create` from working
- Updated outdated syntax for HTTP API causing errors on `et tools create` and other methods
