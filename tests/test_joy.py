"""Unit tests for joy.

To run tests:

    $ py.test .
"""
from joy import render_tag
import pytest
import re
import yaml
from pathlib import Path

def test_render_tag():
    assert render_tag("circle") == "<circle >"
    assert render_tag("circle", cx=0, cy=0, r=10) == '<circle cx="0" cy="0" r="10">'
    assert render_tag("circle", cx=0, cy=0, r=10, close=True) == '<circle cx="0" cy="0" r="10" />'
    assert render_tag("circle", fill='text "with" quotes') == '<circle fill="text &quot;with&quot; quotes">'


def read_tests_files():
    tests = []
    p = Path(__file__).parent
    files = p.rglob('*.yml')
    for f in files:
        items = list(yaml.safe_load_all(f.open()))
        items = [dict(item, name="{}: {}".format(f.name, item['name'])) for item in items]
        tests.extend(items)
    return tests

# Get all tests
testdata = read_tests_files()
test_ids = [t['name'] for t in testdata]

@pytest.mark.parametrize('testspec', testdata, ids=test_ids)
def test_shapes(testspec):
    code = testspec['code']
    expected = testspec['expected']

    env = {}
    exec("from joy import *", env, env)
    node = eval(code, env)

    # svg = normalize_space(node._svg())
    # expected = normalize_space(expected)
    svg = node._svg().strip()
    expected = expected.strip()

    assert expected == svg

def normalize_space(text):
    return re.sub("\s+", " ", text).strip()
