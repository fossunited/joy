from joy import *
from _img import render

def donut(x, y, r):
    c1 = Circle(center=Point(x=x, y=y), radius=r)
    c2 = Circle(center=Point(x=x, y=y), radius=r/2)
    return c1+c2

d = donut(0, 0, 100)
render(d)
