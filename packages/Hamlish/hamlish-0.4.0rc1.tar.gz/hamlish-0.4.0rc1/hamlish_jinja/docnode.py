from __future__ import annotations

from typing import Any, Callable


__all__ = [
	"Node",
	"EmptyLine",
	"HTMLTag",
	"JinjaTag",
	"ExtendedJinjaTag",
	"TextNode",
	"FilterNode",
	"InlineData",
	"NestedTags",
	"PreformatedText",
	"SelfClosingTag",
	"SelfClosingJinjaTag",
	"SelfClosingHTMLTag",
	"JinjaVariable",
	"ExtendingJinjaTag"
]


class Node:
	"Represents a single HAML node in a template"

	def __init__(self) -> None:
		self.children: list[Node] = []


	def has_children(self) -> bool:
		# returns False if children is empty or contains only empty lines else True.
		return bool([x for x in self.children if not isinstance(x, EmptyLine)])


	def add(self, child: Node) -> None:
		self.children.append(child)


	def can_have_children(self) -> bool:
		return True


class EmptyLine(Node):
	# Used in debug mode.
	pass


class HTMLTag(Node):
	"Represents an HTML tag"

	def __init__(self, tag_name: str, attrs: str):
		Node.__init__(self)

		self.tag_name: str = tag_name
		self.attrs: str = attrs


class JinjaTag(Node):
	"Represents a Jinja tag"

	def __init__(self, tag_name: str, attrs: str):
		Node.__init__(self)

		self.tag_name: str = tag_name
		self.attrs: str = attrs


class ExtendedJinjaTag(Node):
	pass


class TextNode(Node):
	def __init__(self, data: str):
		Node.__init__(self)

		self.data = data


class FilterNode(TextNode):
	def __init__(self, filter_func: Callable[[str], str], data: str):
		TextNode.__init__(self, data)

		self.filter_func: Callable[[str], str] = filter_func


	def has_children(self) -> bool:
		return False


	@property
	def data(self) -> str:
		return self.filter_func(self._data)


	@data.setter
	def data(self, value: str) -> None:
		self._data = value


class InlineData(Node):
	def __init__(self, node: Node, data: str):
		Node.__init__(self)

		self.node: Any = node
		self.data: str = data


	def can_have_children(self) -> bool:
		return False


class NestedTags(Node):
	def __init__(self, nodes: list[Node]):
		Node.__init__(self)

		self.nodes: list[Node] = nodes


	def can_have_children(self) -> bool:
		# check if last node can have children
		return self.nodes[-1].can_have_children()


class PreformatedText(TextNode):
	pass


class SelfClosingTag:
	pass


class SelfClosingJinjaTag(JinjaTag, SelfClosingTag):
	def can_have_children(self) -> bool:
		return False


class SelfClosingHTMLTag(HTMLTag, SelfClosingTag):
	def can_have_children(self) -> bool:
		return False


class JinjaVariable(TextNode):
	pass


class ExtendingJinjaTag(JinjaTag, SelfClosingTag):
	pass
