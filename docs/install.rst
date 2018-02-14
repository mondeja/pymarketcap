Install
=======

Dependencies
------------

You need to install `cython <http://cython.readthedocs.io/en/latest/src/quickstart/install.html>`__, and, optionally, `libcurl <https://curl.haxx.se/docs/install.html>`__ .

Without libcurl (light version)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    git clone https://github.com/mondeja/pymarketcap.git
    cd pymarketcap
    pip3 install Cython
    python setup.py install --no-curl

``urllib`` will be used instead.

With libcurl
^^^^^^^^^^^^

::

    pip3 install https://github.com/mondeja/pymarketcap/archive/master.zip

or from source as above wihout ``--no-curl`` flag.