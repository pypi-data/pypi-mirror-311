from jinja2 import TemplateSyntaxError

from .base import TestCase


class TestHtmlTags(TestCase):
	def test_content(self) -> None:
		s = self._h("""
%div
    Test
""")

		r = """\
<div>
  Test
</div>\
"""

		self.assertEqual(s, r)


	def test_content_with_attributes(self) -> None:
		s = self._h("""
%div id="test" class="test"
    Test
""")

		r = """\
<div id="test" class="test">
  Test
</div>\
"""
		self.assertEqual(s, r)


	def test_inline_content(self) -> None:
		s = self._h("""%div << Test""")
		r = """<div>Test</div>"""
		self.assertEqual(s, r)


	def test_inline_content_with_attributes(self) -> None:
		s = self._h("""%div class="test" id="test" << Test""")
		r = """<div class="test" id="test">Test</div>"""
		self.assertEqual(s, r)


	def test_empty_tags(self) -> None:
		s = self._h("""%div""")
		r = """<div></div>"""
		self.assertEqual(s, r)


	def test_self_closing(self) -> None:
		s = self._h("""
%br.
%hr.
%meta name="description".
%div.
%div class="test".
""")

		r = """\
<br />
<hr />
<meta name="description" />
<div />
<div class="test" />\
"""

		self.assertEqual(s, r)


	def test_auto_self_closing(self) -> None:
		s = self._h("""
%br
%hr
%meta name="description"
%input type="text"
%link rel="stylesheet"
%img src="test"
""")

		r = """\
<br />
<hr />
<meta name="description" />
<input type="text" />
<link rel="stylesheet" />
<img src="test" />\
"""

		self.assertEqual(s, r)


	def test_doctype(self) -> None:
		self.assertEqual(
			self._h("!!!"),
			"<!DOCTYPE HTML>"
		)

		self.assertEqual(
			self._h("!!!html5"),
			"<!DOCTYPE HTML>"
		)

		self.assertEqual(
			self._h("!!!strict"),
			'<!DOCTYPE HTML PUBLIC "-//W3C/DTD HTML 4.01//EN", "http://www.w3.org/TR/html4/strict.dtd">' # noqa: E501
		)

		self.assertEqual(
			self._h("!!!trans"),
			'<!DOCTYPE HTML PUBLIC "-//W3C/DTD HTML 4.01 Transitional//EN", "http://www.w3.org/TR/html4/loose.dtd">' # noqa: E501
	   ) # noqa: E122

		self.assertEqual(
			self._h("!!!frameset"),
			'<!DOCTYPE HTML PUBLIC "-//W3C/DTD HTML 4.01 Frameset//EN", "http://www.w3.org/TR/html4/frameset.dtd">' # noqa: E501
		)

		self.assertEqual(
			self._h("!!!xhtml"),
			'<!DOCTYPE HTML PUBLIC "-//W3C/DTD XHTML 1.1//EN", "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' # noqa: E501
		)

		self.assertEqual(
			self._h("!!!xstrict"),
			'<!DOCTYPE HTML PUBLIC "-//W3C/DTD XHTML 1.0 Strict//EN", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' # noqa: E501
		)

		self.assertEqual(
			self._h("!!!xtrans"),
			'<!DOCTYPE HTML PUBLIC "-//W3C/DTD XHTML 1.0 Transitional//EN", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">' # noqa: E501
	   ) # noqa: E122

		self.assertEqual(
			self._h("!!!xframeset"),
			'<!DOCTYPE HTML PUBLIC "-//W3C/DTD XHTML 1.0 Frameset//EN", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">' # noqa: E501
		)


	def test_invalid_self_closing(self) -> None:
		self.assertRaises(TemplateSyntaxError,
			lambda: self._h("""
%div.
    Test
"""))

	def test_invalid_self_closing_auto_close(self) -> None:
		self.assertRaises(TemplateSyntaxError,
			lambda: self._h("""
%br
    Test
"""))


	def test_invalid_self_closing_inline_data(self) -> None:
		self.assertRaises(TemplateSyntaxError,
			lambda: self._h("""
%div. << Test
"""))


	def test_invalid_self_closing_inline_data_auto_close(self) -> None:
		self.assertRaises(TemplateSyntaxError,
			lambda: self._h("""
%br << Test
"""))


	def test_invalid_doctype(self) -> None:
		self.assertRaises(
			TemplateSyntaxError,
			lambda: self._h("!!!merp")
		)
