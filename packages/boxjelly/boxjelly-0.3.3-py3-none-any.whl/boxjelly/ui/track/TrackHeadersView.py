from PyQt6 import QtWidgets, QtCore, QtGui

from boxjelly.delegates.TrackHeadersDelegate import TrackHeadersDelegate


class TrackHeadersView(QtWidgets.QListView):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setItemDelegate(TrackHeadersDelegate(self))
        self.viewport().setMouseTracking(True)
        
        self.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
        
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
    def set_vertical_scroll(self, value: int):
        self.verticalScrollBar().setValue(value)
    
    def wheelEvent(self, e: QtGui.QWheelEvent):
        pass