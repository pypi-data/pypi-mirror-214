import enum
import mimetypes

import cv2
import numpy as np

# image and video file types enum
class DataType(enum.Enum):
	IMAGE = enum.auto()
	VIDEO = enum.auto()

class Visual:
	def __init__(self, path, max_width=500, max_height=500):
		self.path = path
		
		self.preview_dimensions = (max_width, max_height)

		self.type = self.check_valid_file(path)

		if self.type == DataType.VIDEO:
			self.original = self._read_video()
			self.preview = self._resize_video(self.original.copy())
		elif self.type == DataType.IMAGE:
			self.original = self._read_image()
			self.preview = self._resize_image(self.original.copy())
		else:
			raise ValueError("The file is neither an image nor a video.")
		
		self.original_preview = self.preview.copy()

		self.sample_rate_multiplier = self.preview.size / self.original.size

		self.effects = []
	
	@staticmethod
	def check_valid_file(path):
		mime_type, _ = mimetypes.guess_type(path)

		if mime_type is None:
			return False

		if mime_type.startswith("video") or mime_type == "image/gif":
			return DataType.VIDEO
		elif mime_type.startswith("image"):
			return DataType.IMAGE
		else:
			return False

	def _read_image(self):
		return cv2.imread(self.path)

	def _resize_image(self, image):		
		# Get the dimensions of the image
		height, width, _ = image.shape

		aspect_ratio = width / height

		if width > height:
			width = min(self.preview_dimensions[0], width)
			height = int(width / aspect_ratio)
		else: 
			height = min(self.preview_dimensions[1], height)
			width = int(height * aspect_ratio)

		# Resize the image
		return cv2.resize(image, (width, height))

	def _read_video(self):
		cap = cv2.VideoCapture(self.path)

		num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

		height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

		video_array = np.empty((num_frames, height, width, 3), dtype=np.uint8)

		# Read the video frames and store them in the numpy array
		frame_index = 0
		while cap.isOpened():
			ret, frame = cap.read()
			if not ret:
				break

			# Store the frame in the numpy array
			video_array[frame_index] = frame
			frame_index += 1

		# Release the video capture object
		cap.release()

		return video_array

	def _resize_video(self, video):
		# Get the dimensions of the video
		num_frames, height, width, _ = video.shape

		aspect_ratio = width / height

		if width > height:
			width = min(self.preview_dimensions[0], width)
			height = int(width / aspect_ratio)
		else: 
			height = min(self.preview_dimensions[1], height)
			width = int(height * aspect_ratio)

		# Resize the video
		return np.array([cv2.resize(frame, (width, height)) for frame in video])