import numpy as np

from pedalboard import Pedalboard

from neophaser.options import OptionType, EffectOption
from neophaser.visual import DataType

class ControllerBoard(list):
	def __init__(self, visual):
		super().__init__()

		self.type = visual.type

		# we remove color channels so images only have 2 dims, and videos only have 3 dims
		self.dimensionality_options = EffectOption("Dimensionality", OptionType.DROPDOWN, options=["row", "column"] if self.type == DataType.IMAGE else ["row", "column", "temporal row", "temporal column", "pseudo-temporal row(?)", "pseudo-temporal column(?)"])
		self.sample_rate_options = EffectOption("Sample Rate", OptionType.RANGE_SLIDER, min=10000, max=40000, interval=5000)

		self.options = {
			"dimensionality": self.dimensionality_options,
			"sample_rate": self.sample_rate_options,
		}

		self.board = Pedalboard()

	def _preprocess(self, data):
		self.dimensionality_lookup = [(0, 1, 2), (1, 0, 2)] if self.type == DataType.IMAGE else [(0, 1, 2, 3), (0, 2, 1, 3), (1, 2, 0, 3), (2, 1, 0, 3), (1, 0, 2, 3), (2, 0, 1, 3)]
		self.dimensionality_transpose = self.dimensionality_lookup[self.dimensionality_options.options.index(self.dimensionality_options.value)]

		self.original_shape = data.shape
		transposed_data = np.transpose(data, self.dimensionality_transpose).copy()
		self.process_shape = transposed_data.shape
		return transposed_data.flatten()

	def _postprocess(self, audio):
		shaped_data = np.reshape(audio, self.process_shape)
		involuted_data = np.transpose(shaped_data, self.dimensionality_transpose).copy()

		# wanna see the worst hack of all time?

		# basically if our "transposition" (really a permutation of axes on a tensor) permutes more than 2 axes it's not an involution
		# it has to be called as many times as the axes were changed to get back to the original shape (god damned group theory)
		# in our case we're only in 4 dimensions, 3 because we don't care about the color channel
		# so we can just transpose twice to get back to the original shape because we'll never permute more than 2 axes
		if involuted_data.shape != self.original_shape:
			involuted_data = np.transpose(involuted_data, self.dimensionality_transpose).copy()
			
		return involuted_data.astype(np.uint8)
	
	def append(self, item):
		super().append(item)
		self.board.append(item.effect)
	
	def remove(self, item):
		super().remove(item)
		self.board.remove(item.effect)
	
	def insert(self, index, item):
		super().insert(index, item)
		self.board.insert(index, item.effect)
	
	def process(self, data, sample_rate_multiplier=1):
		d = self._preprocess(data)
		self._apply_options()
		out = self.board(d.astype(np.float32), self.sample_rate*sample_rate_multiplier).astype(np.uint8)
		return self._postprocess(out)

	def _apply_options(self):
		self.sample_rate = self.sample_rate_options.value
		for index, item in enumerate(self):
			if self.board[index] != item.effect: # update any effects that have been changed
				self.board[index] = item.effect # only really used for external plugin effects
			item._apply_options()