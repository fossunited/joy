from joy import *
from _img import render

c = Circle(center=Point(x=100, y=0), radius=50)
shape = c | Repeat(36*4, Rotate(10) | Scale(0.97))
render(shape)

