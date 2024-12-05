import unittest

from .compact_output import TestCompactOutput # noqa: F401
from .debug_output import TestDebugOutput # noqa: F401
from .div_shortcut import TestDivShortcut # noqa: F401
from .filters import TestFilters # noqa: F401
from .haml_tags import TestHamlTags # noqa: F401
from .html_tags import TestHtmlTags # noqa: F401
from .jinja_tags import TestJinjaTags, TestJinjaTagsCustomPlaceholders # noqa: F401
from .syntax import TestSyntax # noqa: F401

unittest.main()
