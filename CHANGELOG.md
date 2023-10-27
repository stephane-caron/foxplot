# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Rename internal ``IndexedSeries`` to just ``Series``
- Repeat previous value when there is a gap in the input

## [0.4.0] - 2023-10-23

### Added

- Automatic plot title from log file name
- Plotting a internal node plots all indexed series within (non-recursively)
- Warn when trying to plot structured data

### Changed

- Node labels are internal (not exposed to TAB completion)

## [0.3.0] - 2023-09-04

### Added

- Allow single-series plots
- Detect time key from root keys in the input
- Length attribute to indexed series

### Changed

- CLI: Expose `foxplot` function rather than a fox instance
- CLI: Expose `set_time` function
- Put filename at the end of suggested command line
- Removed `time` argument from the plot function
- Rephrase command-line hint

## [0.2.0] - 2023-08-08

### Added

- CI workflow checking that PyPI package installation upon new releases

### Changed

- Increase time precision from 3 to 4 significant digits
- Keep ordered axis labels for plot color consistency (thanks to @boragokbakan)

### Fixed

- Consistent key order between plots of the same log (thanks to @boragokbakan)

## [0.1.0] - 2023-05-23

### Added

- Export ``data`` in interactive mode
- Plot function now has a ``time`` keyword argument
- Usage message in interactive mode

### Changed

- Can now set time from label or series data
- Switch to interactive mode by default when there is nothing to plot

### Fixed

- Use ``None`` as the default (undefined) time key

## [0.0.2] - 2023-05-02

### Added

- MessagePack support

## [0.0.1] - 2023-04-25

### Added

- Command-line interface
- Generate plot as a temporary HTML page
- Internal: Color picker
- Internal: Custom exceptions
- Internal: Logging with an spdlog-like format
- Python interactive shell

[unreleased]: https://github.com/stephane-caron/foxplot/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/stephane-caron/foxplot/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/stephane-caron/foxplot/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/stephane-caron/foxplot/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/stephane-caron/foxplot/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/stephane-caron/foxplot/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/stephane-caron/foxplot/releases/tag/v0.0.1
