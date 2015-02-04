.. image:: https://travis-ci.org/danbradham/apptemplate.svg
  :target: https://travis-ci.org/danbradham/apptemplate
  :alt: Build Status


.. image:: https://coveralls.io/repos/danbradham/apptemplate/badge.png
  :target: https://coveralls.io/r/danbradham/apptemplate
  :alt: Coverage Status

.. image:: https://img.shields.io/badge/pypi-0.1.4-brightgreen.svg
    :target: https://testpypi.python.org/pypi/apptemplate/
    :alt: Latest Version

=======
psforms
=======
PySide forms. Hassle-free.

Provides a unified api for all standard PySide input widgets. Making it
possible to map python standard types to controls.

::

    import psforms
    from psforms import Form, Field

    class MyForm(Form):
        '''My amazing form, useful in many scenarios.'''

        title = 'My Form'
        mapping = psforms.STANDARD
        int_field = Field('Integer Value', 20)
        str_field = Field('String Value', ['Item A', 'Item B', 'Item C'])
        bool_field = Field('Boolean Value', False)
        strb_field = Field('String Value B', '')

Features
========

* Super simple forms

* Unified API

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


Documentation
=============

For more information visit the `docs <http://psforms.readthedocs.org>`_.
