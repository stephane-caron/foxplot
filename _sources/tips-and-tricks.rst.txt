***************
Tips and tricks
***************

Plotting from files
===================

It is also possible to plot data from files and pipes directly. For instance for JSON:

.. code:: console

    foxplot my_data.json -l /observation/cpu_temperature

And for MessagePack:

.. code:: console

   foxplot my_data.mpack -l /observation/cpu_temperature

Shell completion
================

Zsh users can filter foxplot completion on JSON and MessagePack files:

.. code:: zsh

    zstyle ":completion:*:*:foxplot:*" ignored-patterns "^*.(json|mpack)"
