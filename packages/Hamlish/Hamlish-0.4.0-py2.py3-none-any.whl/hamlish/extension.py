import re

from collections.abc import Callable, MutableMapping
from dataclasses import dataclass, field, fields
from jinja2 import Environment, TemplateSyntaxError, nodes as Nodes
from jinja2.environment import Template
from jinja2.ext import Extension
from jinja2.nodes import Node
from jinja2.parser import Parser
from os.path import splitext
from typing import Any, Type, TypedDict

from .exception import TemplateIndentationError
from .parser import Hamlish, Output, OutputMode


START_TAG = re.compile(r"\{%\-?\s*haml.*?%\}")
END_TAG = re.compile(r"\{%\-?\s*endhaml\s*\-?%\}")
PROP_NAMES: tuple[str, ...] = (
	"file_extensions",
	"indent_string",
	"newline_string",
	"debug",
	"enable_div_shortcut",
	"mode"
)


class EnvConfig(TypedDict):
	block_start_string: str
	block_end_string: str
	variable_start_string: str
	variable_end_string: str


@dataclass(slots = True)
class HamlishSettings:
	"Stores the settings for a Hamlish extension. Properties can be accessed like a dict"


	file_extensions: tuple[str, ...] = (".haml", ".jhaml", ".jaml")
	"File extensions the extension should handle"

	indent_string: str = "    "
	"String used for indenting when the output mode is not set to :any:`OutputMode.COMPACT`"

	newline_string: str = "\n"
	"String to use on new lines when the output mode is not set to :any:`OutputMode.COMPACT`"

	debug: bool = False
	"¯\\\\_(ツ)_/¯"

	enable_div_shortcut: bool = True
	"""
		Enables the div shortcut so you can create div tags with a id (#myid) or class (.myclass) at
		the beginning of a line.
	"""

	mode: OutputMode = OutputMode.COMPACT
	"How to format the resulting code"

	filters: dict[str, Callable[[str], str]] = field(default_factory = dict)
	"Functions that can be called on text to modify it"


	def __getitem__(self, name: str) -> Any:
		return getattr(self, name)


	def __setitem__(self, name: str, value: Any) -> None:
		setattr(self, name, value)


	def __delitem__(self, name: str) -> None:
		for item in fields(self):
			if item.name == name:
				self[name] = item.default
				return

		raise KeyError(name)


	def set_mode(self, mode: OutputMode | str) -> None:
		"""
			Set the :attr:`HamlishSettings.mode` setting. :class:`str` values will be parsed.

			:param mode: New output mode to set
		"""

		self.mode = OutputMode.parse(mode)


class HamlishExtension(Extension):
	"An extension for Jinja2 that adds support for HAML-like templates."


	def __init__(self, environment: Environment):
		Extension.__init__(self, environment)

		self.settings: HamlishSettings = HamlishSettings()
		"Settings for the extension"

		environment.extend(
			hamlish_from_string = self.from_string,
			hamlish_settings = self.settings
		)


	def get_property(self, name: str) -> Any:
		if name not in PROP_NAMES:
			raise AttributeError(f"Invalid extension config: {name}")

		return getattr(self, name)


	def set_property(self, name: str, value: Any) -> None:
		if name not in PROP_NAMES:
			raise AttributeError(f"Invalid extension config: {name}")

		setattr(self, name, value)


	def preprocess(self, source: str, name: str | None, filename: str | None = None) -> str:
		"""
			Transpile a Hamlish template into a Jinja template

			:param source: Full text source of the template
			:param name: Name of the template
			:param filename: Path to the template
			:raises TemplateSyntaxError: When the template cannot be parsed
		"""

		if name is None:
			return source

		if splitext(name)[1] not in self.settings.file_extensions:
			return source

		h = self.get_preprocessor(self.settings.mode)

		try:
			return h.convert_source(source)

		except (TemplateSyntaxError, TemplateIndentationError) as e:
			raise TemplateSyntaxError(e.message or "", e.lineno, name, filename) from None


	def get_preprocessor(self, mode: OutputMode) -> Hamlish:
		"""
			Gets the preprocessor

			:param mode: Output format to use
			:raises ValueError: When an invalid mode is specified
		"""

		mode = OutputMode.parse(mode)
		env_settings: EnvConfig = {
			"block_start_string": self.environment.block_start_string,
			"block_end_string": self.environment.block_end_string,
			"variable_start_string": self.environment.variable_start_string,
			"variable_end_string": self.environment.variable_end_string}

		if mode == OutputMode.COMPACT:
			output = Output(
				indent_string = "",
				newline_string = "",
				**env_settings
			)

		elif mode == OutputMode.DEBUG:
			output = Output(
				indent_string = "    ",
				newline_string = "\n",
				debug = True,
				**env_settings
			)

		else:
			output = Output(
				indent_string = self.settings.indent_string,
				newline_string = self.settings.newline_string,
				debug = self.settings.debug,
				**env_settings
			)

		return Hamlish(
			output,
			self.settings.enable_div_shortcut,
			self.settings.filters
		)


	def set_mode(self, value: OutputMode | str) -> None:
		"""
			Set the output mode to use when preprocessing templates

			:param value: Output format to use
			:raises ValueError: When a string is provided and connot be parsed into a
				:class:`OutputMode` value
		"""

		self.mode = OutputMode.parse(value)


	def from_string(self,
					source: str,
					name: str | None = None,
					global_vars: MutableMapping[str, Any] | None = None,
					template_class: Type[Template] = Template) -> Template:

		global_vars = self.environment.make_globals(global_vars)
		cls = template_class or self.environment.template_class
		template_name = name or "hamlish_from_string"

		if len(self.settings.file_extensions):
			template_name += self.settings.file_extensions[0]

		else:
			template_name += ".haml"

		return cls.from_code(
			self.environment,
			self.environment.compile(source, template_name),
			global_vars,
			None
		)


class HamlishTagExtension(HamlishExtension):
	"""
		An extension for Jinja2 that adds a ``{% haml %}`` tag to use the syntax supported by
		:class:HamlishExtension: in an HTML template.
	"""

	tags = set(["haml"])


	def _get_lineno(self, source: str) -> int:
		matches = re.finditer(r"\n", source)

		if matches:
			return len(tuple(matches))

		return 0


	def parse(self, parser: Parser) -> list[Node] | Node:
		"""
			Parse all ``haml`` blocks in a Jinja template
		"""
		haml_data = parser.parse_statements(("name:endhaml",))
		parser.stream.expect("name:endhaml")

		return [
			Nodes.Output([haml_data])
		]


	def preprocess(self, source: str, name: str | None, filename: str | None = None) -> str:
		"""
			Transpile a Hamlish block

			:param source: Full text source of the template
			:param name: Name of the template
			:param filename: Path to the template
			:raises TemplateSyntaxError: When the template cannot be parsed
		"""

		ret_source = ""
		start_pos = 0

		while True:
			tag_match = START_TAG.search(source, start_pos)

			if tag_match:
				end_tag = END_TAG.search(source, tag_match.end())

				if not end_tag:
					raise TemplateSyntaxError(
						"Expecting 'endhaml' tag",
						self._get_lineno(source[:start_pos])
					)

				haml_source = source[tag_match.end():end_tag.start()]
				h = self.get_preprocessor(self.settings.mode)

				try:
					ret_source += source[start_pos:tag_match.start()]
					ret_source += h.convert_source(haml_source)

				except (TemplateSyntaxError, TemplateIndentationError) as e:
					raise TemplateSyntaxError(e.message or "", e.lineno, name, filename) from None

				start_pos = end_tag.end()

			else:
				ret_source += source[start_pos:]
				break

		return ret_source
