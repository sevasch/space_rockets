import pygame
from simulator import Simulator
from entity_library import *
from component_library import *
from pid_controller import PIDController

# TODO: first, do rockets only, implement aerodynamics a bit later with athmosphere

if '__main__' == __name__:

    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 1200

    RANGE = 10000

    s = Simulator(window_size=(WINDOW_WIDTH, WINDOW_HEIGHT), scale_init=100)
    s.camera_center = Vector(0, 0)

    # add home planet
    s.add_entity(Planet(position_init=Vector(0, 100), radius=100, density=5, color=(0, 255, 0),
                        athmosphere_radius=200, athmosphere_density=1, athmosphere_color=(100, 100, 255), max_wind=0))

    # add other planets randomly
    for i in range(50):
        radius = np.random.randint(5, 50)
        athmosphere_radius = radius + np.random.randint(100)
        position = Vector(np.random.randint(-RANGE, RANGE), np.random.randint(-RANGE, RANGE))
        color = tuple([np.random.randint(0, 256) for _ in range(3)])
        athmosphere_color = tuple([max(0, c - 100) for c in color])

        distances = [(entity.position_of_center_of_gravity - position).norm() for entity in s.entities]

        if min(distances) > 5 * radius:
            s.add_entity(Planet(position_init=position, radius=radius, density=5 + np.random.rand() * 10, color=color,
                                athmosphere_radius=athmosphere_radius, athmosphere_density=np.random.rand() * 10, athmosphere_color=athmosphere_color,
                                max_wind=np.random.randint(2) * np.random.randint(-20, 20)))

    pid1 = PIDController(k_proportional=0.5, k_integral=0, k_derivative=0)
    pid2 = PIDController(k_proportional=0, k_integral=0, k_derivative=0)
    pid3 = PIDController(k_proportional=0, k_integral=0, k_derivative=0)
    pid4 = PIDController(k_proportional=0, k_integral=0, k_derivative=0)
    s.add_entity(rocket := Rocket(position_init=Vector(0, -3), orientation_init=np.pi,
                                  mass=100, max_thrust=250, max_thrust_thrusters=100,
                                  height=2, diameter=0.3, rel_height_pressure_center=0.2,
                                  throttle_fn=lambda: (1 if pygame.key.get_pressed()[pygame.K_w] else 0),
                                  vector_fn=lambda: pid1.get(-rocket.velocity_angular,0.5 if pygame.key.get_pressed()[pygame.K_a] else (-0.5 if pygame.key.get_pressed()[pygame.K_d] else 0)),
                                  thruster_left_fn=lambda: (1 if pygame.key.get_pressed()[pygame.K_q] else 0) + (1 if pid2.get(-rocket.velocity_angular, 0) > 0.3 else 0),
                                  thruster_right_fn=lambda: (1 if pygame.key.get_pressed()[pygame.K_e] else 0)  + (1 if pid3.get(rocket.velocity_angular, 0) > 0.3 else 0)))

    s.track(rocket)
    s.run(60)
