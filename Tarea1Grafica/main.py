# coding=utf-8
"""Actividad 2"""
import math

import glfw
from OpenGL.GL import (glUseProgram, glClearColor, glEnable, GL_DEPTH_TEST,
                       GL_STATIC_DRAW, glUniformMatrix4fv, glGetUniformLocation,
                       GL_TRUE, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       glPolygonMode, GL_FRONT_AND_BACK, GL_FILL, GL_LINES)
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


def main():
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Projections Demo", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Convenience function to ease initialization
    def createGPUShape(shape):
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        return gpuShape

    # Creating shapes on GPU memory
    gpuAxis = createGPUShape(bs.createAxis(7))

    gpuSol = createGPUShape(bs.crearEsferaConPuntosCaoticos(2, 1, 50 / 255, 0))  # Valor real 7

    gpuMercurio = createGPUShape(bs.crearEsferaConPuntosCaoticos(0.12, 1, 180 / 255, 0))  # Valor real 0.03
    gpuVenus = createGPUShape(bs.crearEsferaConZonasCaoticas(0.24, 1, 120 / 255, 0))  # Valor real 0.06
    gpuTierra = createGPUShape(bs.crearEsfera(0.252, 0, 170 / 255, 0))  # Valor real 0.063
    gpuLuna = createGPUShape(bs.crearEsfera(0.084, 100/255, 100/255, 100/255))
    gpuMarte = createGPUShape(bs.crearEsfera(0.132, 1, 0, 0))
    gpuJupiter = createGPUShape(bs.crearEsferaConZonasCaoticas(0.8, 241 / 255, 173 / 255, 101 / 255))  # Valor real: 1.4
    gpuSaturno = createGPUShape(bs.crearEsferaConZonasCaoticas(0.7, 1, 191 / 255, 94 / 255))  # Valor real: 1.1
    gpuAnilloSaturno = createGPUShape(bs.crearCircunferencia(1, 192 / 255, 150/255, 101/255))
    gpuUrano = createGPUShape(bs.crearEsferaConZonasCaoticas(0.3, 0, 1, 200 / 255))  # Valor real: 0.5
    gpuNeptuno = createGPUShape(bs.crearEsferaConZonasCaoticas(0.29, 0, 0, 1))  # Valor real: 0.49

    camera_theta = np.pi / 4

    # Setting up the view transform

    cam_radius = 14
    cam_x = cam_radius * np.sin(camera_theta)
    cam_y = cam_radius * np.cos(camera_theta)
    cam_z = cam_radius

    viewPos = np.array([cam_x, cam_y, cam_z])

    view = tr.lookAt(viewPos, np.array([0, 0, 0]), np.array([0, 0, 1]))

    # Setting up the projection transform

    # projection = tr.ortho(-8, 8, -8, 8, 0.1, 100)
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    ##### UN CONTADOR QUE NOS ASISTIRA EN LAS TRANSFORMACIONES #####
    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        ##### CALCULAMOS EL DELTA DEL TIEMPO #####

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        ##### ENTRAREMOS EN MAS DETALLE SOBRE VIEW Y PROJECTION EN EL FUTURO #####

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        matrizSol = tr.matmul([tr.rotationZ(t1 * 0.5)])

        matriz_mercurio = tr.matmul([tr.rotationZ(2*t1), tr.translate(2 + 0.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_venus = tr.matmul([tr.rotationZ(1.5*t1), tr.translate(2 + 1, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_tierra = tr.matmul([tr.rotationZ(1.25*t1), tr.translate(2 + 1.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_luna = tr.matmul(([tr.rotationZ(1.25*t1), tr.translate(2+1.5, 0, 0), tr.rotationZ(1.5*t1), tr.translate(0.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)]))
        matriz_marte = tr.matmul([tr.rotationZ(1.05*t1), tr.translate(2 + 2, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_jupiter = tr.matmul([tr.rotationZ(t1/3), tr.translate(4 + 2.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_saturno = tr.matmul([tr.rotationZ(t1/4), tr.translate(4 + 4, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_anillo_saturno = tr.matmul([tr.rotationZ(t1/4), tr.translate(4 + 4, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_urano = tr.matmul([tr.rotationZ(t1/5), tr.translate(4 + 5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_neptuno = tr.matmul([tr.rotationZ(t1/8), tr.translate(4 + 6, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])

        # matrizSol = tr.translate(0, 4*math.sin(t1), 0)
        # matrizSol = tr.translate(4*math.sin(t1), 0 , 0)
        # matrizSol = tr.translate(0, 0, 4 * math.sin(t1))

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_mercurio)
        pipeline.drawCall(gpuMercurio)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_venus)
        pipeline.drawCall(gpuVenus)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_tierra)
        pipeline.drawCall(gpuTierra)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_luna)
        pipeline.drawCall(gpuLuna)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_marte)
        pipeline.drawCall(gpuMarte)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_jupiter)
        pipeline.drawCall(gpuJupiter)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_saturno)
        pipeline.drawCall(gpuSaturno)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno)
        pipeline.drawCall(gpuAnilloSaturno)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_urano)
        pipeline.drawCall(gpuUrano)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_neptuno)
        pipeline.drawCall(gpuNeptuno)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matrizSol)
        pipeline.drawCall(gpuSol)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        pipeline.drawCall(gpuAxis, GL_LINES)

        ##### NO ES NECESARIO QUE MODIFIQUEN NADA DESPUES DE ESTE PUNTO #####

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    gpuMercurio.clear()
    gpuVenus.clear()
    gpuTierra.clear()
    gpuMarte.clear()
    gpuJupiter.clear()
    gpuSaturno.clear()
    gpuUrano.clear()
    gpuNeptuno.clear()
    gpuSol.clear()

    glfw.terminate()


if __name__ == "__main__":
    main()
