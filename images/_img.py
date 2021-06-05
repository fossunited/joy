from joy import *

def render(*shapes):
    """Renders the shapes as svg and prints them.
    """
    bg = combine(
        rect(x=-150, y=-150, width=300, height=300, fill="white", stroke="#ddd"),
        line(x1=-150, y1=0, x2=150, y2=0, stroke="#ddd"),
        line(x1=0, y1=-150, x2=0, y2=150, stroke="#ddd"))
    shape = combine(bg, *shapes)
    print(shape.as_svg())