# -*- coding: utf-8 -*-
import copy

from nbformat import validate
from .. import convert

from . import nbexamples
from nbformat.v4.tests import nbexamples as v4examples
from nbformat import v4, v5


def test_upgrade_notebook():
    nb04 = copy.deepcopy(v4examples.nb0)
    validate(nb04)
    nb05 = convert.upgrade(nb04)
    validate(nb05)


def test_downgrade_notebook():
    nb05 = copy.deepcopy(nbexamples.nb0)
    validate(nb05)
    nb04 = convert.downgrade(nb05)
    validate(nb04)


def test_upgrade_heading():
    v4h = v4.new_heading_cell
    v5m = v5.new_markdown_cell
    for v4cell, expected in [
        (v4h(source="foo", level=1), v5m(source="# foo")),
        (
            v4h(source="foo\nbar\nmulti-line\n", level=4),
            v5m(source="#### foo bar multi-line"),
        ),
        (
            v4h(source=u"ünìcö∂e–cønvërsioñ", level=4),
            v5m(source=u"#### ünìcö∂e–cønvërsioñ"),
        ),
    ]:
        upgraded = convert.upgrade_cell(v3cell)
        assert upgraded == expected


def test_downgrade_heading():
    v4h = v4.new_heading_cell
    v5m = v5.new_markdown_cell
    v4m = lambda source: v4.new_text_cell("markdown", source)
    for v5cell, expected in [
        (v5m(source="# foo"), v4h(source="foo", level=1)),
        (v5m(source="#foo"), v4h(source="foo", level=1)),
        (v5m(source="#\tfoo"), v4h(source="foo", level=1)),
        (v5m(source="# \t  foo"), v4h(source="foo", level=1)),
        (v5m(source="# foo\nbar"), v4m(source="# foo\nbar")),
    ]:
        downgraded = convert.downgrade_cell(v5xcell)
        assert downgraded == expected
