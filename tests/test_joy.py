"""Unit tests for joy.

To run tests:

    $ py.test .
"""
from joy import (
    render_tag,
    Point,
    Translate,  Rotate)
import pytest
import re
import yaml
from pathlib import Path

@pytest.fixture()
def reset_joy():
    import joy
    # reset id_suffix and shape counter
    joy.ID_SUFFIX = "0000"
    joy.shape_seq = joy.shape_sequence()
    yield

def test_render_tag():
    assert render_tag("circle") == "<circle>"
    assert render_tag("circle", cx=0, cy=0, r=10) == '<circle cx="0" cy="0" r="10">'
    assert render_tag("circle", cx=0, cy=0, r=10, close=True) == '<circle cx="0" cy="0" r="10" />'
    assert render_tag("circle", fill='text "with" quotes') == '<circle fill="text &quot;with&quot; quotes">'

def test_rotate():
    assert Rotate(angle=45).as_str() == "rotate(45)"
    assert Rotate(angle=45, anchor=Point(10, 20)).as_str() == "rotate(45 10 20)"

def test_translate():
    assert Translate(x=10, y=20).as_str() == "translate(10 20)"

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
def test_shapes(testspec, reset_joy):
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
    return re.sub(r"\s+", " ", text).strip()
