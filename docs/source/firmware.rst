Building firmware
====

.. _Dependencies:
.. _Building:


Based on the instructions from `PyCubed <https://pycubed.org/Building-the-PyCubed-Firmware-from-Source-edd6215b3d364fdf9dc4af67582c4006>` and
`CircuitPython <https://learn.adafruit.com/building-circuitpython/linux>`.

Dependencies
------------

If you are not on Linux, follow the instructions at the above links.
For Ubuntu, the following packages are required:

You will need to install **build-essential**, **gettext**, and **uncrustify** by running::
    sudo apt install build-essential
    # The version of uncrustify you need is in a PPA:
    sudo add-apt-repository ppa:pybricks/ppa
    sudo apt install git gettext uncrustify

Building
------------