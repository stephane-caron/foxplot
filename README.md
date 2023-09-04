# foxplot

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/CI.yml?branch=main)](https://github.com/stephane-caron/foxplot/actions)
[![Documentation](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/docs.yml?branch=main&label=docs)](https://stephane-caron.github.io/foxplot/)
[![Coverage](https://coveralls.io/repos/github/stephane-caron/foxplot/badge.svg?branch=main)](https://coveralls.io/github/stephane-caron/foxplot?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/foxplot)](https://pypi.org/project/foxplot/)

Plot time-series data from [newline-delimited JSON](https://en.wikipedia.org/wiki/JSON_streaming#Newline-delimited-JSON).

Foxplot stands for "Frequent Observation diXionary plots". Frequent observations arise from the project's initial use case with robot control loops, while dictionaries are a common weakly-typed self-describing format (used *e.g.* in the [GitHub REST API](https://docs.github.com/en/rest/), [robot logging](https://github.com/tasts-robots/mpacklog), ...).

## Installation

```console
pip install foxplot
```

## Usage

### Interactive mode

In interactive mode, you can explore the data in ``data`` (tab completion works) and plot it using the ``foxplot`` function:

```python
$ foxplot -i upkie_2023-05-03-103245.mpack
Python 3.8.10 (default, Mar 13 2023, 10:26:41)
Type 'copyright', 'credits' or 'license' for more information
IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: foxplot(
   ...:     [
   ...:         data.observation.servo.left_knee.torque,
   ...:         data.observation.servo.left_wheel.torque,
   ...:     ],
   ...:     right=[
   ...:         data.observation.servo.left_knee.velocity,
   ...:         data.observation.servo.left_wheel.velocity,
   ...:     ],
   ...: )
New tab opened in your web browser! The command line is to produce it directly is:

foxplot upkie_2023-05-03-103245.mpack -l /observation/servo/left_knee/torque /observation/servo/left_wheel/torque -r /observation/servo/left_knee/velocity /observation/servo/left_wheel/velocity
```

### Plotting from files

- JSON: ``foxplot my_data.json -l /observation/cpu_temperature``
- MessagePack: ``foxplot my_data.mpack -l /observation/cpu_temperature``

## Design notes

* Foxplot prioritizes ease-of-use (interactive mode) over performance

## Tips

* For Zsh users:

```zsh
zstyle ":completion:*:*:foxplot:*" ignored-patterns "^*.(json|mpack)"
```

## See also

* [µPlot](https://github.com/leeoniya/uPlot)'s performance was a key enabler for this project.
* [rq](https://github.com/dflemstr/rq/), a tool to manipulate streams of records in various formats.
