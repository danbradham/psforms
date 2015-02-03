.. image:: https://travis-ci.org/danbradham/apptemplate.svg
  :target: https://travis-ci.org/danbradham/apptemplate
  :alt: Build Status


.. image:: https://coveralls.io/repos/danbradham/apptemplate/badge.png
  :target: https://coveralls.io/r/danbradham/apptemplate
  :alt: Coverage Status

.. image:: https://img.shields.io/badge/pypi-0.1.4-brightgreen.svg
    :target: https://testpypi.python.org/pypi/apptemplate/
    :alt: Latest Version

============
PySide Forms
============
Forms in PySide without hassle.

Provides a unified api for all standard PySide input widgets. Making it
possible to map python dictionaries to forms.

::

    import psforms

    MyForm = psforms.Form(
        intvalue=('Integer Value', 20),
        strvalue=('String Value', ['Item A', 'Item B', 'Item C']),
        boolvalue=('Boolean Value', False),
        strvalueb=('String Value B', ''),
    )

    filled_out = MyForm.as_dialog()
    if filled_out:
        print MyForm.get_value()


Features
========

* Super simple forms

* Unified control api

* Parent forms to your own window or use them as their own stand alone dialog


Get psforms
===========

PyPa
----
psforms is available through the python package index as **psforms**.

::

    pip install psforms

Distutils/Setuptools
--------------------

::

    git clone git@github.com/danbradham/psforms.git
    cd psforms
    python setup.py install


Table of Contents
=================

.. toctree::
    :maxdepth: 2

    guide
    api
