'''
pslive
======
Live CSS Reloading for PySide.
This is pretty useful. You might want to use it too!
'''

from PySide import QtCore
from collections import defaultdict


class LiveLinker(QtCore.QFileSystemWatcher):
    '''Updates a widgets style when its css changes.

    Simple usage case::

        w = QtGui.QWidget()
        LiveLinker(path='path/to/style.css', parent=w)

    Multiple widgets and stylesheets::

        w = QtGui.QMainWindow()
        d = QtGui.QDialog(parent=w)

        live = LiveLinker(parent=w)
        live.link(w, 'path/to/windowstyle.css')
        live.link(d, 'path/to/dialogstyle.css')

    '''

    def __init__(self, path=None, parent=None):
        super(LiveLinker, self).__init__(parent)
        self.fileChanged.connect(self.css_changed)
        self.path_mapping = defaultdict(set)

        if path and parent:
            self.link(parent, path)

    def __repr__(self):
        return '<{}>(parent={})'.format(self.__class__.__name__, self.parent())

    def link(self, widget, path):
        '''Links a widget to a stylesheet path. Updating the widgets stylesheet
        when changes occur to the path.

        :param widget: QtGui.QWidget instance
        :param path: Filepath to stylesheet
        '''

        self.path_mapping[path].add(widget)
        self.addPath(path)

    def unlink(self, widget, path):
        '''Unlinks a widget from a stylesheet path.

        :param widget: QtGui.QWidget instance
        :param path: Filepath to stylesheet
        '''

        if not self.path_mapping[path]:
            return

        self.path_mapping[path].discard(widget)
        if not self.path_mapping[path]:
            self.path_mapping.pop(path)
            self.removePath(path)

    def css_changed(self, path):
        '''Updates all widget linked to the changed filepath.'''

        widgets = self.path_mapping[path]
        with open(path) as f:
            for widget in widgets:
                widget.setStyleSheet(f.read())
                widget.style().unpolish(widget)
                widget.style().polish(widget)
