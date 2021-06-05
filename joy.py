"""
Joy
===

Joy is a tiny creative coding library in Python.

BASIC USAGE

An example of using joy:

    >>> from joy import *
    >>>
    >>> c = circle(cx=100, cy=100, r=50)
    >>> show(c)

The `cicle` function creates a new circle and the `show` function
displys it.

PRINCIPLES

Joy follows functional programming approach for it's interface. Each
function/class gives a shape and those shapes can be transformed and
combined using other utililty functions.

By design, there is no global state in the library.

Joy uses SVG to render the shapes and the shapes are really a very thin
wrapper over SVG nodes. It is possible to use every functionality of SVG,
even if that is not exposed in the API.

COORDINATE SYSTEM

Joy uses a canvas with (0, 0) as the center of the canvas.

By default the size of the canvas is (300, 300).

BASIC SHAPES

Joy supports `circle`, `rect` and `line` as basic shapes.

    >>> c = circle(cx=100, cy=100, r=50)
    >>> r = rect(x=-100, y=-100, width=200, height=200)
    >>> show(c, r)

All basic shapes have default values of all the arguments, making it
easier to start using them.

    >>> circle()
    <circle {'cx': 0, 'cy': 0, 'r': 100}>
    >>> rect()
    <rect {'x': -100, 'y': -100, 'width': 100, 'height': 100}>
    >>> line()
    <line {'x1': -100', 'y1': 0, 'x2': 100, 'y2': 0}

COMBINING SHAPES

The `combine` function is used to combine multiple shapes into a
single shape.

    >>> c = combine(circle(), rect())
    >>> show(c)

TRANSFORMATIONS

Joy supports `translate`, `rotate` and `scale` transformations.

The `translate` functions moves the given shape by `x` and `y`.

    >>> c = circle(cx=0, cy=0, r=50)
    >>> shape = combine(c, translate(c, x=50, y=0))
    >>> show(c)

The `rotate` function rotates a shape anti-clockwise by the specified
angle.

    >>> shape = rotate(rect(), angle=45)
    >>> show(shape)

By default the `rotate` function rotates the shape around the origin.
However, it is possible to specify the reference point for rotation
using the `x` and `y` parameters.

    >>> shape = rotate(rect(), angle=45, x=100, y=100)
    >>> show(shape)

The `scale` function scales a shape.

    >>> shape = scale(circle(), sx=1, sy=0.5)
    >>> show(shape)

HIGER ORDER TRANSFORMATIONS

Joy supports a transorm called `cycle` to rotate a shape multiple times
with angle from 0 to 360 degrees and combining all the resulting shapes.

    >>> flower = cycle(rect())
    >>> show(flower)

By default, cycle repeats the rotation for 18 times, however that can be
customizing by specifying the parameter `n`.

    >>> shape = cycle(rect(), n=3)
    >>> show(shape)

JUPYTER LAB INTEGRATION

Joy integrates very well with Jupyter notebooks and every shape is
represented as SVG image by jupyter.
"""
import html

__version__ = "0.1"
__author__ = "Anand Chitipothu <anand@fossunited.org>"

SQRT2 = 2**0.5

class Shape:
    """Shape is the base class for all shapes in Joy.

    A Shape is an SVG node and supports converting it self into svg text.

    Typically, users do not interact with this class directly, but use it
    through it's subclasses.
    """
    def __init__(self, tag, children=None, **attrs):
        """Creates a new shape.
        """
        self.tag = tag
        self.children = children
        self.attrs = attrs

    def __repr__(self):
        return f"<{self.tag} {self.attrs}>"

    def __getattr__(self, name):
        if not name.startswith("_") and name in self.attrs:
            return self.attrs[name]
        else:
            raise AttributeError(name)

    def _svg(self, indent="") -> str:
        """Returns the svg representation of this node.

        This method is used to recursively construct the svg of a node
        and it's children.

            >>> c = circle(cx=100, cy=100, r=50)
            >>> c._svg()
            '<circle cx="100" cy="100" r="50" />'
        """
        if self.children:
            tag_text = render_tag(self.tag, **self.attrs, close=False)
            return (
                indent + tag_text + "\n" +
                "".join(c._svg(indent + "  ") for c in self.children) +
                indent + "</" + self.tag + ">\n"
            )
        else:
            tag_text = render_tag(self.tag, **self.attrs, close=True)
            return indent + tag_text + "\n"

    def as_svg(self, width=300, height=300) -> str:
        """Renders this node as svg image.

        The svg image is assumed to be of size (300, 300) unless the
        width and the height arguments are provided.

        Example:

            >>> c = circle(cx=100, cy=100, r=50)
            >>> print(c.as_svg())
            <svg width="300" height="300" viewBox="-150 -150 300 350" fill="none" stroke="black" xmlns="http://www.w3.org/2000/svg">
              <circle cx="100" cy="100" r="50" />
            </svg>
        """
        return SVG([self], width=width, height=height).render()

    def _repr_svg_(self):
        """Returns the svg representation of this node.

        This method is called by Juputer to render this object as an
        svg image.
        """
        return self.as_svg()

class SVG:
    """SVG renders any svg element into an svg image.
    """
    def __init__(self, nodes, width=300, height=300):
        self.nodes = nodes
        self.width = width
        self.height = height

    def render(self):
        svg_header = render_tag(
            tag="svg",
            width=self.width,
            height=self.height,
            viewBox=f"-{self.width//2} -{self.height//2} {self.width} {self.height}",
            fill="none",
            stroke="black",
            xmlns="http://www.w3.org/2000/svg") + "\n"
        svg_footer = "</svg>\n"

        nodes = "".join(node._svg(indent="  ") for node in self.nodes)
        return svg_header + nodes + svg_footer

    def _repr_svg_(self):
        return self.render()

    def __str__(self):
        return self.render()

    def __repr__(self):
        return "SVG:{self.nodes}"


class circle(Shape):
    """Creates a circle shape.

    Parameters:
        cx:
            The x-coordinate of the center of the circle.
            Defaults to 0 when not specified.

        cy:
            The y-coordinate of the center of the circle.
            Defaults to 0 when not specified.

        r:
            The radius of the circle.
            Defaults to 100 when not specified.

    Examples:

    Draw a circle with center at (100, 100) and radius as 50.

        >>> c = circle(cx=100, cy=100, r=50)
        >>> show(c)

    When no arguments are specified, it uses (0, 0) as the center and
    100 as the radius.

        >>> c = circle()
        >>> show(c)
    """
    def __init__(self, **kwargs):
        cx = kwargs.pop("cx", 0)
        cy = kwargs.pop("cy", 0)
        r = kwargs.pop("r", 100)
        super().__init__("circle", cx=cx, cy=cy, r=r, **kwargs)

class rect(Shape):
    """Creates a rectangle shape.

    Parameters:
        x:
            The x-coordinate of the top-left corner of the rectangle.

        y:
            The y-coordinate of the top-left corner of the rectangle.

        width:
            The width of the rectangle.

        height:
            The height of the rectangle.

    Examples:

    Draw a rectangle with top-left corner at (100, 100) and with a width
    of 200 and height of 100.

        >>> r = rect(x=100, y=100, width=200, height=100)
        >>> show(r)

    When no arguments are specified, it draws a rectangle with a width
    of 200 and a height of 200, centered around the origin.

        >>> r = rect()
        >>> show(r)

    It is also possible to specify just the width and height to create a
    rectangle centered around origin.

        >>> r = rect(width=200, height=100)
        >>> show(r)
    """
    def __init__(self, **kwargs):
        width = kwargs.pop("width", 200)
        height = kwargs.pop("height", 200)
        x = kwargs.pop("x", -width/2)
        y = kwargs.pop("y", -height/2)
        super().__init__("rect", x=x, y=y, width=width, height=height, **kwargs)

class line(Shape):
    """Basic shape for drawing a line connecting two points.

    Parameters:
        x1:
            The x-coordinate of the starting point of the line.

        y1:
            The y-coordinate of the starting point of the line.

        x2:
            The x-coordinate of the ending point of the line.

        y2:
            The y-coordinate of the ending point of the line.

    Examples:

    Draw a line from (0, 0) to (100, 50).

        >>> shape = line(x1=0, y1=0, x2=100, y2=50)
        >>> show(shape)

    When no arguments are specified, it draws a line from (-100, 0) to
    (100, 0).

        >>> shape = line()
        >>> show(shape)
    """
    def __init__(self, **kwargs):
        x1 = kwargs.pop("x1", -100)
        y1 = kwargs.pop("y1", 0)
        x2 = kwargs.pop("x2", 100)
        y2 = kwargs.pop("y2", 0)
        super().__init__("line", x1=x1, y1=y1, x2=x2, y2=y2, **kwargs)

class group(Shape):
    """Creates a container to group a list of shapes.

    This class is not meant for direct consumption of the users. Users
    are recommended to use `combine` to combine multiple shapes and use
    `translate`, `rotate` and `scale` for doing transformations.

    This creates an svg <g> element.

    Parameters:
        shapes:
            The list of shapes to group.

        transform:
            The transformation to apply as an string.

    Examples:

    Combine a circle and a rectangle.

        >> c = circle()
        >> r = rect()
        >>> shape = group([c, r])
        >>> show(shape)

    Transformations can specified when creating a group.

        >> c = circle()
        >> r = rect()
        >>> shape = group([c, r], transform="scale(1, 0.5))
        >>> show(shape)

    Refer to SVG documentation to understand the transform parameter.
    """
    def __init__(self, shapes, transform=None, **kwargs):
        super().__init__("g", children=shapes, transform=transform, **kwargs)

def render_tag(tag, *, close=False, **attrs):
    """Renders a html/svg tag.

        >>> render_tag("circle", cx=0, cy=0, r=10)
        '<circle cx="0" cy="0" r="10">'

    When `close=True`, the tag is closed with "/>".

        >>> render_tag("circle", cx=0, cy=0, r=10, close=True)
        '<circle cx="0" cy="0" r="10" />'

    Underscore characters in the attribute name are replaced with hypens.

        >>> render_tag("circle", cx=0, cy=0, r=10, stroke_width=2)
        '<circle cx="0" cy="0" r="10" stroke-width="2">'
    """
    end = " />" if close else ">"

    items = [(k.replace("_", "-"), html.escape(str(v))) for k, v in attrs.items() if v is not None]
    attrs_text = " ".join(f'{k}="{v}"' for k, v in items)

    return f"<{tag} {attrs_text}{end}"

def combine(*shapes):
    """Combines multiple shapes in to a single shape by overlaying all
    the shapes.

        >>> shape = combine(circle(), rect())
        >>> show(shape)
    """
    return group(shapes)

def translate(shape, x=0, y=None):
    """Return a new shape containing given shape moved by x and y.

    Parameters:
        shape:
            The shape to translate

        x:
            The number of units to move in the x direction

        y:
            The number of units to move in the y direction

    Example:

    Translate a circle by (100, 50).

        >>> c = translate(circle(), 100, 50)
        >>> show(c)
    """
    if y is None:
        y = x
    return group([shape], transform=f"translate({x} {y})")

def rotate(shape, angle, x=None, y=None):
    """Returns a new shape containing the given shape rotated by
    the specified angle.

    The shape is rotated around the point (x, y), which defaults to
    (0, 0) when not specified.

    Parameters:

        shape:
            The shape to rotate.

        angle:
            The angle to rotate the shape in degrees.

        x:
            The x-coordinate of the reference point used for rotation.
            Defaults to 0 when not specified.

        y:
            The y-coordinate of the reference point used for rotation.
            Defaults to 0 when not specified.

    Examples:

    Rotates a square by 45 degrees.

        >>> shape = rotate(rect(), 45)
        >>> show(shape)

    Rotate a rectangle around it's top-left corner and
    combine with it self.

        >>> r = rect(x=-50, y=-50, w=100, h=100)
        >>> shape = combine(r, rotate(r, 45, x=r.x, y=r.y))
        >>> show(shape)
    """
    args = f"{angle}"
    if x is not None and y is not None:
        args += f" {x} {y}"
    return group([shape], transform=f"rotate({args})")

def scale(shape, xs, ys=None):
    """Returns a new shape containing the given shape scaled by xs and
    ys in horizontally and vertically respectively.

    Parameters:

        shape:
            The shape to scale.

        xs:
            The scale factor in the horizontal direction.

        ys:
            The scale factor in the horizontal direction. Defaults to
            the value of xs if not provided.
    """
    if ys is None:
        ys = xs
    return group([shape], transform=f"scale({xs} {ys})")

def cycle(shape, n=18, x=0, y=0, s=None, angle=None):
    """
    Rotates the given shape repeatedly and combines all the resulting
    shapes.

    The cycle function is very amazing transformation and it creates
    surprising patterns.

    Parameters:

        shape:
            The shape to cycle.

        n:
            The number of times to rotate. This also determines the
            angle of each rotation, which will be 360/n.

        x:
            The x-coordinate of the reference point used for rotation.
            Defaults to 0 when not specified.

        y:
            The y-coordinate of the reference point used for rotation.
            Defaults to 0 when not specified.

        s:
            Optional scale factor to scale the shape for each rotation.
            This can be used to grow or shrink the shape while rotating.

        angle:
            Optional angle of rotation. Defaults to 360/n when not
            specified,
    Examples:

    Cycle a line:

        >>> shape = cycle(line())
        >>> show(shape)

    Cycle a square:

        >>> shape = cycle(rect())
        >>> show(shape)

    Cycle a rectangle:

        >>> shape = cycle(rect(width=200, height=100))
        >>> show(shape)

    Cycle an ellipse:

        >>> e = scale(circle(), xs=1, ys=0.5)
        >>> show(cycle(e))

    Create a spiral with shirnking squares:

        >>> shape = cycle(rect(width=300, height=300), n=72, s=0.92)
        >>> show(shape)
    """
    angle = angle if angle is not None else 360/n
    shapes = [rotate(shape, i*angle, x, y) for i in range(n)]
    if s is not None:
        shapes = [scale(shape_, xs=s**i) for i, shape_ in enumerate(shapes)]
    return group(shapes)

def show(*shapes):
    """Shows the given shapes.

    It also adds a border to the canvas and axis at the origin with
    a light color as a reference.

    Parameters:

        shapes:
            The shapes to show.

    Examples:

    Show a circle:

        >>> show(circle())

    Show a circle and square.

        >>> c = circle()
        >>> s = rect()
        >>> show(c, s)
    """
    markers = [
        rect(x=-150, y=-150, width=300, height=300, stroke="#ddd"),
        line(x1=-150, y1=0, x2=150, y2=0, stroke="#ddd"),
        line(x1=0, y1=-150, x2=0, y2=150, stroke="#ddd")
    ]
    shapes = markers + list(shapes)
    img = SVG(shapes)

    from IPython.display import display
    display(img)
