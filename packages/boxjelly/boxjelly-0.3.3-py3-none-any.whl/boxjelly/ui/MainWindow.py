from PyQt6 import QtCore, QtMultimedia, QtWidgets, QtGui

from boxjelly.commands.TrackListCommand import BatchRenameTracksCommand, DeleteTrackByIDCommand, BatchDeleteTracksByIDCommand, BatchRenameTracksCommand, SplitTrackCommand, MergeTracksCommand
from boxjelly.lib.constants import APP_NAME
from boxjelly.models.TrackListModel import TrackListModel
from boxjelly.ui.OpenDialog import OpenDialog
from boxjelly.ui.settings.SettingsDialog import SettingsDialog
from boxjelly.ui.track.TrackPanel import TrackPanel
from boxjelly.ui.video.CthulhuVideoController import CthulhuVideoController

class MainWindow(QtWidgets.QMainWindow):
    """Application main window"""
    
    mediaLoaded = QtCore.pyqtSignal(QtCore.QUrl)
    tracksLoaded = QtCore.pyqtSignal(list)
    
    readRequested = QtCore.pyqtSignal()
    writeRequested = QtCore.pyqtSignal(list)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set window title
        self.setWindowTitle(APP_NAME)
        
        # Set window icon
        self.setWindowIcon(QtGui.QIcon(':/icons/logo'))
        
        # Create media
        self._media = None
        
        # Create track list model
        self._track_model = TrackListModel(self)
        
        # Create selection model
        self._selection_model = QtCore.QItemSelectionModel(self._track_model)
        
        # Create undo stack
        self._undo_stack = QtGui.QUndoStack(self)
        
        # Create the menu bar
        self._create_menu_bar()
        
        # Create the track panel and set it as the main widget
        self._track_panel = TrackPanel(self, self._track_model, self._selection_model)
        self.setCentralWidget(self._track_panel)
        
        # Create the Cthulhu video controller
        self._video_controller = CthulhuVideoController(self, self._track_model, self._selection_model)
        
        # Create the settings dialog
        self._settings_dialog = SettingsDialog(self)
        
        # Media content and track IO
        self._media_content = None
        self._track_io = None
        
        # Create the background worker thread
        self._worker_thread = QtCore.QThread()
        self._worker_thread.start()
        
        # Connect signals
        self.mediaLoaded.connect(self._video_controller.set_media)
        self._video_controller.mediaSetStatus.connect(self._on_media_set_status)
        self._track_panel.frameSelected.connect(self._video_controller.set_frame)
        self._video_controller.frameUpdated.connect(self._track_panel.show_frame)
        self._selection_model.selectionChanged.connect(self._on_selection_changed)
    
    @QtCore.pyqtSlot(bool)
    def _on_media_set_status(self, status):
        """Handle the media set status."""
        if not status:  # Failure to set media
            QtWidgets.QMessageBox.critical(self, 'Error', 'Failed to open media in Cthulhu.\nIs Cthulhu running?')
    
    @QtCore.pyqtSlot(QtCore.QItemSelection, QtCore.QItemSelection)
    def _on_selection_changed(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        # Select
        for model_index in selected.indexes():
            self._track_model.select_track(model_index.row())
        
        # Deselect
        for model_index in deselected.indexes():
            self._track_model.deselect_track(model_index.row())

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction('&Open', QtGui.QKeySequence('Ctrl+O'), self.open)
        file_menu.addAction('&Save', QtGui.QKeySequence('Ctrl+S'), self.save)
        file_menu.addAction('Save &As', QtGui.QKeySequence('Ctrl+Shift+S'), self.save_as)
        file_menu.addSeparator()
        file_menu.addAction('Se&ttings', QtGui.QKeySequence('Ctrl+,'), self.open_settings)
        file_menu.addSeparator()
        file_menu.addAction('&Quit', QtGui.QKeySequence('Ctrl+Q'), self.close)
        
        # Edit menu
        edit_menu = menu_bar.addMenu('&Edit')
        rename_action = edit_menu.addAction(QtGui.QIcon(':/icons/rename'), 'Re&name', QtGui.QKeySequence('Ctrl+R'), self.rename_selected_tracks)
        split_action = edit_menu.addAction(QtGui.QIcon(':/icons/split'), '&Split', QtGui.QKeySequence('Ctrl+N'), self.split_selected_track)
        merge_action = edit_menu.addAction(QtGui.QIcon(':/icons/merge'), '&Merge', QtGui.QKeySequence('Ctrl+M'), self.merge_selected_tracks)
        delete_action = edit_menu.addAction(QtGui.QIcon(':/icons/delete'), '&Delete', QtGui.QKeySequence('Del'), self.delete_selected_tracks)
        edit_menu.addSeparator()
        undo_action = edit_menu.addAction(QtGui.QIcon(':/icons/undo'), '&Undo', QtGui.QKeySequence('Ctrl+Z'), self._undo_stack.undo)
        redo_action = edit_menu.addAction(QtGui.QIcon(':/icons/redo'), '&Redo', QtGui.QKeySequence('Ctrl+Shift+Z'), self._undo_stack.redo)
        
        # Go menu
        go_menu = menu_bar.addMenu('&Go')
        seek_beginning_action = go_menu.addAction(QtGui.QIcon(':/icons/seek_beginning'), 'Seek &beginning', QtGui.QKeySequence('Ctrl+['), self.seek_beginning_selected_tracks)
        seek_end_action = go_menu.addAction(QtGui.QIcon(':/icons/seek_end'), 'Seek &end', QtGui.QKeySequence('Ctrl+]'), self.seek_end_selected_tracks)
        
        # Add actions to toolbar
        toolbar = QtWidgets.QToolBar('Edit', self)
        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar)
        toolbar.addActions([rename_action, split_action, merge_action, delete_action])
        toolbar.addSeparator()
        toolbar.addActions([seek_beginning_action, seek_end_action])
        toolbar.addSeparator()
        toolbar.addActions([undo_action, redo_action])
    
    def open_settings(self):
        """Open the settings dialog."""
        self._settings_dialog.show()
    
    def open(self):
        """Show the open dialog and load."""
        # Create and run the dialog
        open_dialog = OpenDialog(self)
        open_dialog.exec()
        
        # If not accepted, return
        if open_dialog.result() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        
        # Otherwise, get the media content and track IO
        self._media_content = open_dialog.media_content
        self._track_io = open_dialog.track_io
        
        # Load the media
        self.load_media(self._media_content)
        
        # Run the track IO read in the worker thread thread
        self._track_io.moveToThread(self._worker_thread)
        self._track_io.fileRead.connect(self._track_model.set_tracks)
        self._track_io.fileWritten.connect(self._on_save_finished)
        self._track_io.fileReadFailure.connect(self._on_read_failure)
        self._track_io.fileWriteFailure.connect(self._on_write_failure)
        self.readRequested.connect(self._track_io.read)
        self.writeRequested.connect(self._track_io.write)
        self.do_read()
    
    def do_read(self):
        """Read the tracks from the track IO."""
        self.readRequested.emit()
        
        # Show a progress dialog while reading
        progress = QtWidgets.QProgressDialog('Reading tracks...', None, 0, 0, self)
        progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.show()
        
        # Wait for the read to finish or fail, then close
        self._track_io.fileRead.connect(progress.close)
        self._track_io.fileReadFailure.connect(progress.close)
    
    @QtCore.pyqtSlot(str)
    def _on_read_failure(self, error_message: str):
        """Show a message box when reading fails."""
        QtWidgets.QMessageBox.critical(self, 'Error', 'Failed to read tracks: \n\n{}'.format(error_message))
    
    def do_write(self):
        """Write the tracks to the track IO."""
        self.writeRequested.emit(self._track_model.get_all_tracks())
    
    @QtCore.pyqtSlot(str)
    def _on_write_failure(self, error_message: str):
        """Show a message box when writing fails."""
        QtWidgets.QMessageBox.critical(self, 'Error', 'Failed to write tracks: \n\n{}'.format(error_message))
    
    @QtCore.pyqtSlot()
    def _on_save_finished(self):
        QtWidgets.QMessageBox.information(self, 'Saved', 'Saved successfully.')
    
    def save(self):
        # If no track IO, show an error
        if not self._track_io:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No file open.')
            return
        
        # Get confirmation
        confirm = QtWidgets.QMessageBox.question(self, 'Confirm', 'Are you sure you want to save?')
        
        # If confirmed, send the signal to save
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            self.do_write()
    
    def save_as(self):
        # If no track IO, show an error
        if not self._track_io:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No file open.')
            return
        
        # Get the new file path, requiring the same suffix as the current
        current_dir = self._track_io.path.parent
        current_suffix = self._track_io.path.suffix
        new_path_str, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save As', str(current_dir), f'{current_suffix[1:].upper()} (*{current_suffix})')
        
        if not ok:
            return
        
        # Update the track IO target path
        self._track_io.path = new_path_str
        
        # Send the signal to save
        self.do_write()
        
    
    @QtCore.pyqtSlot(QtCore.QUrl)
    def load_media(self, media):
        """Load the media and emit the mediaLoaded signal."""
        self._media = media
        self.mediaLoaded.emit(media)
    
    @QtCore.pyqtSlot(list)
    def load_tracks(self, tracks):
        """Load the tracks and emit the tracksLoaded signal."""
        self._track_model.set_tracks(tracks)
        self.tracksLoaded.emit(tracks)
    
    @QtCore.pyqtSlot(int)
    def delete_track(self, track_id):
        """Delete a track from the model by its ID."""
        command = DeleteTrackByIDCommand(self._track_model, track_id)
        self._undo_stack.push(command)
    
    def delete_selected_tracks(self):
        """Delete the selected tracks."""
        selected_indices = self._selection_model.selectedIndexes()
        selected_ids = [index.data(TrackListModel.IDRole) for index in selected_indices]
        
        command = BatchDeleteTracksByIDCommand(self._track_model, selected_ids)
        self._undo_stack.push(command)
    
    def rename_selected_tracks(self):
        """Change the label of a track by its ID."""
        new_label, ok = QtWidgets.QInputDialog.getText(self, 'Rename track', 'Label:')
        if not ok:
            return
        
        selected_indices = self._selection_model.selectedIndexes()
        selected_ids = [index.data(TrackListModel.IDRole) for index in selected_indices]
        
        command = BatchRenameTracksCommand(self._track_model, selected_ids, new_label)
        self._undo_stack.push(command)
        
    def split_selected_track(self):
        """Split a track at the current frame."""
        selected_indices = self._selection_model.selectedIndexes()
        if len(selected_indices) != 1:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select a single track to split.')
            return
        
        selected_id = selected_indices[0].data(TrackListModel.IDRole)
        selected_start_frame = selected_indices[0].data(TrackListModel.StartFrameRole)
        
        split_idx = self._video_controller.get_frame_number() - selected_start_frame
        
        if not 1 <= split_idx <= len(selected_indices[0].data(TrackListModel.EventsRole)):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid split position for selected track.')
            return
        
        command = SplitTrackCommand(self._track_model, selected_id, split_idx)
        self._undo_stack.push(command)
        
        # Add the new track to the selection
        new_row_idx = self._track_model.index_by_id(command.new_track_id)
        self._selection_model.select(self._track_model.index(new_row_idx), QtCore.QItemSelectionModel.SelectionFlag.Select)
    
    def merge_selected_tracks(self):
        """Merge the selected tracks."""
        selected_indices = self._selection_model.selectedIndexes()
        if len(selected_indices) < 2:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select at least two tracks to merge.')
            return
        
        selected_ids = [index.data(TrackListModel.IDRole) for index in selected_indices]
        
        command = MergeTracksCommand(self._track_model, selected_ids)
        self._undo_stack.push(command)
        
        # Add the new track to the selection
        new_row_idx = self._track_model.index_by_id(command.new_track_id)
        self._selection_model.select(self._track_model.index(new_row_idx), QtCore.QItemSelectionModel.SelectionFlag.Select)
    
    def seek_beginning_selected_tracks(self):
        """Seek to the first frame of the selected tracks."""
        selected_indices = self._selection_model.selectedIndexes()
        if len(selected_indices) < 1:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select at least one track to seek to.')
            return
        
        selected_start_frames = [index.data(TrackListModel.StartFrameRole) for index in selected_indices]
        
        self._video_controller.set_frame(min(selected_start_frames))
    
    def seek_end_selected_tracks(self):
        """Seek to the last frame of the selected tracks."""
        selected_indices = self._selection_model.selectedIndexes()
        if len(selected_indices) < 1:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select at least one track to seek to.')
            return
        
        selected_end_frames = [index.data(TrackListModel.EndFrameRole) for index in selected_indices]
        
        self._video_controller.set_frame(max(selected_end_frames))
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._video_controller.try_close()
        self._worker_thread.quit()
        return super().closeEvent(a0)
