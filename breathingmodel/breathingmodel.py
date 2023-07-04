import math

P = (1.581, -5.534, 0.5523)
w = (1.214, 0.001414, 2.401)
c = (-0.3132, 3.297, -2.381)

R = (1.137, 1.137)  # airflow
C = (0.1066, 0.0533)  # lung compliance
tao = ((2.115, 0.5289), (0.2198, 1.0320))


def twocomplinear(t):
    result = 0
    for i in range(3):
        for lung in range(2):
            result += P[i] * C[lung] * (
                    math.sin(w[i] * t + c[i]) - w[i] * ((R[lung] * C[lung]) ** 2) * math.cos(w[i] * t + c[i])) / (
                              1 + w[i] * w[i] * ((R[lung] * C[lung]) ** 2))
    return result
