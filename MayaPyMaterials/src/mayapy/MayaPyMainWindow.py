# MayaPyMainWindow.py


from PySide import QtGui

from pyglass.windows.PyGlassWindow import PyGlassWindow

from mayapy.views.home.MayaPyHomeWidget import MayaPyHomeWidget

#___________________________________________________________________________________________________ MayaPyMainWindow
class MayaPyMainWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        PyGlassWindow.__init__(
            self,
            widgets={
                'home':MayaPyHomeWidget},
            title='Materials',
            **kwargs )

        self.setMinimumSize(960,540)
        self.setMaximumSize(960,540)
        self.setContentsMargins(0, 0, 0, 0)

        widget = self._createCentralWidget()
        layout = QtGui.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)

        self.setActiveWidget('home')
