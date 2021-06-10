from joy import *

def render(*shapes):
    """Renders the shapes as svg and prints them.
    """
    bg = Group([
        Rectangle(width=300, height=300, fill="white", stroke="#ddd"),
        Line(start=Point(x=-150, y=0), end=Point(x=150, y=0), stroke="#ddd"),
        Line(start=Point(y=-150, x=0), end=Point(y=150, x=0), stroke="#ddd"),
    ])

    shape = Group(
        [bg, *shapes],
        stroke_width=2 # increase the stroke-width to compensate for scaling
    )
    shape = shape | Scale(0.5)
    svg = SVG([shape], width=150, height=150)
    print(svg)