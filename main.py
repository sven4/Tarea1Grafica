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
from grafica.createShapes import createGPUShapeStatic, createOffShape

# Flags para controlar la view
viewing1 = True
viewing2 = False
viewing3 = False

# Inicializando el array view
view = None


class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.X = 17
        self.Y = 17
        self.Z = 17
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
    pipelinePhong = pi.SimplePhongShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0, 0, 0, 1.0)

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

    gpuBackground.texture = es.textureSimpleSetup(getAssetPath("stars.jpg"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    # Variables para asignar los colores del sol de manera dinamica
    rsol = 255
    gsol = 50
    bsol = 0

    # Aqui se crean las figuras planetarias
    gpuSol = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(2, rsol/255, gsol / 255, bsol/255, 10))  # Valor real 7

    gpuMercurio = createGPUShapeStatic(pipelinePhong, bs.crearEsferaConPuntosCaoticos(0.12, 1, 180 / 255, 0))  # Valor real 0.03
    gpuVenus = createGPUShapeStatic(pipelinePhong, bs.crearEsferaConZonasCaoticas(0.24, 1, 120 / 255, 0))  # Valor real 0.06
    gpuTierra = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.252, 0, 170 / 255, 0, 4))  # Valor real 0.063
    gpuLumbre = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.252, 218/255, 247 / 255, 166/255, 0))  # Planeta estatico para practicar las camaras
    gpuLuna = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.084, 100/255, 100/255, 100/255, 0))
    gpuMarte = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.132, 1, 0, 0, 0))
    gpuJupiter = createGPUShapeStatic(pipelinePhong, bs.crearEsferaConZonasCaoticas(0.8, 241 / 255, 173 / 255, 101 / 255))  # Valor real: 1.4
    gpuSaturno = createGPUShapeStatic(pipelinePhong, bs.crearEsferaConZonasCaoticas(0.7, 170/255, 170 / 255, 170 / 255))  # Valor real: 1.1
    gpuAnilloSaturnoA = createGPUShapeStatic(pipelinePhong, bs.crearAnillo(1.2, 1.15, 100 / 255, 100/255, 101/255))
    gpuAnilloSaturnoB = createGPUShapeStatic(pipelinePhong, bs.crearAnillo(1.15, 1.1, 1, 1, 1))
    gpuAnilloSaturnoC = createGPUShapeStatic(pipelinePhong, bs.crearAnillo(1.1, 1.05, 50/255, 50/255, 50/255))
    gpuAnilloSaturnoD = createGPUShapeStatic(pipelinePhong, bs.crearAnillo(1.05, 1, 0, 0, 0))
    gpuAnilloSaturnoE = createGPUShapeStatic(pipelinePhong, bs.crearAnillo(1, 0.9, 100/ 255, 100/255, 100/255))
    gpuUrano = createGPUShapeStatic(pipelinePhong, bs.crearEsferaConZonasCaoticas(0.3, 0, 1, 200 / 255))  # Valor real: 0.5
    gpuNeptuno = createGPUShapeStatic(pipelinePhong, bs.crearEsferaConZonasCaoticas(0.29, 0, 0, 1))  # Valor real: 0.49
    gpuAnilloNeptuno1 = createGPUShapeStatic(pipelinePhong, bs.crearAnillo(0.4, 0.395, 0, 200/255, 140/255))
    gpuEstelaUnitaria1 = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.5, 20/255, 120/255, 20/255, 0))  # Verde
    gpuEstelaUnitaria2 = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.5, 20/255, 20/255, 120/255, 0))  # Azul
    gpuEstelaUnitaria3 = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.5, 120/255, 120/255, 0/255, 0))  # Amarillo
    gpuEstelaUnitaria4 = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.5, 0/255, 120/255, 120/255, 0))  # cyan
    gpuEstelaUnitaria5 = createGPUShapeStatic(pipelinePhong, bs.crearEsfera(0.5, 180/255, 20/255, 20/255, 0))  # Rojo

    gpuNave1 = createOffShape(pipelineReadOff, "NabooFighter.off", 20 / 255, 120 / 255, 20 / 255)
    gpuNave2 = createOffShape(pipelineReadOff, "FromSP.off", 20 / 255, 20 / 255, 120 / 255)
    gpuNave3 = createOffShape(pipelineReadOff, "Tri_Fighter.off", 120 / 255, 120 / 255, 0 / 255)
    gpuNave4 = createOffShape(pipelineReadOff, "XJ5 X-wing starfighter.off", 0 / 255, 120 / 255, 120 / 255)
    gpuNave5 = createOffShape(pipelineReadOff, "NabooFighter.off", 180 / 255, 20 / 255, 20 / 255)
    tamanhoNaves = 0.2

    # Aqui se crea la view1
    cam_radius = 18
    viewPos = np.array([cam_radius, cam_radius, cam_radius])

    view1 = tr.lookAt(viewPos, np.array([0, 0, 0]), np.array([0, 0, 1]))

    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    view = view1
    t0 = glfw.get_time()
    N = 250
    C1 = curvas.generarCurvaCerradaNave1(N, 5, 0)
    indiceEstelas = 0
    indiceEstelaNave5 = 0
    matricesEstelas1 = [None] * (N//3)
    matricesEstelas2 = [None] * (N//3)
    matricesEstelas3 = [None] * (N//3)
    matricesEstelas4 = [None] * (N//3)
    matricesEstelas5 = [None] * (N//3)
    C2 = curvas.generarCurvaCerradaNave2(N, 6, 3)
    C3 = curvas.generarCurvaCerradaNave1(N, 7, -2)
    C4 = curvas.generarCurvaCerradaNave2(N, 10, 0)
    step = 0

    tiempoLimite = 222
    while not glfw.window_should_close(window):
        glfw.poll_events()
        # processCamera()

        t1 = glfw.get_time()
        velocidadTiempo = t1
        dt = velocidadTiempo - t0
        t0 = velocidadTiempo

        # Aqui dependiendo del flag activo actual se crea una u otra view
        if viewing1:
            view = view1
        elif viewing2:
            viewPos = crear_view2(velocidadTiempo * 1.25, 7)
            view = tr.lookAt(viewPos, np.array([0, 0, 0]), np.array([0, 0, 1]))
        elif viewing3:
            viewPos = crear_view2(velocidadTiempo/4, 2 + 16)
            view = tr.lookAt(viewPos, np.array([0, 0, 0]), np.array([0, 0, 1]))
        elif viewing4:
            Xesf = tamanhoNaves * 4 * np.sin(controller.pitch + np.pi/8) * np.cos(controller.yaw - np.pi/8)  # coordenada X esferica
            Yesf = tamanhoNaves * 4 * np.sin(controller.pitch + np.pi/8) * np.sin(controller.yaw - np.pi/8)  # coordenada Y esferica
            Zesf = tamanhoNaves * 4 * np.cos(controller.pitch + np.pi/8)
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
            velocidadNave = 5
        else:
            velocidadNave = 1

        matriz_estela_nueva5 = tr.matmul([
            tr.translate(controller.X, controller.Y, controller.Z),
            tr.uniformScale(0.01)])

        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            if indiceEstelaNave5 >= (N // 3):
                indiceEstelaNave5 = 0
            matricesEstelas5[indiceEstelaNave5] = matriz_estela_nueva5
            indiceEstelaNave5 += 1
            controller.X += velocidadNave * dt * np.cos(controller.yaw)
            controller.Y += velocidadNave * dt * np.sin(controller.yaw)

        if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            if indiceEstelaNave5 >= (N // 3):
                indiceEstelaNave5 = 0
            matricesEstelas5[indiceEstelaNave5] = matriz_estela_nueva5
            indiceEstelaNave5 += 1
            controller.X -= velocidadNave * dt * np.cos(controller.yaw)
            controller.Y -= velocidadNave * dt * np.sin(controller.yaw)

        if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
            controller.yaw += dt * 1.5

        if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
            controller.yaw -= dt * 1.5

        if (glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS):
            if indiceEstelaNave5 >= (N // 3):
                indiceEstelaNave5 = 0
            matricesEstelas5[indiceEstelaNave5] = matriz_estela_nueva5
            indiceEstelaNave5 += 1
            controller.posicionAnterior = [controller.X, controller.Y, controller.Z]
            controller.Z += velocidadNave * dt
        if (glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
                or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS):
            if indiceEstelaNave5 >= (N // 3):
                indiceEstelaNave5 = 0
            matricesEstelas5[indiceEstelaNave5] = matriz_estela_nueva5
            indiceEstelaNave5 += 1
            controller.Z -= velocidadNave * dt
        glUseProgram(pipelinePhong.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "projection"), 1, GL_TRUE, projection)

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
        matriz_sol = tr.matmul([tr.rotationZ(velocidadTiempo * 0.5), tr.uniformScale(1.2)])

        # Se crean las matrices de movimiento de los demas planetas
        matriz_mercurio = tr.matmul(
            [tr.rotationZ(2*velocidadTiempo),
             tr.translate(2 + 2, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_venus = tr.matmul(
            [tr.rotationZ(1.5*velocidadTiempo),
             tr.translate(2 + 3, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_tierra = tr.matmul(
            [tr.rotationZ(1.25*velocidadTiempo),
             tr.translate(2 + 4, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_luna = tr.matmul((
            [tr.rotationZ(1.25*velocidadTiempo),
             tr.translate(2 + 4, 0, 0),
             tr.rotationZ(1.5*velocidadTiempo),
             tr.translate(0.5, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)]))
        matriz_marte = tr.matmul(
            [tr.rotationZ(1.05*velocidadTiempo),
             tr.translate(2 + 5, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_jupiter = tr.matmul(
            [tr.rotationZ(velocidadTiempo/3),
             tr.translate(4 + 6, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_saturno = tr.matmul(
            [tr.rotationZ(velocidadTiempo/4),
             tr.translate(4 + 8, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_anillo_saturno1 = tr.matmul(
            [tr.rotationZ(velocidadTiempo/4),
             tr.translate(4 + 8, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_urano = tr.matmul(
            [tr.rotationZ(velocidadTiempo/5),
             tr.translate(4 + 10, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])
        matriz_neptuno = tr.matmul(
            [tr.rotationZ(velocidadTiempo/8),
             tr.translate(4 + 12, 0, 0),
             tr.rotationX(0.5),
             tr.rotationY(0.1*velocidadTiempo)])

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
            tr.rotationZ(math.pi/2),
            tr.uniformScale(tamanhoNaves)])

        matriz_estela_nueva1 = tr.matmul([
            tr.translate(C1[step-1, 0], C1[step-1, 1], C1[step-1, 2]),
            tr.rotationZ(-angle),
            tr.rotationY(math.pi/2),
            tr.uniformScale(0.01)])

        matriz_estela_nueva2 = tr.matmul([
            tr.translate(C2[step-1, 0], C2[step-1, 1], C2[step-1, 2]),
            tr.rotationZ(-angle),
            tr.rotationY(math.pi/2),
            tr.uniformScale(0.01)])

        matriz_estela_nueva3 = tr.matmul([
            tr.translate(C3[step-1, 0], C3[step-1, 1], C3[step-1, 2]),
            tr.rotationZ(-angle),
            tr.rotationY(math.pi/2),
            tr.uniformScale(0.01)])

        matriz_estela_nueva4 = tr.matmul([
            tr.translate(C4[step-1, 0], C4[step-1, 1], C4[step-1, 2]),
            tr.rotationZ(-angle),
            tr.rotationY(math.pi/2),
            tr.uniformScale(0.01)])

        if indiceEstelas >= (N//3):
            indiceEstelas = 0
        matricesEstelas1[indiceEstelas] = matriz_estela_nueva1
        matricesEstelas2[indiceEstelas] = matriz_estela_nueva2
        matricesEstelas3[indiceEstelas] = matriz_estela_nueva3
        matricesEstelas4[indiceEstelas] = matriz_estela_nueva4
        indiceEstelas += 1
        step = step + 1

        glUseProgram(pipelineTexture.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipelineTexture.shaderProgram, "transform"), 1, GL_TRUE, tr.uniformScale(10))
        pipelineTexture.drawCall(gpuBackground)

        # Lightning
        glUseProgram(pipelinePhong.shaderProgram)

        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Ka"), 1, 1, 1)
        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Kd"), 1, 1, 1)
        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "lightPosition"), 0, 0, 0)

        glUniform1f(glGetUniformLocation(pipelinePhong.shaderProgram, "constantAttenuation"), 0.5)
        glUniform1f(glGetUniformLocation(pipelinePhong.shaderProgram, "linearAttenuation"), 0.0009)
        glUniform1f(glGetUniformLocation(pipelinePhong.shaderProgram, "quadraticAttenuation"), 0.00032)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_sol)
        pipelinePhong.drawCall(gpuSol)

        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Ka"), 0.3, 0.3, 0.3)
        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Ks"), 0, 0, 0)
        glUniform1ui(glGetUniformLocation(pipelinePhong.shaderProgram, "shininess"), 1000)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_mercurio)
        pipelinePhong.drawCall(gpuMercurio)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_venus)
        pipelinePhong.drawCall(gpuVenus)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_tierra)
        pipelinePhong.drawCall(gpuTierra)

        # glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, tr.translate(5.5, 1, 1))
        # pipelinePhong.drawCall(gpuLumbre) # Esto es un objeto estatico para probar la camara en movimiento

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_luna)
        pipelinePhong.drawCall(gpuLuna)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_marte)
        pipelinePhong.drawCall(gpuMarte)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_jupiter)
        pipelinePhong.drawCall(gpuJupiter)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_saturno)
        pipelinePhong.drawCall(gpuSaturno)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
        pipelinePhong.drawCall(gpuAnilloSaturnoA)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
        pipelinePhong.drawCall(gpuAnilloSaturnoB)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
        pipelinePhong.drawCall(gpuAnilloSaturnoC)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
        pipelinePhong.drawCall(gpuAnilloSaturnoD)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_anillo_saturno1)
        pipelinePhong.drawCall(gpuAnilloSaturnoE)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_urano)
        pipelinePhong.drawCall(gpuUrano)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_neptuno)
        pipelinePhong.drawCall(gpuNeptuno)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_neptuno)
        pipelinePhong.drawCall(gpuAnilloNeptuno1)

        glUniform3f(glGetUniformLocation(pipelinePhong.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_nave1)
        pipelinePhong.drawCall(gpuNave1)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_nave2)
        pipelinePhong.drawCall(gpuNave2)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_nave3)
        pipelinePhong.drawCall(gpuNave3)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_nave4)
        pipelinePhong.drawCall(gpuNave4)

        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matriz_nave5)
        pipelinePhong.drawCall(gpuNave5)

        for matrizEstela in matricesEstelas1:
            if matrizEstela is not None:
                glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matrizEstela)
                pipelinePhong.drawCall(gpuEstelaUnitaria1)

        for matrizEstela in matricesEstelas2:
            if matrizEstela is not None:
                glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matrizEstela)
                pipelinePhong.drawCall(gpuEstelaUnitaria2)

        for matrizEstela in matricesEstelas3:
            if matrizEstela is not None:
                glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matrizEstela)
                pipelinePhong.drawCall(gpuEstelaUnitaria3)

        for matrizEstela in matricesEstelas4:
            if matrizEstela is not None:
                glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matrizEstela)
                pipelinePhong.drawCall(gpuEstelaUnitaria4)

        for matrizEstela in matricesEstelas5:
            if matrizEstela is not None:
                glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, matrizEstela)
                pipelinePhong.drawCall(gpuEstelaUnitaria5)


        glUniformMatrix4fv(glGetUniformLocation(pipelinePhong.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        pipelinePhong.drawCall(gpuAxis, GL_LINES)

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
    gpuEstelaUnitaria1.clear()
    gpuEstelaUnitaria2.clear()
    gpuEstelaUnitaria3.clear()
    gpuEstelaUnitaria4.clear()
    gpuEstelaUnitaria5.clear()

    glfw.terminate()


if __name__ == "__main__":
    main()
