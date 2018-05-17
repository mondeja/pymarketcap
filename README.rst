pymarketcap
===========


|TravisCI| |AppVeyor| |Status|

|ReadTheDocs| |Binder|

|PyPI| |PyPI-Versions| |LICENSE|


pymarketcap is a library for retrieve data from
`coinmarketcap <http://coinmarketcap.com/>`__ API and website. Consist
of a cythonized scraper and and API wrapper built with libcurl, but is
posible to compile a lightweight version with standard ``urllib``

New version 4.0.0
-----------------

- See `changelog <http://pymarketcap.readthedocs.io/dev_guide/changelog.html>`__ for more details.

This new version introduce some breaking changes (see `Documentation reference <http://pymarketcap.readthedocs.io/reference.html>`__).


Install
=======

You need to install `cython <http://cython.readthedocs.io/en/latest/src/quickstart/install.html>`__ before pymarketcap. Try: ``pip3 install Cython`` and then:

::

   pip3 install pymarketcap

- On Windows will be used ``urllib`` library to make synchronous requests and on Linux/Mac will be build against `libcurl <https://curl.haxx.se/docs/install.html>`__ C library. You can control this (see below):


From source
-----------

::

   git clone https://github.com/mondeja/pymarketcap.git
   cd pymarketcap
   pip3 install -r requirements.txt
   python setup.py install

- To force installation with libcurl, use ``--force-curl`` in last command.
- To install with urllib, use ``--no-curl``.


Documentation
-------------
- `Static documentation at Readthedocs <https://pymarketcap.readthedocs.io>`__.
- `Live running notebook hosted at Binderhub <https://mybinder.org/v2/gh/mondeja/pymarketcap/master?filepath=docs%2Fsync_live.ipynb>`__.

`Contributing <https://github.com/mondeja/pymarketcap/blob/master/doc/dev_guide/contributing.rst>`__
------------------------------------------------------------------------------------------

`Testing <https://github.com/mondeja/pymarketcap/blob/master/doc/dev_guide/testing.rst>`__
--------------------------------------------------------------------------------

`Changelog <https://cnhv.co/1y9ex>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`License <https://cnhv.co/1xgxi>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Support
~~~~~~~

- Issue Tracker: https://github.com/mondeja/pymarketcap/issues
- |Ask me anything| mondejar1994@gmail.com



.. |TravisCI| image:: https://travis-ci.org/mondeja/pymarketcap.svg?branch=master
   :target: https://cnhv.co/1xgw5
.. |PyPI| image:: https://img.shields.io/pypi/v/pymarketcap.svg
   :target: https://cnhv.co/1xgwg
.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/pymarketcap.svg
   :target: https://cnhv.co/1xgwm
.. |Binder| image:: https://mybinder.org/badge.svg
   :target: https://cnhv.co/1y9ff
.. |Status| image:: https://img.shields.io/pypi/status/pymarketcap.svg
   :target: https://cnhv.co/1xgwm
.. |ReadTheDocs| image:: https://readthedocs.org/projects/pymarketcap/badge/?version=latest
   :target: https://cnhv.co/1xgx1
.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/puy2p0qhjna4hosc?svg=true
   :target: https://cnhv.co/1xgx7
.. |LICENSE| image:: https://img.shields.io/pypi/l/pymarketcap.svg
   :target: https://cnhv.co/1xgxd
.. |Ask me anything| image:: https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg


