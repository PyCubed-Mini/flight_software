Building firmware
====

.. _Dependencies:
.. _Building:


Based on the instructions from `PyCubed <https://pycubed.org/Building-the-PyCubed-Firmware-from-Source-edd6215b3d364fdf9dc4af67582c4006>`_ and
`CircuitPython <https://learn.adafruit.com/building-circuitpython/linux>`_.
CircuitPython is meant to be built in a Unix (Linux, Mac, etc.) environment.
While it is possible to build on Windows with the appropriate workarounds, it is not recommended.

Dependencies
------------

If you are not on Linux, follow the instructions at the above links.
For Ubuntu, the following packages are required:

You will need to install **build-essential**, **gettext**, and **uncrustify** by running

.. code-block:: console

    $ sudo apt install build-essential
    $ # The version of uncrustify you need is in a PPA:
    $ sudo add-apt-repository ppa:pybricks/ppa
    $ sudo apt install git gettext uncrustify

The Pycubed-Mini board uses a Cortex-M build. 
Therefore it will require the ARM Cortex-M toolchain.
Unfortunately, the ARM Cortex-M toolchain is not available through apt or snap.
To install download the `10-2020-q4-major <https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2?revision=ca0cbf9c-9de2-491c-ac48-898b5bbc0443&la=en&hash=68760A8AE66026BCF99F05AC017A6A50C6FD832A>`_ version.

Then extract it somewhere and add the following to your `.bashrc` (make sure to modify the path as required)

.. code-block:: console

    $ export PATH="$PATH:/home/user/path/to/gcc-arm-none-eabi-10-2020-q4-major/bin/"

Building
------------

First fetch the code required to build. 
This should take a while, as many submodules are being donwloaded.

.. code-block:: console

    $ git clone https://github.com/adafruit/circuitpython.git
    $ cd circuitpython
    $ make fetch-submodules

Then install the required python dependencies

.. code-block:: console

    $ pip3 install --upgrade -r requirements-dev.txt
    $ pip3 install --upgrade -r requirements-doc.txt

Then build the mpy-cross compiler via

.. code-block:: console

    $ make -C mpy-cross

Then download the pycubed-mini v3 firmware from `here <https://github.com/PyCubed-Mini/avionics-motherboard/tree/main/firmware/pycubedminiv03/firmware_build>`_.
Then create a `pycubed-mini` folder in the `ports/atmel-samd/boards` directory.
Then place the firmware in the `pycubed-mini` folder.

Finally run the following command to build the firmware

.. code-block:: console

    $ cd ports/atmel-samd
    $ make BOARD=pycubed-mini