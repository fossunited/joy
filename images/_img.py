from joy import *

def render(*shapes):
    """Renders the shapes as svg and prints them.
    """
    bg = combine(
        rect(x=-150, y=-150, width=300, height=300, fill="white", stroke="#ddd"),
        line(x1=-150, y1=0, x2=150, y2=0, stroke="#ddd"),
        line(x1=0, y1=-150, x2=0, y2=150, stroke="#ddd"))

    shape = group(
        [bg, *shapes],
        stroke_width=2 # increase the stroke-width to compensate for scaling
    )
    shape = scale(shape, xs=0.5)
    svg = SVG([shape], width=150, height=150)
    print(svg)