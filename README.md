# foxplot

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/ci.yml?branch=main)](https://github.com/stephane-caron/foxplot/actions)
[![Documentation](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/docs.yml?branch=main&label=docs)](https://stephane-caron.github.io/foxplot/)
[![Coverage](https://coveralls.io/repos/github/stephane-caron/foxplot/badge.svg?branch=main)](https://coveralls.io/github/stephane-caron/foxplot?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/foxplot)](https://pypi.org/project/foxplot/)

Manipulate time series read from [MessagePack](https://msgpack.org/) or [newline-delimited JSON](https://en.wikipedia.org/wiki/JSON_streaming#Newline-delimited-JSON).

## Installation

```console
pip install foxplot
```

## Usage

The `foxplot` command-line tool starts in interactive mode by default to explore the input gathered in `data` (tab completion works: try `data.<TAB>`). Plot times series using the `fox.plot` function, for example:

```python
$ foxplot upkie_2023-05-03-103245.mpack
Python 3.8.10 (default, Mar 13 2023, 10:26:41)
Type 'copyright', 'credits' or 'license' for more information
IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: fox.plot(data.observation.imu.angular_velocity)
```

This call opens a new tab in your browser with the desired plot. In this example, `angular_velocity` is a 3D vector, thus the plot will include three curves.

Check out the [documentation](https://stephane-caron.github.io/foxplot/) for more advanced examples, such as left and right axes or computing new series from existing ones.

## See also

- [mpacklog.cpp](https://github.com/stephane-caron/mpacklog.cpp): library to log dictionaries to MessagePack files in C++.
- [mpacklog.py](https://github.com/stephane-caron/mpacklog.py): library and command-line tools to log dictionaries to MessagePack files in Python.
- [rq](https://github.com/dflemstr/rq/): command-line tool to manipulate streams of records in various formats.
- [uplot-python](https://github.com/stephane-caron/uplot-python): plotting backend used in this project.
- [µPlot](https://github.com/leeoniya/uPlot): time-series plotting library, whose performance was a key enabler for this project.
