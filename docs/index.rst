.. image:: https://travis-ci.org/danbradham/psforms.svg
  :target: https://travis-ci.org/danbradham/psforms
  :alt: Build Status


.. image:: https://coveralls.io/repos/danbradham/psforms/badge.png
  :target: https://coveralls.io/r/danbradham/psforms
  :alt: Coverage Status

.. image:: https://img.shields.io/badge/pypi-0.1.0-brightgreen.svg
    :target: https://testpypi.python.org/pypi/psforms/
    :alt: Latest Version

=======
psforms
=======
Hassle free PySide forms.

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


    myform_dialog = MyForm.as_dialog()
    if myform_dialog.accepted:
        print dialog.get_value()


Features
========

* Easy Form creation

* Parent forms to your own window or use them as their own stand alone dialog

* Unified api for all standard PySide input widgets


Get psforms
===========

You can install psforms using pip::

    pip install psforms

or you can use setuptools::

    git clone git@github.com/danbradham/psforms.git
    cd psforms
    python setup.py install


Table of Contents
=================

.. toctree::
    :maxdepth: 2

    guide
    api
