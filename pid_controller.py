import numpy as np
import matplotlib.pyplot as plt

class PIDController():
    def __init__(self, k_proportional:float, k_integral:float=0, k_derivative:float=0):
        self.k_proportional = k_proportional
        self.k_integral = k_integral
        self.k_derivative = k_derivative

        self.error_last = 0
        self.error_integrated = 0

    def get(self, signal, target):
        error = target - signal
        self.error_integrated += error
        error_derivative = error - self.error_last
        output = self.k_proportional * error \
                 + self.k_integral * self.error_integrated \
                 + self.k_derivative * error_derivative
        # print('signal: {}, error: {}, integrated: {}, derivative: {}, output: {}'.format(signal, error, self.error_integrated, error_derivative, output))
        return output

if '__main__' == __name__:
    n = 100
    target = np.ones(n)
    pid = PIDController(k_proportional=1, k_integral=0, k_derivative=0.8)
    signal = np.zeros(n)
    i = 1
    while i < n:

        signal[i] = signal[i - 1] + 0.1 * pid.get(signal[i - 1], target[i])
        i += 1

    plt.plot(target, label='target')
    plt.plot(signal, label='signal')
    plt.ylim(-0.5, 1.5)
    plt.show()

