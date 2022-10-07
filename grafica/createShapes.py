import grafica.easy_shaders as es
from grafica.readOff import readOFF
from grafica.assets_path import getAssetPath
import grafica.basic_shapes as bs
from OpenGL.GL import GL_STATIC_DRAW, GL_REPEAT, GL_NEAREST


def createGPUShapeStatic(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape


def createOFFShape(pipeline, r, g, b):
    shape = readOFF(getAssetPath('Tri_Fighter.off'), (r, g, b))
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape


def createTextureShape(pipeline, r, g, b):
    shape = bs.createTextureQuad(1.0, 1.0)
    gpuBackground = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBackground)
    gpuBackground.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuBackground.texture = es.textureSimpleSetup(getAssetPath("estrellas.jpg"), GL_REPEAT, GL_REPEAT, GL_NEAREST,
                                                  GL_NEAREST)

    return gpuBackground