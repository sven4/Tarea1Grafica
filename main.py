import math

import glfw
from OpenGL.GL import *
import numpy as np

import grafica.transformations as tr
import grafica.pipelines as pi
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from grafica import curvas
from grafica.assets_path import getAssetPath
from grafica.camaras import crear_view2, crear_view3
from grafica.createShapes import createGPUShapeStatic, createOFFShape

# Flags para controlar la view
viewing1 = True
viewing2 = False
viewing3 = False

# Inicializando el array view
view = None


class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.X = 3.0
        self.Y = 3.0
        self.Z = 2.0
        self.pitch = np.pi/2
        self.yaw = 0.0
        self.turbo = False


controller = Controller()
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    global view, viewing1, viewing2, viewing3, viewing4
    print(action)

    # En cada parte se cambian las camaras, se desactivan las actuales y se activa la que se presiono
    if key == glfw.KEY_1:
        viewing2 = False
        viewing3 = False
        viewing4 = False
        viewing1 = True
    if key == glfw.KEY_2:
        viewing3 = False
        viewing1 = False
        viewing4 = False
        viewing2 = True
    if key == glfw.KEY_3:
        viewing2 = False
        viewing1 = False
        viewing4 = False
        viewing3 = True
    if key == glfw.KEY_4:
        viewing2 = False
        viewing1 = False
        viewing3 = False
        viewing4 = True

    if key == glfw.KEY_TAB:
        controller.fillPolygon = not controller.fillPolygon

    if key == glfw.KEY_F:
        controller.turbo = not controller.turbo

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

def main():
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    global view, viewing1, viewing2, viewing3, viewing4, controller
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
    pipelineTexture = es.SimpleTextureShaderProgram()
    pipelineReadOff = pi.SimpleFlatShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = createGPUShapeStatic(pipeline, bs.createAxis(7))

    # Codigo para hacer las estrellas
    shapeBackground = bs.createTextureQuad(1.0, 1.0)
    gpuBackground = es.GPUShape().initBuffers()
    pipelineTexture.setupVAO(gpuBackground)
    gpuBackground.fillBuffers(shapeBackground.vertices, shapeBackground.indices, GL_STATIC_DRAW)

    gpuBackground.texture = es.textureSimpleSetup(getAssetPath("estrellas.jpg"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    # Variables para asignar los colores del sol de manera dinamica
    rsol = 255
    gsol = 100
    bsol = 0

    # Aqui se crean las figuras planetarias
    gpuSol = createGPUShapeStatic(pipeline, bs.crearEsferaConPuntosCaoticos(2, rsol/255, gsol / 255, bsol/255))  # Valor real 7

    gpuMercurio = createGPUShapeStatic(pipeline, bs.crearEsferaConPuntosCaoticos(0.12, 1, 180 / 255, 0))  # Valor real 0.03
    gpuVenus = createGPUShapeStatic(pipeline, bs.crearEsferaConZonasCaoticas(0.24, 1, 120 / 255, 0))  # Valor real 0.06
    gpuTierra = createGPUShapeStatic(pipeline, bs.crearEsfera(0.252, 0, 170 / 255, 0))  # Valor real 0.063
    gpuLumbre = createGPUShapeStatic(pipeline, bs.crearEsfera(0.252, 218/255, 247 / 255, 166/255))  # Planeta estatico para practicar las camaras
    gpuLuna = createGPUShapeStatic(pipeline, bs.crearEsfera(0.084, 100/255, 100/255, 100/255))
    gpuMarte = createGPUShapeStatic(pipeline, bs.crearEsfera(0.132, 1, 0, 0))
    gpuJupiter = createGPUShapeStatic(pipeline, bs.crearEsferaConZonasCaoticas(0.8, 241 / 255, 173 / 255, 101 / 255))  # Valor real: 1.4
    gpuSaturno = createGPUShapeStatic(pipeline, bs.crearEsferaConZonasCaoticas(0.7, 170/255, 170 / 255, 170 / 255))  # Valor real: 1.1
    gpuAnilloSaturnoA = createGPUShapeStatic(pipeline, bs.crearAnillo(1.2, 1.15, 100 / 255, 100/255, 101/255))
    gpuAnilloSaturnoB = createGPUShapeStatic(pipeline, bs.crearAnillo(1.15, 1.1, 1, 1, 1))
    gpuAnilloSaturnoC = createGPUShapeStatic(pipeline, bs.crearAnillo(1.1, 1.05, 50/255, 50/255, 50/255))
    gpuAnilloSaturnoD = createGPUShapeStatic(pipeline, bs.crearAnillo(1.05, 1, 0, 0, 0))
    gpuAnilloSaturnoE = createGPUShapeStatic(pipeline, bs.crearAnillo(1, 0.9, 100/ 255, 100/255, 100/255))
    gpuUrano = createGPUShapeStatic(pipeline, bs.crearEsferaConZonasCaoticas(0.3, 0, 1, 200 / 255))  # Valor real: 0.5
    gpuNeptuno = createGPUShapeStatic(pipeline, bs.crearEsferaConZonasCaoticas(0.29, 0, 0, 1))  # Valor real: 0.49
    gpuAnilloNeptuno1 = createGPUShapeStatic(pipeline, bs.crearAnillo(0.4, 0.395, 0, 200/255, 140/255))

    gpuNave1 = createOFFShape(pipelineReadOff, 120/255, 20/255, 20/255)
    gpuNave2 = createOFFShape(pipelineReadOff, 20/255, 20/255, 120/255)
    gpuNave3 = createOFFShape(pipelineReadOff, 120/255, 120/255, 0/255)
    gpuNave4 = createOFFShape(pipelineReadOff, 0/255, 120/255, 120/255)
    gpuNave5 = createOFFShape(pipelineReadOff, 180/255, 180/255, 180/255)
    tamanhoNaves = 0.18
    velocidadNave = 1

    # Aqui se crea la view1
    cam_radius = 10
    viewCam = np.array([cam_radius, cam_radius, cam_radius])

    view1 = tr.lookAt(viewCam, np.array([0, 0, 0]), np.array([0, 0, 1]))

    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    view = view1
    t0 = glfw.get_time()
    N = 250
    C1 = curvas.generarCurvaCerradaNave1(N, 5, 0)
    C2 = curvas.generarCurvaCerradaNave2(N, 3, 5)
    C3 = curvas.generarCurvaCerradaNave1(N, 7, -4)
    C4 = curvas.generarCurvaCerradaNave2(N, 10, 0)
    step = 0

    tiempoLimite = 222
    while not glfw.window_should_close(window):
        glfw.poll_events()
        # processCamera()

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Aqui dependiendo del flag activo actual se crea una u otra view
        if viewing1:
            view = view1
        elif viewing2:
            view = tr.lookAt(crear_view2(t1), np.array([0,0,0]), np.array([0, 0, 1]))
        elif viewing3:
            view = tr.lookAt(crear_view3(t1, 13), crear_view3(t1, 12), np.array([0,0,1]))
        elif viewing4:
            Xesf = tamanhoNaves * 4 * np.sin(controller.pitch) * np.cos(controller.yaw)  # coordenada X esferica
            Yesf = tamanhoNaves * 4 * np.sin(controller.pitch) * np.sin(controller.yaw)  # coordenada Y esferica
            Zesf = tamanhoNaves * 4 * np.cos(controller.pitch)
            viewPos = np.array([
                controller.X - Xesf,
                controller.Y - Yesf,
                controller.Z - Zesf
            ])
            view = tr.lookAt(
                viewPos,
                np.array([controller.X, controller.Y, controller.Z]),
                np.array([0, 0, 1]))
        else:  # En caso de algun error, view se queda fija
            view = view1

        if controller.turbo:
            velocidadNave = 3
        else:
            velocidadNave = 1

        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            controller.X += velocidadNave * dt * np.cos(controller.yaw)
            controller.Y += velocidadNave * dt * np.sin(controller.yaw)

        if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            controller.X -= velocidadNave * dt * np.cos(controller.yaw)
            controller.Y -= velocidadNave * dt * np.sin(controller.yaw)

        if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
            controller.yaw += dt * 1.5

        if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
            controller.yaw -= dt * 1.5

        if (glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS):
            controller.Z += velocidadNave * dt
        if (glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
                or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS):
            controller.Z -= velocidadNave * dt
        glUseProgram(pipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if step > N*2 - 3:
            step = 0

        if step < N*2 - 3:
            angle = np.arctan2(C1[step + 1, 1] - C1[step, 1], C1[step + 1, 0] - C1[step, 0])
        else:
            angle = np.arctan2(C1[0, 1] - C1[step, 1], C1[0, 0] - C1[step, 0])


        # Antes de los 44 segundos el sol se agrande y luego se contrae, esto se logra gracias a la funcion coseno
        if t1 < tiempoLimite:
            matriz_sol = tr.matmul([tr.rotationZ(t1 * 0.5), tr.uniformScale(1 + 0.5*t1*math.cos(math.pi*t1/(tiempoLimite+2))/(tiempoLimite+2))])
        else: # Cuando se llega a los 44 el sol se mantiene constante
            matriz_sol = tr.matmul([tr.rotationZ(t1 * 0.5), tr.uniformScale(0.5)])

        # Se crean las matrices de movimiento de los demas planetas
        matriz_mercurio = tr.matmul(
            [tr.rotationY(5),
             tr.rotationZ(2*t1),
             tr.translate(2 + 0.5, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_venus = tr.matmul(
            [tr.rotationY(6),
             tr.rotationZ(1.5*t1),
             tr.translate(2 + 1, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_tierra = tr.matmul(
            [tr.rotationZ(1.25*t1),
             tr.translate(2 + 1.5, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_luna = tr.matmul((
            [tr.rotationZ(1.25*t1),
             tr.translate(2 + 1.5, 0, 0),
             tr.rotationZ(1.5*t1),
             tr.translate(0.5, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)]))
        matriz_marte = tr.matmul(
            [tr.rotationX(3),
             tr.rotationZ(1.05*t1),
             tr.translate(2 + 2, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_jupiter = tr.matmul(
            [tr.rotationX(math.pi/4),
             tr.rotationZ(t1/3),
             tr.translate(4 + 2.5, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_saturno = tr.matmul(
            [tr.rotationY(4),
             tr.rotationZ(t1/4),
             tr.translate(4 + 4, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_anillo_saturno1 = tr.matmul(
            [tr.rotationY(4),
             tr.rotationZ(t1/4),
             tr.translate(4 + 4, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_urano = tr.matmul(
            [tr.rotationY(5),
             tr.rotationZ(t1/5),
             tr.translate(4 + 5, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])
        matriz_neptuno = tr.matmul(
            [tr.rotationX(20),
             tr.rotationZ(t1/8),
             tr.translate(4 + 6, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*t1)])

        matriz_nave1 = tr.matmul(
            [tr.translate(C1[step, 0], C1[step, 1], C1[step, 2]),
             tr.rotationZ(angle),
             tr.rotationY(math.pi/2),
             tr.uniformScale(tamanhoNaves)])
        matriz_nave2 = tr.matmul(
            [tr.translate(C2[step, 0], C2[step, 1], C2[step, 2]),
             tr.rotationZ(-angle),
             tr.rotationY(math.pi/2),
             tr.uniformScale(tamanhoNaves)])
        matriz_nave3 = tr.matmul(
            [tr.translate(C3[step, 0], C3[step, 1], C3[step, 2]),
             tr.rotationZ(angle),
             tr.rotationY(math.pi/2),
             tr.uniformScale(tamanhoNaves)])
        matriz_nave4 = tr.matmul(
            [tr.translate(C4[step, 0], C4[step, 1], C4[step, 2]),
             tr.rotationZ(-angle),
             tr.rotationY(math.pi/2),
             tr.uniformScale(tamanhoNaves)])
        matriz_nave5 = tr.matmul([
            tr.translate(controller.X, controller.Y, controller.Z),
            tr.rotationZ(controller.yaw),
            tr.rotationY(math.pi/2),
            tr.uniformScale(tamanhoNaves)])

        step = step + 1

        # En esta parte se maneja el color
        if t1 < tiempoLimite:  # Antes de los tiempoLimite segundos el color rojo se va incrementando
            gsol = 100 - 100*t1/tiempoLimite
        elif rsol != 0 and gsol < 220 and bsol < 220 and t1 >= tiempoLimite:
            rsol -= 255*dt*8/tiempoLimite
            gsol += 220*dt*8/tiempoLimite
            bsol += 220*dt*8/tiempoLimite
        else:
            rsol = 0
            gsol = 220
            bsol = 220

        # En esta parte se cambian los colores del sol al iniciar la supernova sin la necesidad de redibujarlo, no es buen diseño considerando
        # la forma en la que se cambiaron los colores del sol antes
        if t1 < tiempoLimite + 5:
            vertices_sol = bs.crearVerticesEsfera(2, 50, rsol/255, gsol/255, bsol/255)
            vertex_data_sol = np.array(vertices_sol, dtype=np.float32)
            glBindBuffer(GL_ARRAY_BUFFER, gpuSol.vbo)
            glBufferData(GL_ARRAY_BUFFER, len(vertex_data_sol) * 4, vertex_data_sol, GL_STREAM_DRAW)
        else:  # Despues de empezar la supernova se aumenta el tamaño del sol hasta que explociona el sistema solar
            matriz_sol = tr.matmul([matriz_sol, tr.uniformScale(t1 - tiempoLimite - 4)])
        glUseProgram(pipelineTexture.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipelineTexture.shaderProgram, "transform"), 1, GL_TRUE, tr.uniformScale(10))
        pipelineTexture.drawCall(gpuBackground)

        glUseProgram(pipeline.shaderProgram)
        if t1 < tiempoLimite + 20: # Esta es una manera de desaparecer los planetas despues de que el sol entra en supernova
            # Es una solucion parche no muy elegante pero funciona

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_mercurio)
            pipeline.drawCall(gpuMercurio)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_venus)
            pipeline.drawCall(gpuVenus)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_tierra)
            pipeline.drawCall(gpuTierra)

            # glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.translate(5.5, 1, 1))
            # pipeline.drawCall(gpuLumbre) # Esto es un objeto estatico para probar la camara en movimiento

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

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_nave2)
            pipeline.drawCall(gpuNave2)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_nave3)
            pipeline.drawCall(gpuNave3)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_nave4)
            pipeline.drawCall(gpuNave4)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, matriz_nave5)
            pipeline.drawCall(gpuNave5)


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
    gpuNave1.clear()
    gpuNave2.clear()
    gpuNave3.clear()
    gpuNave4.clear()
    gpuNave5.clear()

    glfw.terminate()


if __name__ == "__main__":
    main()
