.. image:: https://readthedocs.org/projects/psforms/badge/?version=latest?style=flat-square
    :target: https://readthedocs.org/projects/psforms/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/psforms.svg?style=flat-square
    :target: https://pypi.python.org/psforms
    :alt: Latest Version

=======
psforms
=======
Hassle free PySide forms.

::

    from psforms import (Form, IntField, StringField,
                         StringOptionField, BoolField)


    class MyForm(Form):
        '''My amazing form, useful in many scenarios.'''

        title = 'My Form'
        int_field = IntField('Integer Value')
        str_field = StringOptionField('String Value', options=['A', 'B', 'C'])
        bool_field = BoolField('Boolean Value')
        strb_field = StringField('String Value B')


    myform_dialog = MyForm.as_dialog()
    if myform_dialog.exec_():
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
