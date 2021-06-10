from joy import *
from _img import render

c = Circle(center=Point(x=-100, y=0), radius=50)
shape = c | Repeat(10, Translate(x=20, y=0))
render(shape)
