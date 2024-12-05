import unittest

from collections.abc import Callable
from hamlish_jinja import Hamlish, HamlishSettings, Output
from jinja2 import Environment, Template


class HamlishEnvironment(Environment):
	hamlish_settings: HamlishSettings
	hamlish_from_string: Callable[[str], Template]


class TestCase(unittest.TestCase):
	def setUp(self) -> None:
		self.hamlish = Hamlish(Output(
			indent_string = "  ",
			newline_string = "\n")
		)


	def _h(self, source: str) -> str:
		return self.hamlish.convert_source(source)
