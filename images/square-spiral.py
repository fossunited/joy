from joy import *
from _img import render

shape = Rectangle(width=300, height=300) | Repeat(72, Rotate(360/72) | Scale(0.92))
render(shape)
