import os

import cv2

import numpy as np

from PyQt6.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice, QUrl, QThread, QMutex, QMutexLocker, QSize, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QListWidget, QListWidgetItem, QComboBox, QHBoxLayout, QVBoxLayout, QFormLayout, QCheckBox, QSlider, QGroupBox, QSplitter, QFileDialog, QMessageBox
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QPixmap, QImage

from neophaser.board import ControllerBoard
from neophaser.controllers import controllers
from neophaser.options import OptionType
from neophaser.utils import DecimalSlider
from neophaser.visual import Visual, DataType

class VideoThread(QThread):
	frame_ready = pyqtSignal(np.ndarray)
	frame = 0

	def __init__(self, visual, parent=None):
		super().__init__(parent)
		self.visual = visual
		self.frames = visual.preview.shape[0]
		self._running = True
		self.mutex = QMutex()

	def run(self):
		while self._running:
			self.frame = (self.frame + 1) % self.frames
			self.frame_ready.emit(self.visual.preview[self.frame])
			QThread.msleep(30)
	
	def stop(self):
		with QMutexLocker(self.mutex):
			self._running = False

class PaginatorWidget(QWidget):
	# Define a custom signal that will emit the new page number
	changed = pyqtSignal(int)

	def __init__(self, parent=None):
		super().__init__(parent)

		# Initialize page counter to 1
		self.page_number = 1
		self.maximum = 0

		# Create layout
		self.layout = QHBoxLayout(self)

		# Create and add widgets
		self.left_button = QPushButton('<')
		self.page_label = QLabel(f"{self.page_number}/{self.maximum}")
		self.right_button = QPushButton('>')

		self.layout.addWidget(self.left_button)
		self.layout.addWidget(self.page_label)
		self.layout.addWidget(self.right_button)

		# Connect signals
		self.left_button.clicked.connect(self.decrement_page)
		self.right_button.clicked.connect(self.increment_page)
	
	def set_maximum(self, maximum):
		self.maximum = maximum
		self.page_label.setText(f"{self.page_number}/{self.maximum}")

	def increment_page(self):
		if self.page_number < self.maximum:
			self.page_number += 1
			self.page_label.setText(f"{self.page_number}/{self.maximum}")
			self.changed.emit(self.page_number)

	def decrement_page(self):
		if self.page_number > 1:
			self.page_number -= 1
			self.page_label.setText(f"{self.page_number}/{self.maximum}")
			self.changed.emit(self.page_number)

class MediaLoader(QWidget):
	loaded = pyqtSignal()
	changed_visual = pyqtSignal(Visual)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()

		# Media controls
		controls_layout = QHBoxLayout()
		layout.addLayout(controls_layout)

		open_file_button = QPushButton("Open")
		open_file_button.clicked.connect(self.open_file)
		controls_layout.addWidget(open_file_button)

		self.pagination_widget = PaginatorWidget()
		self.pagination_widget.changed.connect(self.set_active_visual)
		controls_layout.addWidget(self.pagination_widget)
		self.pagination_widget.hide()

		self.save_file_button = QPushButton("Save")
		controls_layout.addWidget(self.save_file_button)
		self.save_file_button.hide()

		self.media_display = QLabel(self)
		layout.addWidget(self.media_display)

		self.setLayout(layout)

		# Media player
		self.media_player = QMediaPlayer(self)
		self.media_player.mediaStatusChanged.connect(self.media_status_changed)

		self.video_thread = None

		# Enable drag and drop
		self.setAcceptDrops(True)

	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.acceptProposedAction()

	def dropEvent(self, event):
		for url in event.mimeData().urls():
			file_path = url.toLocalFile()
			self.load_media(file_path)
			break  # Only load the first file

	def open_file(self):
		file_paths, _ = QFileDialog.getOpenFileNames(self, "Open Media File", "", "Images (*.png *.jpg *.jpeg);;Videos (*.gif *.mp4 *.avi)")

		if file_paths:
			self.load_media(file_paths)

	def load_media(self, file_paths):
		for file_path in file_paths:
			if not Visual.check_valid_file(file_path):
				return QMessageBox.critical(
					self,
					"Invalid File",
					f"{file_path} is not a valid image or video format.",
					buttons=QMessageBox.StandardButton.Ok,
					defaultButton=QMessageBox.StandardButton.Ok,
				)
		
		if len(file_paths) == 1:
			file_path = file_paths[0]

			self.media_player.setSource(QUrl.fromLocalFile(file_path))

			self.visual = Visual(file_path)
			self.data = self.visual.preview
		else:
			self.visuals = [Visual(file_path) for file_path in file_paths]
			self.file_paths = file_paths
			self.active_visual = 0
			self.visual = self.visuals[0]
			self.data = self.visual.preview
			self.pagination_widget.set_maximum(len(self.visuals))
			self.pagination_widget.show()

		self.loaded.emit()

		self.save_file_button.show()

		self.set_data(self.visual)
	
	def set_active_visual(self, page_number):
		self.active_visual = page_number - 1
		self.visual = self.visuals[self.active_visual]
		self.set_data(self.visual)
		self.changed_visual.emit(self.visual)
	
	def set_data(self, visual):
		self.visual = visual
		self.data = self.visual.preview

		if visual.type == DataType.IMAGE:
			self.update_frame(self.data)
		elif self.visual.type == DataType.VIDEO:
			if self.video_thread:
				self.video_thread.stop()
				self.video_thread.wait()
			self.video_thread = VideoThread(self.visual)
			self.video_thread.frame_ready.connect(self.update_frame)
			self.video_thread.start()
	
	def update_frame(self, frame):
		pixmap = QPixmap.fromImage(QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888).rgbSwapped())
		self.media_display.setPixmap(pixmap)

	def media_status_changed(self, status):
		if status == QMediaPlayer.MediaStatus.EndOfMedia:
			self.video_widget.setHidden(True)
			self.media_display.setHidden(False)
			self.layout().removeWidget(self.video_widget)

class EffectOptionsWidget(QWidget):
	render = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.init_ui()

	def init_ui(self):
		self.setLayout(QVBoxLayout())

		self.options_stack = QGroupBox()
		self.options_stack.setMinimumWidth(400)
		self.options_layout = QFormLayout()
		self.options_stack.setLayout(self.options_layout)

		self.layout().addWidget(self.options_stack)
	
	def set_options(self, effect):
		self.layout().removeWidget(self.options_stack)

		self.options_stack = QGroupBox()
		self.options_stack.setMinimumWidth(450)
		self.options_layout = QFormLayout()
		self.options_stack.setLayout(self.options_layout)

		for option in effect.options.values():
			option.callback = lambda v, opt=option: (
				opt.set_value(v),
				self.render.emit(),
			)

			if option.type == OptionType.CHECKBOX:
				checkbox = QCheckBox()
				checkbox.setChecked(True if option.value == option.on else False)
				checkbox.stateChanged.connect(option.callback)
				self.options_layout.addRow(option.name, checkbox)
			elif option.type == OptionType.DROPDOWN:
				dropdown = QComboBox()
				for drop in option.options:
					dropdown.addItem(drop)
				dropdown.setCurrentText(option.value)
				dropdown.currentTextChanged.connect(option.callback)
				self.options_layout.addRow(option.name, dropdown)
			elif option.type == OptionType.RANGE_SLIDER:
				if option.interval < 1:
					slider = DecimalSlider()
					slider.setRange(option.min, option.max)
					slider.setValue(option.value)
					slider.decimalValueChanged.connect(option.callback)
				else:
					slider = QSlider(orientation=Qt.Orientation.Horizontal)
					slider.setRange(option.min, option.max)
					slider.setValue(int(option.value))
					slider.valueChanged.connect(option.callback)
				slider.setMinimumWidth(250)
				slider.setTickPosition(QSlider.TickPosition.TicksBelow)
				slider.setTickInterval(option.interval)
				self.options_layout.addRow(option.name, slider)

		self.options_stack.setLayout(self.options_layout)
		self.layout().addWidget(self.options_stack)
		
class DraggableListWidget(QListWidget):
	render = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setDragEnabled(True)
		self.viewport().setAcceptDrops(True)
		self.setDropIndicatorShown(True)
		self.setDragDropMode(QListWidget.DragDropMode.InternalMove)

	def mimeData(self, items):
		mime_data = QMimeData()
		encoded_data = QByteArray()
		stream = QDataStream(encoded_data, QIODevice.OpenModeFlag.WriteOnly)

		for item in items:
			stream.writeQString(item.text())

		mime_data.setData('application/x-qabstractitemmodeldatalist', encoded_data)
		return mime_data

	def dropMimeData(self, index, mime_data, action):
		if not mime_data.hasFormat('application/x-qabstractitemmodeldatalist'):
			return False

		encoded_data = mime_data.data('application/x-qabstractitemmodeldatalist')
		stream = QDataStream(encoded_data, QIODevice.OpenModeFlag.ReadOnly)

		while not stream.atEnd():
			text = stream.readQString()
			self.insertItem(index, QListWidgetItem(text))
			index += 1

		return True
	
	def mousePressEvent(self, event):
		item = self.itemAt(event.pos())
		if not item:
			self.clearSelection()
			self.setCurrentItem(None)
		super().mousePressEvent(event)

class BoardWidget(QWidget):
	render = pyqtSignal()

	def __init__(self, board, parent=None):
		super().__init__(parent)

		self.effects = list(controllers.keys())

		self.board = board

		self.init_ui()

	def init_ui(self):
		self.setLayout(QVBoxLayout())

		# Splitter for draggable list and options widget
		splitter = QSplitter(Qt.Orientation.Horizontal)
		self.layout().addWidget(splitter)

		# Draggable list widget
		self.list_widget = DraggableListWidget()
		splitter.addWidget(self.list_widget)
		self.list_widget.currentItemChanged.connect(self.show_effect_options)

		# Controls for adding and removing items
		controls_layout = QHBoxLayout()
		self.layout().addLayout(controls_layout)

		self.combo_box = QComboBox()
		controls_layout.addWidget(self.combo_box)

		add_button = QPushButton('+')
		add_button.clicked.connect(self.add_item)
		controls_layout.addWidget(add_button)

		remove_button = QPushButton('-')
		remove_button.clicked.connect(self.remove_item)
		controls_layout.addWidget(remove_button)

		# Dynamic options widget
		self.effect_options_widget = EffectOptionsWidget()
		splitter.addWidget(self.effect_options_widget)
		self.effect_options_widget.set_options(self.board)
		self.effect_options_widget.render.connect(self.render.emit)

		self.populate_dropdown()

	def populate_dropdown(self):
		self.combo_box.addItems(self.effects)

	def add_item(self):
		item_text = self.combo_box.currentText()
		self.list_widget.addItem(item_text)

		controller_item = controllers[item_text]()
		self.board.append(controller_item)

		self.render.emit()

	def remove_item(self):
		current_item = self.list_widget.currentItem()
		if current_item is not None:
			row = self.list_widget.row(current_item)
			self.list_widget.takeItem(row)
			self.board.remove(self.board[row])
		
		self.render.emit()

	def show_effect_options(self, current, previous):
		if current is not None:
			item_index = self.list_widget.row(current)
			effect_item = self.board[item_index]
			self.effect_options_widget.set_options(effect_item)
		else:
			self.effect_options_widget.set_options(self.board)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("neophaser")

		self.layout = QGridLayout()

		self.media_player = MediaLoader()
		self.media_player.loaded.connect(self.load_board)
		self.media_player.changed_visual.connect(self.change_visual)
		self.media_player.save_file_button.clicked.connect(self.render_and_save)
		self.layout.addWidget(self.media_player, 0, 0)

		widget = QWidget()
		widget.setLayout(self.layout)
		self.setCentralWidget(widget)
		self.show()
	
	def change_visual(self, visual):
		self.visual = self.media_player.visual
		self.data = self.visual.original_preview.copy()

		self.process_visual()
	
	def load_board(self):
		self.visual = self.media_player.visual
		self.data = self.visual.preview.copy()

		self.board = ControllerBoard(self.visual)
		board_manager = BoardWidget(self.board)

		board_manager.render.connect(self.process_visual)

		self.layout.addWidget(board_manager, 0, 1)
	
	def process_visual(self):
		self.visual.preview = self.board.process(self.data, sample_rate_multiplier=self.visual.sample_rate_multiplier)
		self.media_player.set_data(self.visual)
	
	def render_and_save(self):
		if hasattr(self.media_player, "visuals"):
			directory_path = QFileDialog.getExistingDirectory(parent=self, caption='Save Files', directory='')

			if directory_path:
				for visual, file_path in zip(self.media_player.visuals, self.media_player.file_paths):
					rendered = self.board.process(visual.original)

					filename = os.path.basename(file_path)
					save_path = os.path.join(directory_path, filename)

					if visual.type == DataType.IMAGE:
						cv2.imwrite(save_path, rendered)
					elif visual.type == DataType.VIDEO:
						fps = 30
						_, height, width, _ = rendered.shape
						out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
						for frame in rendered:
							out.write(frame)
						out.release()
		else:
			file_path, _ = QFileDialog.getSaveFileName(parent=self, caption='Save File', directory='', filter="Images (*.png *.jpg *.jpeg);;Animated (*.gif);;All files (*)")

			rendered = self.board.process(self.visual.original)

			if file_path:
				if self.visual.type == DataType.IMAGE:
					cv2.imwrite(file_path, rendered)
				elif self.visual.type == DataType.VIDEO:
					fps = 30
					_, height, width, _ = rendered.shape
					out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
					for frame in rendered:
						out.write(frame)
					out.release()