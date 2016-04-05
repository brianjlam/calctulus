#!/usr/bin/env python2
from math import sin, cos

PI = 3.1415


#page dimensions (in inches)
page_width = 32
page_height = 18

#necessary beginning syntax (adds page bounds based on above values)
beginningPostscriptSyntax = "%!PS-Adobe-3.0 EPSF-3.0\n%%BoundingBox: 0 0 " \
                             + str(page_width*72) + " " + str(page_height*72) + "\n/Times-Roman findfont\n12 scalefont\nsetfont\n"

#write functions here
def trunk_left(y):
    return -2 + .15 * cos(y) + .5 * cos(.3 * y)
def trunk_right(y):
    return  3 + .15 * sin(y) + .5 * cos(.3 * y)
def width(y):
    return int(72 * (trunk_right(y) - trunk_left(y)))
def altitude(y):
    return int(width(y) / (2 + 2**0.5))
def side(y):
    return int(width(y) - 2 * altitude(y))

def make_coord(y, vertex_num, x_pos, y_pos):

    #dimensions
    w = width(y)
    a = altitude(y)
    s = side(y)

    #specifies how far cutouts are set into the octagon
    corneroffset = int(0.5 * a + 0.5 * s * 6**-0.5)
    sideoffset   = int(0.5 * s * 2 **-0.5)

    coord_list = {0:str(corneroffset  +x_pos) + " " + str(corneroffset  +y_pos),\
                  1:str(a             +x_pos) + " " + str(0             +y_pos),\
                  2:str(w/2           +x_pos) + " " + str(sideoffset    +y_pos),\
                  3:str(a+s           +x_pos) + " " + str(0             +y_pos),\
                  4:str(w-corneroffset+x_pos) + " " + str(corneroffset  +y_pos),\
                  5:str(w             +x_pos) + " " + str(a             +y_pos),\
                  6:str(w-sideoffset  +x_pos) + " " + str(w/2           +y_pos),\
                  7:str(w             +x_pos) + " " + str(a+s           +y_pos),\
                  8:str(w-corneroffset+x_pos) + " " + str(w-corneroffset+y_pos),\
                  9:str(a+s           +x_pos) + " " + str(w             +y_pos),\
                  10:str(w/2          +x_pos) + " " + str(w-sideoffset    +y_pos),\
                  11:str(a            +x_pos) + " " + str(w             +y_pos),\
                  12:str(corneroffset +x_pos) + " " + str(w-corneroffset+y_pos),\
                  13:str(0            +x_pos) + " " + str(a+s           +y_pos),\
                  14:str(sideoffset   +x_pos) + " " + str(w/2           +y_pos),\
                  15:str(0            +x_pos) + " " + str(a             +y_pos)}
    return coord_list[vertex_num]

def make_octagon(y, x_pos, y_pos):
    w = width(y)
    text = "0.1 setlinewidth\n" + str(make_coord(y, 0, x_pos, y_pos)) + " newpath moveto\n"
    for i in range(1, 16):
        text = text + str(make_coord(y, i, x_pos, y_pos)) + " lineto\n"
    text = text + "closepath\n0 setgray\nstroke\n\n"
    #adds a label to the octagon
    text += text + "newpath\n%s %s moveto\n(y=%s) show\n" % (x_pos, y_pos, y)
    return text

"""
dx = board thickness
start = beginning y-value
stop = ending y-value
tilesize = size of largest octagon
"""
def create_ps(dx, start, stop, tilesize):
    y = start
    x_pos = 0
    y_pos = 0
    text = beginningPostscriptSyntax
    while y_pos < 72 * page_height - width(y) and y <= stop:
        while x_pos < 72 * page_width - width(y) and y <= stop:
            text = text + make_octagon(y, x_pos, y_pos)
            y += dx
            x_pos += tilesize * 72
        x_pos = 0
        y_pos += tilesize * 72
    text = text + "showpage"
    return text

print create_ps(0.25, 0, 20, 5.5)




