import math

import glfw
from OpenGL.GL import *
import numpy as np

import grafica.transformations as tr
import grafica.pipelines as pi
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from grafica.assets_path import getAssetPath
from grafica.camaras import crear_view2, crear_view3
from grafica.readOff import readOFF

# Flags para controlar la view
viewing1 = True
viewing2 = False
viewing3 = False

# Inicializando el array view
view = None


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    global view, viewing1, viewing2, viewing3
    print(action)

    # En cada parte se cambian las camaras, se desactivan las actuales y se activa la que se presiono
    if key == glfw.KEY_1:
        viewing2 = False
        viewing3 = False
        viewing1 = True
    if key == glfw.KEY_2:
        viewing3 = False
        viewing1 = False
        viewing2 = True
    if key == glfw.KEY_3:
        viewing2 = False
        viewing1 = False
        viewing3 = True
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

def main():
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    global view, viewing1, viewing2, viewing3
    width = 800
    height = 600

    window = glfw.create_window(width, height, "Sistema Solar", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline2 = es.SimpleTextureShaderProgram()
    pipelineReadOff = pi.SimpleFlatShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Convenience function to ease initialization
    def createGPUShapeStatic(shape):
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
    # Creating shapes on GPU memory
    gpuAxis = createGPUShapeStatic(bs.createAxis(7))

    # Codigo para hacer las estrellas
    shapeBackground = bs.createTextureQuad(1.0, 1.0)
    gpuBackground = es.GPUShape().initBuffers()
    pipeline2.setupVAO(gpuBackground)
    gpuBackground.fillBuffers(shapeBackground.vertices, shapeBackground.indices, GL_STATIC_DRAW)

    gpuBackground.texture = es.textureSimpleSetup(getAssetPath("estrellas.jpg"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    # Variables para asignar los colores del sol de manera dinamica
    rsol = 255
    gsol = 100
    bsol = 0

    # Aqui se crean las figuras planetarias
    gpuSol = createGPUShapeStatic(bs.crearEsferaConPuntosCaoticos(2, rsol/255, gsol / 255, bsol/255))  # Valor real 7

    gpuMercurio = createGPUShapeStatic(bs.crearEsferaConPuntosCaoticos(0.12, 1, 180 / 255, 0))  # Valor real 0.03
    gpuVenus = createGPUShapeStatic(bs.crearEsferaConZonasCaoticas(0.24, 1, 120 / 255, 0))  # Valor real 0.06
    gpuTierra = createGPUShapeStatic(bs.crearEsfera(0.252, 0, 170 / 255, 0))  # Valor real 0.063
    gpuLumbre = createGPUShapeStatic(bs.crearEsfera(0.252, 218/255, 247 / 255, 166/255))  # Planeta estatico para practicar las camaras
    gpuLuna = createGPUShapeStatic(bs.crearEsfera(0.084, 100/255, 100/255, 100/255))
    gpuMarte = createGPUShapeStatic(bs.crearEsfera(0.132, 1, 0, 0))
    gpuJupiter = createGPUShapeStatic(bs.crearEsferaConZonasCaoticas(0.8, 241 / 255, 173 / 255, 101 / 255))  # Valor real: 1.4
    gpuSaturno = createGPUShapeStatic(bs.crearEsferaConZonasCaoticas(0.7, 170/255, 170 / 255, 170 / 255))  # Valor real: 1.1
    gpuAnilloSaturnoA = createGPUShapeStatic(bs.crearAnillo(1.2, 1.15, 100 / 255, 100/255, 101/255))
    gpuAnilloSaturnoB = createGPUShapeStatic(bs.crearAnillo(1.15, 1.1, 1, 1, 1))
    gpuAnilloSaturnoC = createGPUShapeStatic(bs.crearAnillo(1.1, 1.05, 50/255, 50/255, 50/255))
    gpuAnilloSaturnoD = createGPUShapeStatic(bs.crearAnillo(1.05, 1, 0, 0, 0))
    gpuAnilloSaturnoE = createGPUShapeStatic(bs.crearAnillo(1, 0.9, 100/ 255, 100/255, 100/255))
    gpuUrano = createGPUShapeStatic(bs.crearEsferaConZonasCaoticas(0.3, 0, 1, 200 / 255))  # Valor real: 0.5
    gpuNeptuno = createGPUShapeStatic(bs.crearEsferaConZonasCaoticas(0.29, 0, 0, 1))  # Valor real: 0.49
    gpuAnilloNeptuno1 = createGPUShapeStatic(bs.crearAnillo(0.4, 0.395, 0, 200/255, 140/255))

    gpuNave1 = createOFFShape(pipelineReadOff, 250/255, 30/255, 60/255)

    # Aqui se crea la view1
    cam_radius = 10
    viewCam = np.array([cam_radius, cam_radius, cam_radius])

    view1 = tr.lookAt(viewCam, np.array([0, 0, 0]), np.array([0, 0, 1]))

    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    view = view1
    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Aqui dependiendo del flag activo actual se crea una u otra view
        if viewing1:
            view = view1
        elif viewing2:
            view = tr.lookAt(crear_view2(t1), np.array([0, 0, 0]), np.array([0, 0, 1]))
        elif viewing3:
            view = tr.lookAt(crear_view3(t1), np.array([0, 0, 0]), np.array([0, 0, 1]))
        else: # En caso de algun error, view se queda fija
            view = view1

        glUseProgram(pipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Antes de los 44 segundos el sol se agrande y luego se contrae, esto se logra gracias a la funcion coseno
        if t1 < 44:
            matriz_sol = tr.matmul([tr.rotationZ(t1 * 0.5), tr.uniformScale(1 + 0.5*t1*math.cos(math.pi*t1/44)/44)])
        else: # Cuando se llega a los 44 el sol se mantiene constante
            matriz_sol = tr.matmul([tr.rotationZ(t1 * 0.5), tr.uniformScale(0.5)])

        # Se crean las matrices de movimiento de los demas planetas
        matriz_mercurio = tr.matmul([tr.rotationY(5), tr.rotationZ(2*t1), tr.translate(2 + 0.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_venus = tr.matmul([tr.rotationY(6), tr.rotationZ(1.5*t1), tr.translate(2 + 1, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_tierra = tr.matmul([tr.rotationZ(1.25*t1), tr.translate(2 + 1.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_luna = tr.matmul(([tr.rotationZ(1.25*t1), tr.translate(2 + 1.5, 0, 0), tr.rotationZ(1.5*t1), tr.translate(0.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)]))
        matriz_marte = tr.matmul([tr.rotationX(3), tr.rotationZ(1.05*t1), tr.translate(2 + 2, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_jupiter = tr.matmul([tr.rotationX(math.pi/4), tr.rotationZ(t1/3), tr.translate(4 + 2.5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_saturno = tr.matmul([tr.rotationY(4), tr.rotationZ(t1/4), tr.translate(4 + 4, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_anillo_saturno1 = tr.matmul([tr.rotationY(4), tr.rotationZ(t1/4), tr.translate(4 + 4, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_urano = tr.matmul([tr.rotationY(5), tr.rotationZ(t1/5), tr.translate(4 + 5, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])
        matriz_neptuno = tr.matmul([tr.rotationX(20), tr.rotationZ(t1/8), tr.translate(4 + 6, 0, 0), tr.rotationX(0.5), tr.rotationY(0.1*t1)])

        matriz_nave1 = tr.matmul([tr.rotationY(20), tr.translate(3, 3, 3)])

        # En esta parte se maneja el color
        if t1 < 40:  # Antes de los 40 segundos el color rojo se va incrementando
            gsol = 100 - 100*t1/40
        elif rsol != 0 and gsol < 220 and bsol < 220 and t1 >= 40:
            rsol -= 255*dt/5
            gsol += 220*dt/5
            bsol += 220*dt/5
        else:
            rsol = 0
            gsol = 220
            bsol = 220

        # En esta parte se cambian los colores del sol al iniciar la supernova sin la necesidad de redibujarlo, no es buen diseño considerando
        # la forma en la que se cambiaron los colores del sol antes
        if t1 < 44:
            vertices_sol = bs.crearVerticesEsfera(2, 50, rsol/255, gsol/255, bsol/255)
            vertex_data_sol = np.array(vertices_sol, dtype=np.float32)
            glBindBuffer(GL_ARRAY_BUFFER, gpuSol.vbo)
            glBufferData(GL_ARRAY_BUFFER, len(vertex_data_sol) * 4, vertex_data_sol, GL_STREAM_DRAW)
        else:  # Despues de empezar la supernova se aumenta el tamaño del sol hasta que explociona el sistema solar
            matriz_sol = tr.matmul([matriz_sol, tr.uniformScale(t1 - 44)])
        glUseProgram(pipeline2.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipeline2.shaderProgram, "transform"), 1, GL_TRUE, tr.uniformScale(10))
        pipeline2.drawCall(gpuBackground)

        glUseProgram(pipeline.shaderProgram)
        if t1 < 60: # Esta es una manera de desaparecer los planetas despues de que el sol entra en supernova
            # Es una solucion parche no muy elegante pero funciona

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_mercurio)
            pipeline.drawCall(gpuMercurio)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_venus)
            pipeline.drawCall(gpuVenus)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_tierra)
            pipeline.drawCall(gpuTierra)

            # glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.translate(5.5, 1, 1))
            # pipeline.drawCall(gpuLumbre) # Esto es un objeto estatico para probar la camara en movmiento

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_luna)
            pipeline.drawCall(gpuLuna)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_marte)
            pipeline.drawCall(gpuMarte)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_jupiter)
            pipeline.drawCall(gpuJupiter)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_saturno)
            pipeline.drawCall(gpuSaturno)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
            pipeline.drawCall(gpuAnilloSaturnoA)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
            pipeline.drawCall(gpuAnilloSaturnoB)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
            pipeline.drawCall(gpuAnilloSaturnoC)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
            pipeline.drawCall(gpuAnilloSaturnoD)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
            pipeline.drawCall(gpuAnilloSaturnoE)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_urano)
            pipeline.drawCall(gpuUrano)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_neptuno)
            pipeline.drawCall(gpuNeptuno)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_neptuno)
            pipeline.drawCall(gpuAnilloNeptuno1)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_sol)
            pipeline.drawCall(gpuSol)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_nave1)
            pipeline.drawCall(gpuNave1)


        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        pipeline.drawCall(gpuAxis, GL_LINES)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.

        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    gpuBackground.clear()
    gpuMercurio.clear()
    gpuVenus.clear()
    gpuTierra.clear()
    gpuLuna.clear()
    gpuMarte.clear()
    gpuJupiter.clear()
    gpuSaturno.clear()
    gpuAnilloSaturnoA.clear()
    gpuAnilloSaturnoB.clear()
    gpuAnilloSaturnoC.clear()
    gpuAnilloSaturnoD.clear()
    gpuAnilloSaturnoE.clear()
    gpuUrano.clear()
    gpuNeptuno.clear()
    gpuAnilloNeptuno1.clear()
    gpuSol.clear()

    glfw.terminate()


if __name__ == "__main__":
    main()
