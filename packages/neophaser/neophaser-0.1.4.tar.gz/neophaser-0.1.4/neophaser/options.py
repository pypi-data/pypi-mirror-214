import enum

from pedalboard import LadderFilter

class OptionType(enum.Enum):
	CHECKBOX = enum.auto()
	DROPDOWN = enum.auto()
	RANGE_SLIDER = enum.auto()

class EffectOption:
	def __init__(self, name, t, **kwargs):
		self.name = name
		self.type = t

		self.value = None

		if self.type == OptionType.CHECKBOX:
			self.on = kwargs["on"]
			self.off = kwargs["off"]
			self.value = self.off
		elif self.type == OptionType.DROPDOWN:
			self.options = kwargs["options"]
			self.value = self.options[0]
		elif self.type == OptionType.RANGE_SLIDER:
			self.min = kwargs["min"]
			self.max = kwargs["max"]
			self.interval = kwargs["interval"]
			self.value = self.min + ((self.max - self.min) / 2)
	
	def set_value(self, value):
		if self.type == OptionType.CHECKBOX:
			self.value = self.on if value else self.off
		else:
			self.value = value

class EffectController():
	def _apply_options(self):
		for (name, option) in self.options.items():
			setattr(self.effect, name, option.value)