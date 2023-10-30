# foxplot

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/CI.yml?branch=main)](https://github.com/stephane-caron/foxplot/actions)
[![Documentation](https://img.shields.io/github/actions/workflow/status/stephane-caron/foxplot/docs.yml?branch=main&label=docs)](https://stephane-caron.github.io/foxplot/)
[![Coverage](https://coveralls.io/repos/github/stephane-caron/foxplot/badge.svg?branch=main)](https://coveralls.io/github/stephane-caron/foxplot?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/foxplot)](https://pypi.org/project/foxplot/)

Plot time series from [newline-delimited JSON](https://en.wikipedia.org/wiki/JSON_streaming#Newline-delimited-JSON).

## Installation

```console
pip install foxplot
```

## Usage

Foxplot starts in interactive mode by default, which allows us to explore the input gathered in the ``data`` object (tab completion works: type ``data.<TAB>`` to explore) and plot times series from it using the ``fox.plot`` function:

```python
$ foxplot upkie_2023-05-03-103245.mpack
Python 3.8.10 (default, Mar 13 2023, 10:26:41)
Type 'copyright', 'credits' or 'license' for more information
IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: fox.plot(data.observation.imu.angular_velocity)
```

This call will open a new tab in your browser with a plot of the time series. In this example, ``angular_velocity`` is a 3D vector, thus the plot will include three curves.

### Plotting from files

We can also plot data from files and pipes directly, for example:

- JSON: ``foxplot my_data.json -l /observation/cpu_temperature``
- MessagePack: ``foxplot my_data.mpack -l /observation/cpu_temperature``

### Richer plot

Here is a more complex plot with both left- and right-axis time series:

```
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

This call will output a command line to directly reproduce the plot:

```
The command line to generate this plot is:

foxplot upkie_2023-05-03-103245.mpack -l /observation/servo/left_knee/torque /observation/servo/left_wheel/torque -r /observation/servo/left_knee/velocity /observation/servo/left_wheel/velocity
```

Check out the other arguments to ``fox.plot``, for instance in the IPython shell by ``fox.plot?``.

## Tips

Zsh users can filter foxplot completion on JSON and MessagePack files:

```zsh
zstyle ":completion:*:*:foxplot:*" ignored-patterns "^*.(json|mpack)"
```

## See also

* [µPlot](https://github.com/leeoniya/uPlot)'s performance was a key enabler for this project.
* [rq](https://github.com/dflemstr/rq/), a tool to manipulate streams of records in various formats.
