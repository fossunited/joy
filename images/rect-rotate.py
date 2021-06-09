from joy import *
from _img import render

r1 = Rectangle()
r2 = r1 | Rotate(angle=45) | Scale(1/SQRT2)
render(r1, r2)
