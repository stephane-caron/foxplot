****************
Interactive mode
****************

The `foxplot` command-line tool starts in interactive mode by default to explore the input gathered in `data` (tab completion works: try `data.<TAB>`). Plot times series using the `fox.plot` function, for example:

.. code:: console

    $ foxplot upkie_2023-05-03-103245.mpack
    Python 3.8.10 (default, Mar 13 2023, 10:26:41)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: fox.plot(data.observation.imu.angular_velocity)

This call opens a new tab in your browser with the desired plot. In this example, `angular_velocity` is a 3D vector, thus the plot will include three curves.

Plotting left and right
=======================

You can explore the data in ``data`` (tab completion works) and plot it left and right using ``fox.plot``:

.. code:: python

    In [2]: fox.plot(
       ...:     [
       ...:         data.observation.servo.left_knee.torque,
       ...:         data.observation.servo.left_wheel.torque,
       ...:     ],
       ...:     right=[
       ...:         data.observation.servo.left_knee.velocity,
       ...:         data.observation.servo.left_wheel.velocity,
       ...:     ],
       ...: )

Check out the other arguments to `fox.plot` in its documentation (IPython: `fox.plot?`).

Computing new series
====================

Time series are labeled NumPy arrays, and can be manipulated as such. For example:

.. code:: python

    In [1]: left_knee = data.observation.servo.left_knee

    In [2]: left_knee_power = left_knee.torque * left_knee.velocity

    In [3]: fox.plot(left_knee_power, right=[left_knee.velocity])

Foxplot also provides :ref:`functions` for more complex operations on time series.
