#!/usr/bin/env python
import sys
import signal
import pprint
from PySide import QtGui
from pslive import LiveLinker
from psforms import *
from psforms.validators import required, email, checked
from psforms.fields import *


class ValidationTestForm(Form):

    meta = FormMetaData(
        title='Validation Test Form',
        description='Test validation styling',
        header=False,
    )

    required_str = StringField('Valid String', validators=(required,))
    valid_email = StringField('Valid Email', validators=(required, email))


class ImageTestForm(Form):

    meta = FormMetaData(
        title='Validation Test Form',
        description='Test validation styling',
        header=False,
    )

    imagefield = ImageField('ImageField')
    listfield = ListField(
        'ListField',
        options=['option' + str(i) for i in xrange(10)],
    )


class ControlsTestForm(Form):

    meta = FormMetaData(
        title='Controls Test Form',
        columns=2,
    )

    stringfield = StringField('StringField', default='String Field Default')
    intfield = IntField('IntField')
    floatfield = FloatField('FloatField')
    int2field = Int2Field('Int2Field')
    float2field = Float2Field('Float2Field')
    intoptionfield = IntOptionField(
        'IntOptionField',
        options=['option' + str(i) for i in xrange(10)],
    )
    stringoptionfield = StringOptionField(
        'StringOptionField',
        options=['option' + str(i) for i in xrange(10)],
    )
    filefield = FileField('FileField')
    folderfield = FolderField('FolderField')
    savefilefield = SaveFileField('SaveFileField')
    boolfielda = BoolField('BoolFieldA', validators=(checked,))
    boolfieldb = BoolField('BoolFieldB')
    buttonoptionfield = ButtonOptionField(
        'ButtionOptionField',
        options='abc',
    )
    intbuttonoptionfield = IntButtonOptionField(
        'IntButtionOptionField',
        options='xyz',
    )


class VisualTestForm(Form):

    meta = FormMetaData(
        title='Visual Test Form',
        description='Stylsheet + widget tests',
        header=True,
    )

    image_form = ImageTestForm()
    controls_form = ControlsTestForm()
    validation_form = ValidationTestForm()


def form_accepted(form):
    def accepted():
        print 'Form Accepted...\n'
        pprint.pprint(form.get_value(flatten=True))
    return accepted


def form_rejected(form):
    def rejected():
        print 'Form Rejected...'
    return rejected


def run_visual_test():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    dialog = VisualTestForm.as_dialog(frameless=True, dim=True)
    dialog.accepted.connect(form_accepted(dialog))
    dialog.rejected.connect(form_rejected(dialog))
    LiveLinker(path=os.path.abspath('ui_resources/style.css'), parent=app)

    sys.exit(dialog.exec_())


if __name__ == '__main__':

    args = sys.argv
    if len(args) > 1 and args[1] == '--visual':
        run_visual_test()
