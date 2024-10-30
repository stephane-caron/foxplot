# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-10-30

### Added

- Function: lag estimator
- Function: low-pass filter
- docs: Functions page
- docs: Interactive-mode page
- docs: Tips-and-tricks page

### Removed

- Remove `print_command_line` argument from `Fox.plot`
- Remove µPlot source from distribution

## [0.7.0] - 2024-10-28

### Added

- Function: Absolute value

### Fixed

- Allow input files with string values

## [0.6.0] - 2024-06-17

### Added

- Feature: calculation of sums and products between series
- Function: Windowed standard deviations
- Separate classes for "hot" (reading the input) and "frozen" series
- Start a functions submodule for commonly used functions

### Changed

- Bump required Python version to 3.8
- Rename and specialize ``get_series`` to ``get_frozen_series``
- Value type for frozen series switched to NumPy arrays

### Fixed

- Make sure frozen series at leaves are floating-point valued
- Type annotations for NumPy arrays

### Removed

- Replace ``_get(n)`` method by ``_values`` in frozen series

## [0.5.0] - 2023-11-01

### Added

- Allow single-series right plots
- Argument ``print_command_line`` to plotting function

### Changed

- CLI: Revert to `fox.plot` for better docs and discoverability
- Rename internal ``IndexedSeries`` to just ``Series``
- Repeat previous value when there is a gap in the input

### Removed

- Argument ``open_new_tab`` to plotting function

## [0.4.0] - 2023-10-23

### Added

- Automatic plot title from log file name
- Plotting a internal node plots all indexed series within (non-recursively)
- Warn when trying to plot structured data

### Changed

- Node labels are internal (not exposed to TAB completion)

## [0.3.0] - 2023-09-04

### Added

- Allow single-series left plots
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

[unreleased]: https://github.com/stephane-caron/foxplot/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/stephane-caron/foxplot/compare/v0.7.0...v1.0.0
[0.7.0]: https://github.com/stephane-caron/foxplot/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/stephane-caron/foxplot/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/stephane-caron/foxplot/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/stephane-caron/foxplot/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/stephane-caron/foxplot/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/stephane-caron/foxplot/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/stephane-caron/foxplot/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/stephane-caron/foxplot/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/stephane-caron/foxplot/releases/tag/v0.0.1
