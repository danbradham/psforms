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


Documentation
=============

For more information visit the `docs <http://psforms.readthedocs.org>`_.
