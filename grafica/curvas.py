import numpy as np


def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


def bezierMatrix(P0, P1, P2, P3):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Bezier base matrix is a constant
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])

    return np.matmul(G, Mb)


# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)

    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T

    return curve

def generarCurvaCerradaNave1(N, scalexy, altura):
    R0 = np.array([[-scalexy * 1, 0, altura]]).T
    R1 = np.array([[-scalexy * 1, scalexy * 1, altura]]).T
    R2 = np.array([[scalexy * 1, scalexy * 1, altura]]).T
    R3 = np.array([[scalexy * 1, 0, altura]]).T

    M1 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve1 = evalCurve(M1, N)[:N-1]

    R0 = np.array([[scalexy * 1, 0, altura]]).T
    R1 = np.array([[scalexy * 1, -scalexy * 1, altura]]).T
    R2 = np.array([[-scalexy * 1, -scalexy * 1, altura]]).T
    R3 = np.array([[-scalexy * 1, 0, altura]]).T

    M2 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve2 = evalCurve(M2, N)[:N-1]

    C = np.concatenate((bezierCurve1, bezierCurve2), axis=0)
    return C

def generarCurvaCerradaNave2(N, scalexy, altura):
    R0 = np.array([[-scalexy * 1, 0, altura]]).T
    R1 = np.array([[-scalexy * 1, -scalexy * 1, altura]]).T
    R2 = np.array([[scalexy * 1, -scalexy * 1, altura]]).T
    R3 = np.array([[scalexy * 1, 0, altura]]).T

    M1 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve1 = evalCurve(M1, N)[:N-1]


    R0 = np.array([[scalexy * 1, 0, altura]]).T
    R1 = np.array([[scalexy * 1, scalexy * 1, altura]]).T
    R2 = np.array([[-scalexy * 1, scalexy * 1, altura]]).T
    R3 = np.array([[-scalexy * 1, 0, altura]]).T

    M2 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve2 = evalCurve(M2, N)[:N-1]

    C = np.concatenate((bezierCurve1, bezierCurve2), axis=0)
    return C

def generarCurvaCerradaNave3(N):
    R0 = np.array([[0, 0, 0]]).T
    R1 = np.array([[-4, 0, 0]]).T
    R2 = np.array([[4, 6, 0]]).T
    R3 = np.array([[0, 6, 0]]).T

    M1 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve1 = evalCurve(M1, N)

    R0 = np.array([[0, 6, 0]]).T
    R1 = np.array([[-4, 6, 0]]).T
    R2 = np.array([[4, 0, 0]]).T
    R3 = np.array([[0, 0, 0]]).T

    M2 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve2 = evalCurve(M2, N)

    C = np.concatenate((bezierCurve1, bezierCurve2), axis=0)
    return C