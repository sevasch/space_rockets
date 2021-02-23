import numpy as np
import matplotlib.pyplot as plt

def get_lift_coeff(angle_of_attack, parameters=[0, 1.1]):
    lift_coeffs = parameters[0] + np.zeros_like(angle_of_attack)
    for i, parameter in enumerate(parameters):
        lift_coeffs += parameter * np.sin(2 * i * angle_of_attack)
    return lift_coeffs

def get_drag_coeff(angle_of_attack, parameters=[0.4, -0.8]):
    drag_coeffs = parameters[0] + np.zeros_like(angle_of_attack)
    for i, parameter in enumerate(parameters):
        drag_coeffs += parameter * np.cos(2 * i * angle_of_attack)
    return drag_coeffs

if __name__ == '__main__':
    aoa = np.linspace(-np.pi, np.pi, 100)
    lift_coeffs = get_lift_coeff(aoa)
    drag_coeffs = get_drag_coeff(aoa)
    plt.plot(aoa, lift_coeffs, label='lift')
    plt.plot(aoa, drag_coeffs, label='drag')
    plt.legend()
    plt.grid(True)
    plt.show()