from graph import *


brushColor("blue")
rectangle(0, 0, 1000, 300)

brushColor("green")
rectangle(0, 300, 1000, 600)

brushColor("red")
rectangle(50, 250, 150, 350)

penColor("white")
penSize(10)
brushColor("blue")
rectangle(75, 275, 125, 325)
penSize(1)
penColor("black")

brushColor("red")
polygon([(50, 250), (150, 250), (100, 210)])

brushColor("white")
circle(50, 40, 25)
brushColor("white")
circle(80, 40, 25)
brushColor("white")
circle(110, 40, 25)
brushColor("white")
circle(65, 70, 25)
brushColor("white")
circle(95, 70, 25)

brushColor("yellow")
circle(400, 100, 50)


def triangle(x, y, a, h, c):
    """Draw triangle x, y - start point, a - base 
    h - heigth, c - color"""
    brushColor(c)
    polygon([(x, y), (x - a / 2, y + h), (x + a / 2, y + h)])


def fir_tree(x=250, y=250, a=50, h=20, step_a=10, step_h=10, n=10, c="green"):
    """Draw fir tree x, y - start point, a - base of starting triangle
    h - heigth of starting triangle, step_a - step of increasing base, 
    step_h step of increasing heigth, n - number of triangles, c - color"""
    for i in range(n):
        triangle(x, y, a, h, c)
        temp_y = y
        y += step_h
        a += step_a
        temp_h = h
        h += step_h / 5
        step_h += step_h / 10
    brushColor("brown")
    rectangle(x - a / 20, temp_y + temp_h, x + a / 20, temp_y + temp_h + 20)


fir_tree(300, 150)
fir_tree(400, 250, 25, 10, 5, 5)
fir_tree(250, 300, 25, 10, 5, 5, c="red")


run()
