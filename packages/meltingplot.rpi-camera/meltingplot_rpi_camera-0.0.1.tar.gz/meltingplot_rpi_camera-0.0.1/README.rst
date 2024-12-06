MeltingPlot RPi Camera
======================

Overview
--------

MeltingPlot RPi Camera is a Python project designed to interface with a Raspberry Pi camera module.
It captures images and videos, processes them, and provides various functionalities for image analysis
and manipulation.

Features
--------

- Capture images and videos
- Image processing and analysis
- Integration with Raspberry Pi camera module
- Easy-to-use interface

Installation
------------

To install the required dependencies, run:

.. code-block:: bash

    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y python3-picamera2
    python3 -m venv --system-site-packages venv
    source venv/bin/activate
    pip install meltingplot.rpi_camera
    sudo rpi-camera install

Usage
-----

To start streaming images, run:

.. code-block:: bash

    sudo rpi-camera start

or as a service:

.. code-block:: bash

    sudo systemctl start rpi-camera

Contributing
------------

Contributions are welcome! Please fork the repository and submit a pull request.

License
-------

This project is licensed under the Apache 2.0 License. See the LICENSE file for more details.

Contact
-------

For any questions or inquiries, please contact Tim at tim@meltingplot.net