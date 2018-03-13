.. raw:: html

   <h1>

pymarketcap

.. raw:: html

   </h1>

|Build Status| |AppVeyor| |ReadTheDocs| |Binder|

|PyPI| |PyPI Versions| |LICENSE|

**pymarketcap** is a library for retrieve data from
`coinmarketcap <http://coinmarketcap.com/>`__ API and website. Consist
of a cythonized scraper and and API wrapper built with libcurl, but is
posible to compile a lightweight version with standard ``urllib``
library instead. Only works in Python3.6+

.. code:: diff

    + New version 3.9.0 (unstable)
    - Some breaking changes have been introduced since 3.9.0 version. The old version (3.3.158) is still hosted at Pypi and will be there for a short period of time but won't be longer supported. The new stable version will be 4.0.0. Please, update to the new version, is faster, more accurate and has new features!

Install
-------

Dependencies
~~~~~~~~~~~~

You need to install `cython <http://cython.readthedocs.io/en/latest/src/quickstart/install.html>`__ and, optionally, `libcurl <https://curl.haxx.se/docs/install.html>`__.

Without libcurl
^^^^^^^^^^^^^^^

::

    git clone https://github.com/mondeja/pymarketcap.git
    cd pymarketcap
    pip3 install -r requirements.txt
    python setup.py install --no-curl

``urllib`` will be used instead.

In Windows this is the default behaviour, although ``--no-curl`` flag it's specified. If you want try to install with ``curl`` in Windows use ``python setup.py install --force-curl``.

With libcurl
^^^^^^^^^^^^

::

    pip3 install https://github.com/mondeja/pymarketcap/archive/master.zip

or from source as above wihout ``--no-curl`` flag.

Documentation
-------------
- `Live running notebook hosted at Binderhub <https://mybinder.org/v2/gh/mondeja/pymarketcap/master?filepath=docs%2Fsync_live.ipynb>`__.
- `Static documentation at Readthedocs <https://cnhv.co/1y9f0>`__.

`Contributing and testing <https://github.com/mondeja/pymarketcap/blob/master/CONTRIBUTING.rst>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Changelog <https://cnhv.co/1y9ex>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

--------------

`License <https://cnhv.co/1xgxi>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Support
~~~~~~~

-  Issue Tracker: https://github.com/mondeja/pymarketcap/issues
-  If you want contact me → mondejar1994@gmail.com

--------------

Buy me a coffee?
^^^^^^^^^^^^^^^^

If you feel like buying me a coffee (or a beer?), donations are welcome:

::

    BTC: 1LnPPp7nEF7fHNMtHvVaEFNaHmPKji1uCo
    BCH: qp40gr5y9usdyqh62hac7umvcqe5n2nc9vpff4der5
    ETH: 0x3284674cC02d18395a00546ee77DBdaA391Aec23
    LTC: LXSXiczN1ZYyf3WoeawraL7G1d31vVWgXK
    STEEM: @mondeja

.. |Build Status| image:: https://travis-ci.org/mondeja/pymarketcap.svg?branch=master
   :target: https://cnhv.co/1xgw5
.. |PyPI| image:: https://img.shields.io/pypi/v/pymarketcap.svg
   :target: https://cnhv.co/1xgwg
.. |PyPI Versions| image:: https://img.shields.io/pypi/pyversions/pymarketcap.svg
   :target: https://cnhv.co/1xgwm
.. |Binder| image:: https://mybinder.org/badge.svg
   :target: https://cnhv.co/1y9ff
.. |ReadTheDocs| image:: https://readthedocs.org/projects/pymarketcap/badge/?version=latest
   :target: https://cnhv.co/1xgx1
.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/puy2p0qhjna4hosc?svg=true
   :target: https://cnhv.co/1xgx7
.. |LICENSE| image:: https://img.shields.io/pypi/l/pymarketcap.svg
   :target: https://cnhv.co/1xgxd