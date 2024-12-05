__version__: str = "0.4.0"


try:
	from .docnode import HTMLTag, JinjaTag, Node
	from .exception import TemplateIndentationError
	from .extension import HamlishExtension, HamlishSettings, HamlishTagExtension
	from .parser import Hamlish, Output, OutputMode

except ModuleNotFoundError:
	pass
