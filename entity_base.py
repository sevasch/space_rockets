import pygame
import numpy as np
from abc import ABC, abstractmethod
from vector import Vector
from polygon_shapes import *

class EntityBase(ABC):
    def __init__(self, position_init: Vector = Vector(), orientation_init=0, name='', fixed=False, can_crash=False, forget_range=0):
        self.name = name
        self.position_of_center_of_gravity = position_init
        self.orientation = orientation_init  # rad
        self.velocity = Vector()
        self.velocity_angular = 0
        self.components = []
        self.fixed = fixed
        self.can_crash = can_crash
        self.is_crashed = False
        self.forget_range = forget_range

        print('created entity at {}'.format(self.position_of_center_of_gravity))

    def add_component(self, component):
        self.components.append(component)

    def get_total_mass(self):
        total_mass = 0
        for component in self.components:
            total_mass += component.mass
        return total_mass

    def get_center_of_gravity(self):
        center_of_gravity = Vector()
        for component in self.components:
            center_of_gravity += component.position_in_entity * component.mass
        center_of_gravity = center_of_gravity / self.get_total_mass()
        return center_of_gravity  # in entity coordinate system

    def get_distance_to(self, other):
        return (self.position_of_center_of_gravity - other.position_of_center_of_gravity).norm()

    def _get_moment_of_inertia(self):
        total_moment_of_inertia = 0
        for component in self.components:
            rel_pos = component.get_position_relative_to_center_of_gravity()
            total_moment_of_inertia += (rel_pos[0]**2 + rel_pos[1]**2)**2 * component.mass + component.moment_of_inertia
        return total_moment_of_inertia

    def _get_total_force(self):
        total_force = Vector()
        for component in self.components:
            total_force += component.get_total_force()
        return total_force

    def _get_total_torque(self):
        total_torque = 0
        for component in self.components:
            rel_pos = component.get_position_relative_to_center_of_gravity().rotate(self.orientation)
            component_force = component.get_total_force()
            total_torque += rel_pos[0] * component_force[1]
            total_torque += rel_pos[1] * -component_force[0]
        return total_torque

    def _draw_geometry(self, simulator):
        pass

    # def _draw_forces(self, simulator):
    #     # draw net gravitational forces and CG
    #     total_gravitational_force = Vector()
    #     for component in self.components:
    #         for gravitational_force in component.gravitational_forces:
    #             total_gravitational_force += gravitational_force
    #
    #     arrow = get_arrow(length=total_gravitational_force.norm())
    #     arrow = rotate_polygon(arrow, total_gravitational_force.get_angle())
    #     arrow = translate_polygon(arrow, self._get_center_of_gravity())
    #     arrow = simulator.polygon_from_physical(arrow)
    #     pygame.draw.polygon(simulator.window, color=(255, 0, 0), points=make_pairs(arrow))

    def crash(self):
        self.is_crashed = self.can_crash

    def update_and_draw(self, simulator, time_step):
        for component in self.components:
            component.update(simulator)

        if not self.is_crashed:
            if not self.fixed:
                acceleration = self._get_total_force() / self.get_total_mass()
                acceleration_angular = self._get_total_torque() / self._get_moment_of_inertia()
                self.velocity += acceleration * time_step
                self.velocity_angular += acceleration_angular * time_step
                self.position_of_center_of_gravity += self.velocity * time_step
                self.orientation += self.velocity_angular * time_step

            self._draw_geometry(simulator)
            for component in self.components:
                component.draw(simulator)
            pygame.draw.circle(simulator.window, (0, 0, 0), simulator.position_from_physical(self.position_of_center_of_gravity).get(), simulator.scale * 0.05)
        else:
            explosion_radius_init = self.get_total_mass() / 10
            explosion_radius = explosion_radius_init
            for i in range(10):
                x_offset = np.random.random() - 0.5
                y_offset = np.random.random() - 0.5
                for j in range(i+1):
                    pygame.draw.circle(simulator.window, (255, 255 - 20*i, 0), simulator.position_from_physical(self.position_of_center_of_gravity + Vector(x_offset, y_offset) * explosion_radius_init * 0.5).get(), simulator.scale * explosion_radius)
                explosion_radius *= 0.5