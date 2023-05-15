*****
Usage
*****

Interactive mode
================

In interactive mode, you can explore the data in ``data`` (tab completion works) and plot it using the ``fox.plot`` function:

.. code:: console

    $ foxplot -i upkie_2023-05-03-103245.mpack
    Python 3.8.10 (default, Mar 13 2023, 10:26:41)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: fox.plot(
       ...:     [
       ...:         data.observation.servo.left_knee.torque,
       ...:         data.observation.servo.left_wheel.torque,
       ...:     ],
       ...:     right=[
       ...:         data.observation.servo.left_knee.velocity,
       ...:         data.observation.servo.left_wheel.velocity,
       ...:     ],
       ...: )

Plotting from files
===================

- JSON: ``foxplot my_data.json -l /observation/cpu_temperature``
- MessagePack: ``foxplot my_data.mpack -l /observation/cpu_temperature``
