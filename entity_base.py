import pygame
from abc import ABC, abstractmethod
from vector import Vector
from polygon_shapes import *

class EntityBase(ABC):
    def __init__(self, position_init: Vector = Vector(), orientation_init=0, name=''):
        self.name = name
        self.position = position_init
        self.orientation = orientation_init  # rad
        self.velocity = Vector()
        self.velocity_angular = 0
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def _get_total_mass(self):
        total_mass = 0
        for component in self.components:
            total_mass += component.mass
        return total_mass

    def _get_center_of_mass(self):
        center_of_mass = Vector()
        for component in self.components:
            center_of_mass += component.get_global_position() * component.mass
        center_of_mass = center_of_mass / self._get_total_mass()
        return center_of_mass

    def _get_moment_of_inertia(self):
        center_of_mass = self._get_center_of_mass()
        total_moment_of_inertia = 0
        for component in self.components:
            rel_pos = component.get_global_position() - center_of_mass
            total_moment_of_inertia += (rel_pos[0]**2 + rel_pos[1]**2)**2 * component.mass + component.moment_of_inertia
        return total_moment_of_inertia

    def _get_total_force(self):
        total_force = Vector()
        for component in self.components:
            total_force += component.get_total_force()
        return total_force

    def _get_total_torque(self):
        total_torque = 0
        center_of_mass = self._get_center_of_mass()
        for component in self.components:
            rel_pos = component.get_global_position() - center_of_mass
            component_force = component.get_total_force()
            total_torque += rel_pos[0] * component_force[1]
            total_torque += rel_pos[1] * -component_force[0]
        return total_torque

    def _draw_geometry(self, simulator):
        pass

    def _draw_forces(self, simulator):
        # draw net gravitational forces and CG
        total_gravitational_force = Vector()
        for component in self.components:
            for gravitational_force in component.gravitational_forces:
                total_gravitational_force += gravitational_force

        arrow = get_arrow(length=total_gravitational_force.norm())
        arrow = rotate_polygon(arrow, total_gravitational_force.get_angle())
        arrow = translate_polygon(arrow, self._get_center_of_mass())
        arrow = simulator.polygon_from_physical(arrow)
        pygame.draw.polygon(simulator.window, color=(255, 0, 0), points=make_pairs(arrow))


    def update_and_draw(self, simulator, time_step):
        for component in self.components:
            component.update(simulator)

        acceleration = self._get_total_force() / self._get_total_mass()
        acceleration_angular = self._get_total_torque() / self._get_moment_of_inertia()
        self.velocity += acceleration * time_step
        self.velocity_angular += acceleration_angular * time_step
        self.position += self.velocity * time_step
        self.orientation += self.velocity_angular * time_step

        self._draw_geometry(simulator)
        for component in self.components:
            component.draw(simulator)
        self._draw_forces(simulator)