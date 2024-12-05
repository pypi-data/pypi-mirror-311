from jinja2 import TemplateSyntaxError


class TemplateIndentationError(TemplateSyntaxError):
	"Raise when a line in the template is indented improperly"
