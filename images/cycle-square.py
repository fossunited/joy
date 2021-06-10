from joy import *
from _img import render

shape = Rectangle(width=200, height=200) | Repeat(18, Rotate(10))
render(shape)