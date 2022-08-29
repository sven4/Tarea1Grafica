"""Vertices and indices for a variety of simple shapes"""

# A simple class container to store vertices and indices that define a shape
import math
import random


class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n" \
                                                   "indices: " + str(self.indices)


def createAxis(length=1.0):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -length, 0.0, 0.0, 0.0, 0.0, 0.0,
        length, 0.0, 0.0, 1.0, 0.0, 0.0,

        0.0, -length, 0.0, 0.0, 0.0, 0.0,
        0.0, length, 0.0, 0.0, 1.0, 0.0,

        0.0, 0.0, -length, 0.0, 0.0, 0.0,
        0.0, 0.0, length, 0.0, 0.0, 1.0]

    # This shape is meant to be drawn with GL_LINES,
    # i.e. every 2 indices, we have 1 line.
    indices = [
        0, 1,
        2, 3,
        4, 5]

    return Shape(vertices, indices)


def createRainbowCube():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions         colors
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 1.0,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -0.5, -0.5, 0.5, r, g, b,
        0.5, -0.5, 0.5, r, g, b,
        0.5, 0.5, 0.5, r, g, b,
        -0.5, 0.5, 0.5, r, g, b,

        -0.5, -0.5, -0.5, r, g, b,
        0.5, -0.5, -0.5, r, g, b,
        0.5, 0.5, -0.5, r, g, b,
        -0.5, 0.5, -0.5, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def crearEsfera(radio, r, g, b):
    n = 20
    dtheta = math.pi / n
    dphi = 2 * math.pi / n
    vertices = []
    indices = []

    for i in range(n + 1):
        pisoAbajo = i * n
        pisoArriba = (i + 1) * n
        theta = dtheta * i
        for j in range(n + 1):
            phi = dphi * j
            k1 = pisoAbajo + j
            k2 = pisoArriba + j
            vertices += [
                radio * math.cos(phi) * math.sin(theta), radio * math.sin(phi) * math.sin(theta),
                radio * math.cos(theta),
                r, g, b
            ]
            indices += [
                k1, k1 + 1, k2,
                k2, k2 + 1, k1 + 1
            ]

    return Shape(vertices, indices)


def crearEsferaConZonasCaoticas(radio, r, g, b):
    n = 20
    entropia = 20
    dtheta = math.pi / n
    dphi = 2 * math.pi / n
    vertices = []
    indices = []

    for i in range(n + 1):
        pisoAbajo = i * n
        pisoArriba = (i + 1) * n
        theta = dtheta * i
        ran1 = random.randint(-entropia, entropia)
        ran2 = random.randint(-entropia, entropia)
        ran3 = random.randint(-entropia, entropia)
        for j in range(n + 1):
            phi = dphi * j
            k1 = pisoAbajo + j
            k2 = pisoArriba + j
            vertices += [
                radio * math.cos(phi) * math.sin(theta), radio * math.sin(phi) * math.sin(theta),
                radio * math.cos(theta),
                (r * 255 + ran1) / 255, (g * 255 + ran2) / 255, (b * 255 + ran3) / 255
            ]
            indices += [
                k1, k1 + 1, k2,
                k2, k2 + 1, k1 + 1
            ]

    return Shape(vertices, indices)


def crearEsferaConPuntosCaoticos(radio, r, g, b):
    n = 20
    entropia = 10
    dtheta = math.pi / n
    dphi = 2 * math.pi / n
    vertices = []
    indices = []

    for i in range(n + 1):
        pisoAbajo = i * n
        pisoArriba = (i + 1) * n
        theta = dtheta * i
        for j in range(n + 1):
            phi = dphi * j
            k1 = pisoAbajo + j
            k2 = pisoArriba + j
            ran1 = random.randint(-entropia, entropia)
            ran2 = random.randint(-entropia, entropia)
            ran3 = random.randint(-entropia, entropia)
            vertices += [
                radio * math.cos(phi) * math.sin(theta), radio * math.sin(phi) * math.sin(theta),
                radio * math.cos(theta),
                (r * 255 + ran1) / 255, (g * 255 + ran2) / 255, (b * 255 + ran3) / 255
            ]
            indices += [
                k1, k1 + 1, k2,
                k2, k2 + 1, k1 + 1
            ]

    return Shape(vertices, indices)
