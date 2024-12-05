from hamlish import HamlishTagExtension

from .base import HamlishEnvironment, TestCase


jinja_env = HamlishEnvironment(
	extensions = [
		HamlishTagExtension,
	]
)


class TestHamlTags(TestCase):
	def test_basic(self) -> None:
		s = jinja_env.from_string("""{% haml %}
%div
    %p
        test
{% endhaml %}
""")
		r = "<div><p>test</p></div>"
		self.assertEqual(s.render(), r)


	def test_multiple(self) -> None:
		s = jinja_env.from_string("""{% haml %}
%div
    %p
        test
{% endhaml %}
<div>hello</div>
{% haml %}
%div
    %p
        test
{% endhaml %}
""")

		r = "<div><p>test</p></div>\n<div>hello</div>\n<div><p>test</p></div>"
		self.assertEqual(s.render(), r)
