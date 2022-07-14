Building firmware
====

.. _Dependencies:
.. _Building:


Based on the instructions from `PyCubed <https://pycubed.org/Building-the-PyCubed-Firmware-from-Source-edd6215b3d364fdf9dc4af67582c4006>`_ and
`CircuitPython <https://learn.adafruit.com/building-circuitpython/linux>`_.

Dependencies
------------

If you are not on Linux, follow the instructions at the above links.
For Ubuntu, the following packages are required:

You will need to install **build-essential**, **gettext**, and **uncrustify** by running::
    sudo apt install build-essential
    # The version of uncrustify you need is in a PPA:
    sudo add-apt-repository ppa:pybricks/ppa
    sudo apt install git gettext uncrustify

The Pycubed-Mini board uses a Cortex-M build. 
Therefore it will require the ARM Cortex-M toolchain.
Unfortunately, the ARM Cortex-M toolchain is not available through apt or snap.
To install download the `10-2020-q4-major <https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2?revision=ca0cbf9c-9de2-491c-ac48-898b5bbc0443&la=en&hash=68760A8AE66026BCF99F05AC017A6A50C6FD832A>`_ version.

Building
------------