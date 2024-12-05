from __future__ import annotations

import enum
import re

from jinja2 import TemplateSyntaxError
from typing import Callable, Type

from .exception import TemplateIndentationError
from .docnode import (
	Node,
	EmptyLine,
	HTMLTag,
	JinjaTag,
	ExtendedJinjaTag,
	TextNode,
	FilterNode,
	InlineData,
	NestedTags,
	PreformatedText,
	SelfClosingTag,
	SelfClosingJinjaTag,
	SelfClosingHTMLTag,
	JinjaVariable,
	ExtendingJinjaTag
)

try:
	from typing import Self

except ImportError:
	from typing_extensions import Self


DOCTYPES = {
	"html5": (None, None),
	"strict": ("HTML 4.01", "http://www.w3.org/TR/html4/strict.dtd"),
	"trans": ("HTML 4.01 Transitional", "http://www.w3.org/TR/html4/loose.dtd"),
	"frameset": ("HTML 4.01 Frameset", "http://www.w3.org/TR/html4/frameset.dtd"),
	"xhtml": ("XHTML 1.1", "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"),
	"xstrict": ("XHTML 1.0 Strict", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"),
	"xtrans": ("XHTML 1.0 Transitional", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"),
	"xframeset": ("XHTML 1.0 Frameset", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd")
}


class OutputMode(enum.Enum):
	"Output format to use"

	COMPACT = "compact"
	"Remove all extra whitespace and newlines"

	INDENTED = "indented"
	"Intent the result similarly to the source"

	DEBUG = "debug"
	"Indent the result in a more HAML style"


	@classmethod
	def parse(cls: Type[Self], value: Self | str) -> Self:
		"""
			Parse a string into an enum value

			:param value: String to be parsed
			:raises ValueError: When an enum value cannot be found
		"""

		if isinstance(value, cls):
			return value

		for item in cls:
			if value in (item.name, item.value):
				return item

		raise ValueError(f"Invalid output mode: '{value}'")


class Hamlish:
	"""
		Main parser class.
	"""

	INLINE_DATA_SEP: str = " << "
	SELF_CLOSING_TAG: str = "."
	JINJA_TAG: str = "-"
	JINJA_VARIABLE: str = "="
	HTML_TAG: str = "%"
	ESCAPE_LINE: str = "\\"
	PREFORMATED_LINE: str = "|"
	CONTINUED_LINE: str = "\\"
	ID_SHORTCUT: str = "#"
	CLASS_SHORTCUT: str = "."
	LINE_COMMENT: str = ";"
	NESTED_TAGS_SEP: str = " -> "
	FILTER_START: str = ":"
	DOCTYPE_TAG: str = "!!!"


	# Which haml tags that can contain inline data
	_inline_data_tags: set[str] = set([HTML_TAG, JINJA_TAG])

	# Which html tags that can start a line with nested tags
	_nested_tags: set[str] = set([HTML_TAG, JINJA_TAG])

	_div_shorcut_re: re.Pattern[str] = re.compile(r'^(\s*)([#\.])', re.M)

	_self_closing_jinja_tags: set[str] = set([
		'include',
		'extends',
		'import',
		'set',
		'from',
		'do',
		'break',
		'continue'
	])

	_self_closing_html_tags: set[str] = set([
		'br',
		'img',
		'link',
		'hr',
		'meta',
		'input'
	])

	_extended_tags: dict[str, set[str]] = {
		'else': set(['if', 'for']),
		'elif': set(['if']),
		'pluralize': set(['trans'])
	}


	def __init__(self,
				output: Output,
				use_div_shortcut: bool = True,
				filters: dict[str, Callable[[str], str]] | None = None):

		"""
			Create a new HAML parser.

			.. note::
				This is meant to be use internally. Use :meth:`Hamlish.new` instead.

			:param output: ``Output`` object to write the nodes to
			:param use_div_shortcut: Allow using ``.`` and ``#`` to create DIV elements
			:param filters: Functions that can be called in a template to alter the text
		"""

		self.output: Output = output
		"Object all of the nodes will be written to"

		self.enable_div_shortcut: bool = use_div_shortcut
		"Allow using ``.`` and ``#`` to create DIV elements"

		self.filters: dict[str, Callable[[str], str]] = filters or {}
		"Functions that can be called in a template to alter the text"


	@classmethod
	def new(cls: type[Self],
			mode: OutputMode | str = OutputMode.COMPACT,
			indent_string: str = "    ",
			enable_div_shortcut: bool = True,
			filters: dict[str, Callable[[str], str]] | None = None) -> Self:
		"""
			Create a new HAML parser

			:param mode: Output format to use
			:param indent_string: String to use for each indent level if ``mode`` is not
				:attr:`OutputMode.COMPACT`
			:param enable_div_shortcut: Allow using ``.`` and ``#`` to create DIV elements
			:param filters: Filter functions to use in the template
		"""

		mode = OutputMode.parse(mode)
		options: dict[str, str | bool] = {
			"debug": mode == OutputMode.DEBUG
		}

		if mode == OutputMode.COMPACT:
			options["indent_string"] = ""
			options["newline_string"] = ""

		elif mode == OutputMode.DEBUG:
			options["indent_string"] = indent_string
			options["newline_string"] = "\n"

		return cls(Output(**options), enable_div_shortcut, filters) # type: ignore


	def convert_source(self, source: str) -> str:
		"""
			Transpile a Hamlish template into a Jinja template

			:param source: Raw source of the Hamlish template
		"""

		tree = self.get_haml_tree(source)
		return self.output.create(tree)


	def get_haml_tree(self, source: str) -> list[Node]:
		"""
			Parse a Hamlish template and return it as a list of :class:`Node` objects

			:param source: Raw source of the Hamlish template
		"""

		blocks = self._get_haml_tree(source)
		return self._create_extended_jinja_tags(blocks)



	def _get_haml_tree(self, source: str) -> list[Node]:
		source_lines = self._get_source_lines(source)
		root = Node()

		# contains always atleast one element
		block_stack = [root]

		# stack for current indent level
		indent_stack = [-1]

		for lineno, line in enumerate(source_lines, 1):
			if not line.strip():
				block_stack[-1].add(EmptyLine())
				continue

			indent: int = 0
			m = re.match(r"^(\s+)", line)

			if m:
				indent_str = m.group(1)

				if ' ' in indent_str and '\t' in indent_str:
					raise TemplateIndentationError("Mixed tabs and spaces", lineno)

				indent = len(indent_str)

			if indent > indent_stack[-1]:
				indent_stack.append(indent)

			else:
				while indent < indent_stack[-1]:
					indent_stack.pop()
					block_stack.pop()

				block_stack.pop()

			if indent != indent_stack[-1]:
				raise TemplateIndentationError(
					"Unindent does not match any outer indentation level", lineno
				)

			node = self._parse_line(lineno, line.strip())

			if not block_stack[-1].can_have_children():
				if isinstance(node, InlineData):
					raise TemplateSyntaxError("Inline Data Node can't contain child nodes", lineno)

				raise TemplateSyntaxError("Self closing tag can't contain child nodes", lineno)

			block_stack[-1].add(node)
			block_stack.append(node)

		return root.children


	def _get_source_lines(self, source: str) -> list[str]:
		if self.enable_div_shortcut:
			source = self._div_shorcut_re.sub(r"\1%div\2", source)

		lines = []

		# Lines that end with CONTINUED_LINE are merged with the next line
		continued_line: list[str] = []
		source_lines = self._extract_filter_blocks(source)

		for line in source_lines:
			line = line.rstrip()

			if line and line.lstrip()[0] == self.LINE_COMMENT:
				# Add empty line for debug mode
				lines.append('')

			elif line and line[-1] == self.CONTINUED_LINE:
				# If its not the first continued line we strip
				# the whitespace from the beginning
				if continued_line:
					line = line.lstrip()

				# Strip of the CONTINUED_LINE character and save for later
				continued_line.append(line[:-1])

			elif continued_line:
				# If we have a continued line we join them together and add
				# them to the other lines
				continued_line.append(line.strip())
				lines.append(''.join(continued_line))

				# Add empty lines for debug mode
				lines.extend(['']*(len(continued_line)-1))

				# Reset
				continued_line = []

			else:
				lines.append(line)

		return lines


	def _extract_filter_blocks(self, source: str) -> list[str]:
		lines = []
		filter_block = None
		filter_start_indent = None # The indent level of the filter start tag
		filter_block_indent = None # The indent level of the first content in the block

		for line in source.rstrip().split("\n"):
			stripped_line = line.lstrip()

			if filter_block is not None:
				if not stripped_line: # type: ignore[unreachable]
					filter_block.append(stripped_line)
					continue

				# Find the block indent level if this is the first non
				# whitespace line after the start of the block
				if filter_block_indent is None:
					filter_block_indent = line[:len(line) - len(stripped_line)]

				# We are inside the block as long as the lines are at least
				# indented with the filter_block_indent level.
				# If an empty filter block is defined, filter_block_indent may
				# not be correct, because the first non-whitespace line which
				# is used to get the indent level may already be outside the
				# block. So if the line starts with both filter_start_indent
				# and the filter_block_indent and they are not equal we should
				# be inside the block.
				if line.startswith(filter_block_indent) and \
					line.startswith(filter_start_indent) and \
					filter_block_indent != filter_start_indent:

					filter_block.append(line[len(filter_block_indent):])
					continue

				lines.append('\n'.join(filter_block))
				filter_block = None
				filter_block_indent = None

			if not stripped_line:
				# We just leave the whitespace as it is and let it be handled elsewhere
				lines.append(line)

			elif stripped_line.startswith(self.FILTER_START) and \
				self._filter_is_defined(stripped_line):

				# A known filter was found so we start a to collect the filter block
				filter_block = [line.rstrip()]
				filter_start_indent = line[:len(line) - len(stripped_line)]

			else:
				lines.append(line)

		if filter_block is not None:
			lines.append('\n'.join(filter_block))

		return lines


	def _parse_line(self, lineno: int, line: str) -> Node:
		inline_data = None

		if self._has_inline_data(line):
			line, inline_data = self._parse_inline_data(line)

		node: Node

		if self._has_nested_tags(line):
			node = self._parse_nested_tags(lineno, line)

		else:
			node = self._parse_node(lineno, line)

		if inline_data is not None:
			if not node.can_have_children():
				raise TemplateSyntaxError("Node can't contain inline data", lineno)

			if isinstance(node, NestedTags) and isinstance(node.nodes[-1], TextNode):
				raise TemplateSyntaxError("TextNode can't contain inline data", lineno)

			return InlineData(node, inline_data)

		return node


	def _parse_node(self, lineno: int, line: str) -> Node:
		if line.startswith(self.HTML_TAG):
			return self._parse_html(lineno, line)

		if line.startswith(self.JINJA_TAG):
			return self._parse_jinja(lineno, line)

		if line.startswith(self.PREFORMATED_LINE):
			return PreformatedText(line[1:])

		if line.startswith(self.JINJA_VARIABLE):
			return JinjaVariable(line[1:])

		if line.startswith(self.FILTER_START) and self._filter_is_defined(line.split('\n')[0]):
			return self._create_filter_node(lineno, line)

		if line.startswith(self.DOCTYPE_TAG):
			if len(line) == 3:
				return TextNode("<!DOCTYPE HTML>")

			value = line[3:].lower()

			if value == "html5":
				return TextNode("<!DOCTYPE HTML>")

			try:
				data = DOCTYPES[value]

			except KeyError:
				raise TemplateSyntaxError(f"Invalid doctype: '{value}'", lineno) from None

			return TextNode(f"<!DOCTYPE HTML PUBLIC \"-//W3C/DTD {data[0]}//EN\", \"{data[1]}\">")

		if line.startswith(self.ESCAPE_LINE):
			return TextNode(line[1:])

		return TextNode(line)


	def _filter_is_defined(self, line: str) -> bool:
		if line[1:].strip() in self.filters:
			return True

		return False

	# The filter block data should be a single line string
	# that contains both the start tag definion and the content
	# of the block.
	# ie. :testfilter\nblock content\nblock content\n
	def _create_filter_node(self, lineno: int, filter_block_data: str) -> Node:
		data = filter_block_data.split("\n")
		name = data[0].strip()[1:]
		content = '\n'.join(data[1:])

		if not content.strip():
			raise TemplateSyntaxError(f"Empty filter block ({name})", lineno)

		return FilterNode(self.filters[name], content)


	def _has_inline_data(self, line: str) -> bool:
		if line[0] not in self._inline_data_tags:
			return False

		return self.INLINE_DATA_SEP in line


	def _parse_inline_data(self, line: str) -> tuple[str, str]:
		data = line.split(self.INLINE_DATA_SEP, 1)
		return data[0].rstrip(), data[1].lstrip()


	def _has_nested_tags(self, line: str) -> bool:
		if line[0] not in self._nested_tags:
			return False

		return self.NESTED_TAGS_SEP in line


	def _parse_nested_tags(self, lineno: int, line_str: str) -> NestedTags:
		tags = line_str.split(self.NESTED_TAGS_SEP)

		nodes: list[Node] = []
		node_lines: list[str] = [] # Used to make a nicer error message

		for line in [x.strip() for x in tags]:
			node = self._parse_node(lineno, line)

			if nodes and not nodes[-1].can_have_children():
				raise TemplateSyntaxError(
					f"Node '{node_lines[-1]}' can't contain children'", lineno
				)

			nodes.append(node)
			node_lines.append(line)

		return NestedTags(nodes)


	def _parse_html(self, lineno: int, line: str) -> HTMLTag:
		m = re.match(r"^(\w+)(.*)$", line[1:])
		if m is None:
			raise TemplateSyntaxError(f"Expected html tag, got '{line}'", lineno)

		tag = m.group(1)
		attrs = m.group(2)
		self_closing = False

		if attrs and attrs[-1] == self.SELF_CLOSING_TAG:
			self_closing = True
			attrs = attrs[:-1].rstrip()

		elif tag in self._self_closing_html_tags:
			self_closing = True

		if attrs.startswith(self.ID_SHORTCUT) or \
			attrs.startswith(self.CLASS_SHORTCUT):
			attrs = self._parse_shortcut_attributes(attrs)

		elif attrs and attrs[0] == "(" and attrs[-1] == ")":
			attrs = " " + attrs[1:-1]

		if self_closing:
			return SelfClosingHTMLTag(tag, attrs)

		return HTMLTag(tag, attrs)


	def _parse_shortcut_attributes(self, attr_string: str) -> str:
		orig_attrs = attr_string
		value = attr_string
		extra_attrs = ""

		# Extract extra attrs from parentheses, otherwise, split on first space
		m = re.match(r"^([\.#0-9A-Za-z\-]+)\((.+?)\)$", value)

		if m:
			value, extra_attrs = m.group(1), m.group(2)

		elif ' ' in value:
			value, extra_attrs = attr_string.split(" ", 1)

		parts = re.split(r"([\.#])", value)

		# The first part should be empty
		parts = parts[1:]

		# Now parts should be a list like this ['.', 'value', '#', 'value']
		# So we take every second element starting from the first
		# and every second element starting from the second and zip them
		# together.
		parts = list(zip(parts[0::2], parts[1::2]))

		classes = []
		ids = []

		# mypy complains "Unpacking a string is disallowed"
		for type_, value in parts: # type: ignore
			if not value:
				# ignore empty values
				continue

			if type_ == self.CLASS_SHORTCUT:
				classes.append(value)

			else:
				ids.append(value)

		attrs: tuple[tuple[str, list[str]], tuple[str, list[str]]]

		# We make the class and id the same order as in the template
		if orig_attrs.startswith(self.CLASS_SHORTCUT):
			attrs = (("class", classes), ("id", ids))

		else:
			attrs = (("id", ids), ("class", classes))

		rv = " ".join(f"{k}=\"{' '.join(v)}\"" for k, v in attrs if v)

		if extra_attrs:
			rv += " " + extra_attrs

		if rv:
			return " " + rv

		return rv


	def _parse_jinja(self, lineno: int, line: str) -> JinjaTag:
		m = re.match(r"^(\w+)(.*)$", line[1:])

		if m is None:
			raise TemplateSyntaxError(f"Expected jinja tag, got '{line}'.", lineno)

		tag = m.group(1)
		attrs = m.group(2)

		if tag in self._self_closing_jinja_tags:
			return SelfClosingJinjaTag(tag, attrs)

		if tag in self._extended_tags:
			return ExtendingJinjaTag(tag, attrs)

		return JinjaTag(tag, attrs)


	def _create_extended_jinja_tags(self, nodes: list[JinjaTag | Node]) -> list[JinjaTag | Node]:
		jinja_a: JinjaTag | None = None
		ext_node: Node | None = None
		ext_nodes: list[Node] = []

		for node in nodes:
			if isinstance(node, EmptyLine):
				continue

			if node.has_children():
				node.children = self._create_extended_jinja_tags(node.children)

			if not isinstance(node, JinjaTag):
				jinja_a = None
				continue

			if jinja_a is None:
				jinja_a = node
				continue

			if node.tag_name in self._extended_tags and \
				jinja_a.tag_name not in self._extended_tags[node.tag_name]:

				jinja_a = node
				continue

			if node.tag_name in self._extended_tags and \
				jinja_a.tag_name in self._extended_tags[node.tag_name]:

				if ext_node is None:
					ext_node = ExtendedJinjaTag()
					ext_node.add(jinja_a)
					ext_nodes.append(ext_node)

				ext_node.add(node)

			else:
				ext_node = None
				jinja_a = node

		# replace the nodes with the new extended node
		for node in ext_nodes:
			nodes.insert(nodes.index(node.children[0]), node)

			index = nodes.index(node.children[0])
			del nodes[index:index+len(node.children)]

		return nodes


class Output:
	"Class for writing a Jinja template"

	def __init__(self,
				indent_string: str = "    ",
				newline_string: str = "\n",
				debug: bool = False,
				block_start_string: str = "{%",
				block_end_string: str = "%}",
				variable_start_string: str = "{{",
				variable_end_string: str = "}}"):
		"""
			Create a new ``Output`` object

			:param indent_string: String to use for each indent level if ``mode`` is not
				:attr:`OutputMode.COMPACT`
			:param newline_string: String to use as a newline character
			:param debug: Make the output more debug-friendly
			:param block_start_string: String to use for the start of Jinja blocks
			:param block_end_string: String to use for the end of JInja blocks
			:param variable_start_string: String to use for the start of Jinja variable blocks
			:param variable_end_string: String to use for the end of Jinja variable blocks
		"""

		self._indent: str = indent_string
		self._newline: str = newline_string

		self.debug: bool = debug
		self.buffer: list[str] = []
		self.block_start_string: str = block_start_string
		self.block_end_string: str = block_end_string
		self.variable_start_string: str = variable_start_string
		self.variable_end_string: str = variable_end_string


	def create(self, nodes: list[Node]) -> str:
		"""
			Create a jinja template from a list of :class:`Node` objects

			:param nodes: A list of nodes
		"""

		self.buffer.clear()
		self._create(nodes)

		if self.debug:
			return "".join(self.buffer)

		return "".join(self.buffer).strip()


	def write_self_closing_html(self, node: HTMLTag) -> None:
		"""
			Write a self-closing HTML tag to the buffer

			:param node: Node to be written
		"""

		self.write(f"<{node.tag_name}{node.attrs} />")


	def write_open_html(self, node: HTMLTag) -> None:
		"""
			Write the opening HTML tag for a node to the buffer

			:param node: Node to be written
		"""

		self.write(f"<{node.tag_name}{node.attrs}>")


	def write_close_html(self, node: HTMLTag) -> None:
		"""
			Write the closing HTML tag for a node to the buffer

			:param node: Node to be written
		"""

		self.write(f"</{node.tag_name}>")


	def write_open_jinja(self, node: JinjaTag) -> None:
		"""
			Write the opening Jinja block for a node to the buffer

			:param node: Node to be written
		"""

		self.write(f"{self.block_start_string} {node.tag_name}{node.attrs} {self.block_end_string}")


	def write_close_jinja(self, node: JinjaTag) -> None:
		"""
			Write the closing Jinja block for a node to the buffer

			:param node: Node to be written
		"""

		self.write(f"{self.block_start_string} end{node.tag_name} {self.block_end_string}")


	def write_jinja_variable(self, node: JinjaVariable) -> None:
		"""
			Write a Jinja variable block to the buffer

			:param node: Node to be written
		"""

		self.write(f"{self.variable_start_string} {node.data} {self.variable_end_string}")


	def write_newline(self) -> None:
		"Write a newline character to the buffer"

		self.write(self._newline)


	def write_indent(self, depth: int) -> None:
		"""
			Write an indent string to the buffer

			:param depth: Amount to indent by
		"""

		self.write(self._indent * depth)


	def write(self, data: str) -> None:
		"""
			Write a string to the buffer

			:param data: String to be written
		"""

		self.buffer.append(data)


	def write_open_node(self, node: Node) -> None:
		"""
			Write an open tag or block node to the buffer

			:param node: Node to be written
		"""

		if isinstance(node, JinjaTag):
			self.write_open_jinja(node)

		elif isinstance(node, NestedTags):
			for n in node.nodes:
				self.write_open_node(n)

		elif isinstance(node, SelfClosingHTMLTag):
			self.write_self_closing_html(node)

		elif isinstance(node, HTMLTag):
			self.write_open_html(node)

		elif isinstance(node, JinjaVariable):
			self.write_jinja_variable(node)

		elif isinstance(node, PreformatedText):
			self.write(node.data)

		elif isinstance(node, TextNode):
			self.write(node.data)


	def write_close_node(self, node: Node) -> None:
		"""
			Write a close tag or block node to the buffer

			:param node: Node to be written
		"""

		if isinstance(node, SelfClosingTag):
			return

		if isinstance(node, NestedTags):
			for n in reversed(node.nodes):
				self.write_close_node(n)

		elif isinstance(node, JinjaTag):
			self.write_close_jinja(node)

		elif isinstance(node, HTMLTag):
			self.write_close_html(node)

		elif isinstance(node, ExtendedJinjaTag):
			self.write_close_node(node.children[0])


	def _create(self, nodes: list[Node], depth: int = 0) -> None:
		for node in nodes:
			if isinstance(node, EmptyLine):
				if self.debug:
					self.write_newline()

				continue

			if isinstance(node, InlineData):
				self.write_indent(depth)
				self.write_open_node(node.node)
				self.write(node.data)
				self.write_close_node(node.node)
				self.write_newline()

			elif isinstance(node, ExtendedJinjaTag):
				for n in node.children:
					self.write_indent(depth)
					self.write_open_node(n)
					self.write_newline()

					if n.has_children():
						self._create(n.children, depth+1)

			else:
				if not isinstance(node, (PreformatedText, FilterNode)):
					self.write_indent(depth)

				self.write_open_node(node)

				if isinstance(node, SelfClosingTag):
					self.write_newline()

				elif isinstance(node, PreformatedText):
					self.write("\n")

				elif isinstance(node, (JinjaTag, HTMLTag, NestedTags)) and not node.has_children():
					pass

				else:
					self.write_newline()

			if node.children and not isinstance(node, ExtendedJinjaTag):
				self._create(node.children, depth+1)

			if self.debug:
				# Pop off all whitespace above this end tag and save it to be appended after the end
				# tag.
				prev = []

				while self.buffer[-1].isspace():
					prev.append(self.buffer.pop())

			if isinstance(node, SelfClosingTag):
				pass

			elif isinstance(node, (JinjaTag, HTMLTag, ExtendedJinjaTag, NestedTags)):
				if not (self.debug or (isinstance(node, NestedTags) and not node.has_children())):
					self.write_indent(depth)

				self.write_close_node(node)

				if not self.debug or (isinstance(node, NestedTags) and not node.has_children()):
					self.write_newline()

			if self.debug:
				# readd the whitespace after the end tag
				self.write(''.join(prev))
