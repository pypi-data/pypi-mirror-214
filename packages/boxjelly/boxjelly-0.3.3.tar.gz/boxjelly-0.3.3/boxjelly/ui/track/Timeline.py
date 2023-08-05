import math

from PyQt6 import QtWidgets, QtCore, QtGui

from boxjelly.lib.settings import SettingsManager


class Timeline(QtWidgets.QWidget):
    
    frameChanged = QtCore.pyqtSignal(int)
    frameStepChanged = QtCore.pyqtSignal(int)
    frameScaleChanged = QtCore.pyqtSignal(float)
    frameSelected = QtCore.pyqtSignal(int)
    
    def __init__(self, parent, frame_step: int, frame_scale: float = 1.0):
        super().__init__(parent)
        
        self._background_brush = self.palette().window()
        self._foreground_brush = self.palette().windowText()
        
        self._frame = 0
        self._frame_step = frame_step
        self._frame_scale = frame_scale
        
        self._settings = SettingsManager.get_instance()
        
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

    def set_frame(self, frame: int):
        """
        Set the current frame to be displayed.
        """
        if frame != self._frame:
            self.frameChanged.emit(frame)
        self._frame = frame
        self.update()
    
    def set_frame_step(self, frame_step: int):
        """
        Set the frame step.
        """
        if frame_step != self._frame_step:
            self.frameStepChanged.emit(frame_step)
        self._frame_step = frame_step
        self.update()
    
    def set_frame_scale(self, frame_scale: float):
        """
        Set the frame scale.
        """
        if frame_scale != self._frame_scale:
            self.frameScaleChanged.emit(frame_scale)
        self._frame_scale = frame_scale
        self.update()
    
    def map_frame_to_x(self, frame: int) -> int:
        """
        Map a frame to an x coordinate.
        """
        return int((frame - self._frame) * self._frame_scale)
    
    def map_x_to_frame(self, x: int) -> int:
        """
        Map an x coordinate to a frame.
        """
        return int(x / self._frame_scale + self._frame)
    
    def map_frame_to_elapsed_time_ms(self, frame: int) -> int:
        """
        Map a frame to an elapsed time in milliseconds.
        """
        frame_rate = self._settings.frame_rate.value
        return round(frame * 1000 / frame_rate)

    @property
    def frame(self):
        return self._frame
    
    @property
    def frame_step(self):
        return self._frame_step
    
    @property
    def frame_scale(self):
        return self._frame_scale
    
    @property
    def max_frame(self) -> int:
        return int(self._frame + self.width() / self._frame_scale)

    def paintEvent(self, event: QtGui.QPaintEvent):
        # Get the painter
        painter = QtGui.QPainter(self)
        
        # Get the device size
        width = painter.device().width()
        height = painter.device().height()
        
        # Set pen to foreground
        painter.setPen(self._foreground_brush.color())
        
        # Draw horizontal line at bottom
        painter.drawLine(0, height - 1, width, height - 1)
        
        # Compute the multiples of the frame step in the range [frame, max_frame]
        tick_frames = range(math.floor(self._frame / self._frame_step) * self._frame_step, self.max_frame + 1, self._frame_step)
        
        # Compute inter-tick distance and label modulus
        inter_tick_distance = self._frame_scale * self._frame_step
        label_modulus = max(1, 2**math.floor(math.log2(100 / inter_tick_distance)))
        
        # Draw vertical lines and labels at the tick frames
        for tick_frame in tick_frames:
            x = self.map_frame_to_x(tick_frame)
            painter.drawLine(x, height - 1, x, height - height // 4)
            if tick_frame // self._frame_step % label_modulus == 0:
                tick_elaped_time_ms = self.map_frame_to_elapsed_time_ms(tick_frame)
                timedelta_str = QtCore.QTime(0, 0, 0).addMSecs(tick_elaped_time_ms).toString('mm:ss')
                painter.drawText(x + 5, height - 5, timedelta_str)
    
    def sizeHint(self):
        return QtCore.QSize(100, 20)
    
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.frameSelected.emit(self.map_x_to_frame(event.pos().x()))
