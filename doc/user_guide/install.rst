#######
Install
#######

You need to install `cython <http://cython.readthedocs.io/en/latest/src/quickstart/install.html>`__ before pymarketcap. Try: ``pip3 install Cython`` and then:

::

    pip3 install pymarketcap

- On Windows will be used ``urllib`` library to make synchronous requests and on Linux/Mac will be build against `libcurl <https://curl.haxx.se/docs/install.html>`__ C library. You can control this (see below):


***********
From source
***********

::

    git clone https://github.com/mondeja/pymarketcap.git
    cd pymarketcap
    pip3 install -r requirements.txt
    python setup.py install

- To force installation with libcurl, use ``--force-curl`` in last command.
- To install with urllib, use ``--no-curl``.


