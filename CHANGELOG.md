# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2023/05/23

### Added

- Export ``data`` in interactive mode
- Plot function now has a ``time`` keyword argument
- Usage message in interactive mode

### Changed

- Can now set time from label or series data
- Switch to interactive mode by default when there is nothing to plot

### Fixed

- Use ``None`` as the default (undefined) time key

## [0.0.2] - 2023/05/02

### Added

- MessagePack support

## [0.0.1] - 2023/04/25

### Added

- Command-line interface
- Generate plot as a temporary HTML page
- Internal: Color picker
- Internal: Custom exceptions
- Internal: Logging with an spdlog-like format
- Python interactive shell
