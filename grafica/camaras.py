import numpy as np

# Esto es para crear la vista que sigue al planeta Tierra
def crear_view2(theta):
    cam_radius = 2 + 1.33
    cam_x1 = cam_radius * np.cos(1.25 * theta)
    cam_y1 = cam_radius * np.sin(1.25 * theta)
    cam_z1 = 0
    viewEarthEclipse = np.array([cam_x1, cam_y1, cam_z1])
    return viewEarthEclipse


# Esto crea la view de los anillos de Saturno
def crear_view3(theta):
    cam_radius2 = 2 + 10
    cam_x2 = cam_radius2 * np.cos(theta / 4) * np.cos(4)
    cam_y2 = cam_radius2 * np.sin(theta / 4)
    cam_z2 = - cam_radius2 * np.cos(theta / 4) * np.sin(4)

    viewSaturnRings = np.array([cam_x2, cam_y2, cam_z2])
    return viewSaturnRings


