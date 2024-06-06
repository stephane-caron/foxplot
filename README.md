# foxplot

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/ci.yml?branch=main)](https://github.com/stephane-caron/foxplot/actions)
[![Documentation](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/docs.yml?branch=main&label=docs)](https://stephane-caron.github.io/foxplot/)
[![Coverage](https://coveralls.io/repos/github/stephane-caron/foxplot/badge.svg?branch=main)](https://coveralls.io/github/stephane-caron/foxplot?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/foxplot)](https://pypi.org/project/foxplot/)

Plot time series from [newline-delimited JSON](https://en.wikipedia.org/wiki/JSON_streaming#Newline-delimited-JSON).

## Installation

```console
pip install foxplot
```

## Usage

Foxplot starts in interactive mode by default to explore the input gathered in ``data`` (tab completion works: try ``data.<TAB>``). Plot times series using the ``fox.plot`` function, for example:

```python
$ foxplot upkie_2023-05-03-103245.mpack
Python 3.8.10 (default, Mar 13 2023, 10:26:41)
Type 'copyright', 'credits' or 'license' for more information
IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: fox.plot(data.observation.imu.angular_velocity)
```

This call opens a new tab in your browser with the desired plot. In this example, ``angular_velocity`` is a 3D vector, thus the plot will include three curves.

### Left and right axes

Here is a plot with both left- and right-axis time series:

```python
In [2]: fox.plot(
   ...:     [
   ...:         data.observation.servo.left_knee.position,
   ...:         data.observation.servo.left_wheel.position,
   ...:     ],
   ...:     right=[
   ...:         data.observation.servo.left_knee.velocity,
   ...:         data.observation.servo.left_wheel.velocity,
   ...:     ],
   ...:     left_axis_unit="rad",
   ...:     right_axis_unit="rad/s",
   ...:     print_command_line=True,
   ...: )
```

Check out the other arguments to ``fox.plot`` in its documentation (IPython: ``fox.plot?``).

### Computing new series

Time series are labeled NumPy arrays, and can be manipulated as such. For example:

```python
In [1]: left_knee = data.observation.servo.left_knee

In [2]: left_knee_power = left_knee.torque * left_knee.velocity

In [3]: fox.plot(left_knee_power, right=[left_knee.velocity])
```

### Plotting from files

We can also plot data from files and pipes directly, for example:

- JSON: ``foxplot my_data.json -l /observation/cpu_temperature``
- MessagePack: ``foxplot my_data.mpack -l /observation/cpu_temperature``

## Tips

Zsh users can filter foxplot completion on JSON and MessagePack files:

```zsh
zstyle ":completion:*:*:foxplot:*" ignored-patterns "^*.(json|mpack)"
```

## See also

* [µPlot](https://github.com/leeoniya/uPlot): time-series plotting library, whose performance was a key enabler for this project.
- [mpacklog.cpp](https://github.com/upkie/mpacklog.cpp): library to log dictionaries to MessagePack files in C++.
- [mpacklog.py](https://github.com/upkie/mpacklog.py): library and command-line tools to log dictionaries to MessagePack files in Python.
* [rq](https://github.com/dflemstr/rq/): command-line tool to manipulate streams of records in various formats.
