import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import serial
from serial import *


# initialize serial port
ser = serial.Serial(port="COM5", baudrate=9600, bytesize=EIGHTBITS,
                    parity=PARITY_NONE, stopbits=STOPBITS_ONE,
                    timeout=1, xonxoff=False, rtscts=False,
                    write_timeout=None, dsrdtr=False,
                    inter_byte_timeout=None, exclusive=None)

# fetch a description of all port attributes
description  = ("Port description:\n" +
                "port: {}\n".format(ser.port) +
                "status: {}\n".format("port open" if ser.is_open else "port closed") +
                "baudrate: {}\n".format(ser.baudrate) +
                "bytesize: {}\n".format(ser.bytesize) +
                "parity: {}\n".format(ser.parity) +
                "stopbits: {}\n".format(ser.stopbits) +
                "timeout: {}\n".format(ser.timeout) +
                "xonxoff: {}\n".format(ser.xonxoff) +
                "rtscts: {}\n".format(ser.rtscts) +
                "write_timeout: {}\n".format(ser.write_timeout) +
                "dsrdtr: {}\n".format(ser.dsrdtr) +
                "inter_byte_timeout: {}\n".format(ser.inter_byte_timeout) +
                "exclusive: {}\n".format(ser.exclusive))

print(description)

# define the verticies of the obect
verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
)

# define which verticies are needed to be connected
# in order to draw a line (= edge of cube)
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 6),
    (4, 7),
    (6, 5),
    (6, 7),
    (5, 1),
    (5, 4),
    (7, 3),
)

# define which verticies make a surface
surfaces = (
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (7, 3, 0, 4),
    (4, 5, 6, 7),
    (0, 3, 2, 1),
)

# define a color for each vertex
colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (0, 1, 0),
)


# making a colored cube with white edges
def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(colors[vertex])
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        glColor3fv((1, 1, 1))
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


# if one wants to travel with different valocities depending on the
# joy stick value of coordinate x or y (both between -600 and 600)
#
# experience shows that: -1 < valocities < +1 is a practical range
# negative x coords --> travel left; pos. --> right
# negative y coords --> travel down; pos. --> up
def speed(val=0.0):
    # for -4 <= values <= +4 we want to have 0 speed
    # that's because we sometimes return joystick to neutral position
    # and we get a small value between -4 and +4
    if (val * val) <= 16:
        val = 0.0
    max_val = 600.0
    return(val / max_val)

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslate(0, 0, -20)

    glRotatef(25, 2, 1, 0)

    # save x, y values is needed for the speed in x and y direction because
    # we will only get input from joystick control software
    # when there is a change on the joystick, but here we want to
    # travel with a fixed valocity when there is no joystick motion
    x = 0
    y = 0

    while True:
        # check for available serial input
        if ser.in_waiting != 0:
            # read from serial buffer
            msg = ser.readline().decode("utf-8")
            # the massages from the arduino are comming formated like:
            # x=somevalue\r\n
            # or
            # y=somevalue\r\n
            if "x" in msg:
                x = int(msg[2:-2])
                print("x:", x)  # for debuging purpose
                glTranslate(speed(x), 0, 0)
            if "y" in msg:
                y = int(msg[2:-2])
                print("y:", y)  # for debuging purpose
                glTranslate(0, speed(y), 0)
        # here we keep traveling with previous speed when there is no
        # change in the joystick position
        else:
            glTranslate(speed(x), speed(y), 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslate(-1, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslate(1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glTranslate(0, -1, 0)
                if event.key == pygame.K_UP:
                    glTranslate(0, 1, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslate(0, 0, 1)
                if event.button == 5:
                    glTranslate(0, 0, -1)


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()

ser.close()
print("Port is {}".format("still open" if ser.is_open else "closed"))
