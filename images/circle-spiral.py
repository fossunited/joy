from joy import *
from _img import render

c = circle(cx=100, cy=0, r=50)
shape = cycle(c, s=0.97, n=36*4, angle=10)
render(shape)
