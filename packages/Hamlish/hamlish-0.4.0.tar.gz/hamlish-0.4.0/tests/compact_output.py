from hamlish import Hamlish, Output

from .base import TestCase


class TestCompactOutput(TestCase):
	def setUp(self) -> None:
		self.hamlish = Hamlish(
			Output(
				indent_string = "",
				newline_string = "",
				debug = False
			)
		)


	def test_pre_tags(self) -> None:
		s = self._h("""
%pre
    |def test():
    |    if 1:
    |        print "Test"
""")

		r = """<pre>def test():
    if 1:
        print "Test"
</pre>\
"""

		self.assertEqual(s, r)
