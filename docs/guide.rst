.. _guide:
.. currentmodule:: psforms

=====
Guide
=====
This guide will walk you through using psforms. Let's start by expanding on the example from the ReadMe.

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

The :class:`psforms.Form` is a factory for creating various types of forms.
:class:`psforms.Field` attributes are used to describe a label and it's default value. The ``mapping`` attribute is used to map the defaul value type to an appropriate control. The default ``mapping`` is psforms.STANDARD, I've included it here for clarity. :class:`psforms.Form` subclasses are only skeletons of a widget, waiting to be created. To create an actual form widget, use one of following methods, all of which start with the prefix **as_**.

Forms as Dialogs
================
::

    myform_dialog = MyForm.as_dialog()
    if myform_dialog.accepted:
        print dialog.get_value()

The :meth:`as_dialog` returns a :class:`psforms.Dialog` instance with the
fields specified in :class:`MyForm`. :class:`psforms.Dialog` accepts two
keyword arguments; columns and parent. :meth:`get_value` returns a dictionary of names and values for all the fields in MyForm. In this next example
``ParentWidget`` refers to a parent applications :class:`QtGui.QWidget` or
:class:`QtGui.QMainWindow`.

::

    myform_dialog = MyForm.as_dialog(columns=2, parent=ParentWidget)

The previous examples create a modal dialog, which blocks all other PySide
widgets from receiving input until after the dialog is accepted or rejected.
Pass the False to the keyword argument modal to retrieve a non-blocking dialog.


Forms as Widgets and Groups
===========================
You can also get a Form as a mulit-column :class:`psforms.Widget` or
:class:`psforms.Group`.

::

    myform_widget = MyForm.as_widget(columns=2)
    myform_group = MyForm.as_group(columns=1, collapsable=True)

The above :class:`psforms.Widget` and :class:`psforms.Group` are derived from
a standard :class:`QtGui.QWidget` and a standard :class:`QtGui.QGroupBox`; therefore, they can be added to any PySide layout. The collapsable parameter
refers to whether or not the entire :class:`psforms.Group` can be collapsed. Both of these also have a :meth:`get_value` like the dialog above.


Getting the value of a control
==============================
All psform Field controls share the same api. You can use :meth:`get_value` to set them and :meth:`set_value` to retrieve them.

::

    myform_dialog.int_field.set_value(40)
    assert myform_dialog.int_field.get_value() == 40

All controls also have changed and validate signals that are emitted whenever their values are modified by user interaction.

Validation
==========
We can modify the above class declaration to support validation by setting
:attribute:`validates` to True and overriding :meth:`validate`.

::

    class MyForm(Form):
        ...
        validates = True

        def validate(self):
            if len(self.strb_field.get_value()) < 3:
                return False, 'String B must be at least 3 characters.'

            return True

Here we ensure that strb_field is at least 3 characters in length. Any dialog created with :meth:`MyForm.as_dialog` can not be accepted unless the rules set
in the :meth:`validate` method are passed.
