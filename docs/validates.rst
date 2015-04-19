
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
