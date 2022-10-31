import numpy as np
import grafica.transformations as tr

# Esto es para crear la vista que sigue al planeta Tierra
def crear_view2(theta, radius):
    cam_radius = radius
    cam_x = cam_radius * np.cos(theta)
    cam_y = cam_radius * np.sin(theta)
    cam_z = 0.5
    viewEarthEclipse = np.array([cam_x, cam_y, cam_z])
    return viewEarthEclipse


# Esto crea la view de los anillos de Saturno
def crear_view3(theta, radius):
    cam_radius2 = radius
    cam_x2 = cam_radius2 * np.cos(theta / 4) * np.cos(4)
    cam_y2 = cam_radius2 * np.sin(theta / 4)
    cam_z2 = - cam_radius2 * np.cos(theta / 4) * np.sin(4)

    viewSaturnRings = np.array([cam_x2, cam_y2, cam_z2])
    return viewSaturnRings
