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


def createColorNormalsCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions         colors   normals
        # Z+
        -0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, 0.5, 0.5, r, g, b, 0, 0, 1,
        -0.5, 0.5, 0.5, r, g, b, 0, 0, 1,

        # Z-
        -0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, 0.5, -0.5, r, g, b, 0, 0, -1,
        -0.5, 0.5, -0.5, r, g, b, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, 0.5, r, g, b, 1, 0, 0,
        0.5, -0.5, 0.5, r, g, b, 1, 0, 0,

        # X-
        -0.5, -0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, 0.5, r, g, b, -1, 0, 0,
        -0.5, -0.5, 0.5, r, g, b, -1, 0, 0,

        # Y+
        -0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, 0.5, r, g, b, 0, 1, 0,
        -0.5, 0.5, 0.5, r, g, b, 0, 1, 0,

        # Y-
        -0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, 0.5, r, g, b, 0, -1, 0,
        -0.5, -0.5, 0.5, r, g, b, 0, -1, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)


def crearCircunferencia(radio, r, g, b):
    n = 50
    dtheta = 2 * math.pi / n
    indices = []
    vertices = [0, 0, 0, r, g, b]

    for i in range(n):
        theta = dtheta * i
        vertices += [radio * math.cos(theta), radio*math.sin(theta), 0,
                    r, g, b]
        indices += [0, i, i+1]

    return Shape(vertices, indices)


def crearAnillo(radio,radioInterior, r, g, b):
    n = 50
    dtheta = 2 * math.pi / n
    indices = []
    vertices = []

    for i in range(n+1):
        theta = dtheta * i
        vertices += [radio * math.cos(theta), radio*math.sin(theta), 0,
                     r, g, b,
                     0, 0, 1]
        vertices += [radioInterior * math.cos(theta), radioInterior*math.sin(theta), 0,
                     r, g, b,
                     0, 0, 1]

        indices += [i, i+1, i+2]
        indices += [n+i, n+i+1, n+i+2]
    return Shape(vertices, indices)


def crearVerticesEsfera(radio, n, r, g, b, entropia):
    dtheta = math.pi / n
    dphi = 2 * math.pi / n
    vertices = []
    for i in range(n+1):
        theta = dtheta * i
        for j in range(n+1):
            ran1 = random.randint(-entropia, entropia)
            ran2 = random.randint(-entropia, entropia)
            ran3 = random.randint(-entropia, entropia)
            phi = dphi * j
            vertices += [
                radio * math.cos(phi) * math.sin(theta), radio * math.sin(phi) * math.sin(theta),
                radio * math.cos(theta),
                (r * 255 + ran1) / 255, (g * 255 + ran2) / 255, (b * 255 + ran3) / 255,
                math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)
            ]
    return vertices


def crearIndicesEsfera(n):
    indices = []
    for i in range(n+1):
        pisoAbajo = i * n
        pisoArriba = (i + 1) * n
        for j in range(n+1):
            k1 = pisoAbajo + j
            k2 = pisoArriba + j
            indices += [
                k1, k1 + 1, k2,
                k2, k2 + 1, k1 + 1
            ]
    return indices


def crearEsfera(radio, r, g, b, entropia):
    n = 50
    vertices = crearVerticesEsfera(radio, n, r, g, b, entropia)
    indices = crearIndicesEsfera(n)

    return Shape(vertices, indices)


def createTextureQuad(nx, ny):

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
    #   positions        texture
        -0.5*2, -0.5*2, 0.0,  0, ny,
         0.5*2, -0.5*2, 0.0, nx, ny,
         0.5*2,  0.5*2, 0.0, nx, 0,
        -0.5*2,  0.5*2, 0.0,  0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)

def crearEsferaConZonasCaoticas(radio, r, g, b):
    n = 50
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
                (r * 255 + ran1) / 255, (g * 255 + ran2) / 255, (b * 255 + ran3) / 255,
                math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)
            ]
            indices += [
                k1, k1 + 1, k2,
                k2, k2 + 1, k1 + 1
            ]

    return Shape(vertices, indices)


def crearEsferaConPuntosCaoticos(radio, r, g, b):
    n = 50
    entropia = 5
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
                (r * 255 + ran1) / 255, (g * 255 + ran2) / 255, (b * 255 + ran3) / 255,
                math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)
            ]
            indices += [
                k1, k1 + 1, k2,
                k2, k2 + 1, k1 + 1
            ]

    return Shape(vertices, indices)
