import numpy as np
import pygame
from component_base import ComponentBase
from polygon_shapes import *
from apostolyuk import get_lift_coeff, get_drag_coeff

class Mass(ComponentBase):
    def __init__(self, entity, position_in_entity, mass, moment_of_inertia):
        super().__init__(entity, position_in_entity=position_in_entity, orientation_in_entity=0, mass=mass, moment_of_inertia=moment_of_inertia)


class Sphere(ComponentBase):
    def __init__(self, entity, position_in_entity, radius, density, color=(0, 255, 0)):
        volume = 4 / 3 * np.pi * np.power(float(radius), 3)
        moment_of_inertia = 2 / 5 * volume * density * radius ** 2
        super().__init__(entity, position_in_entity=position_in_entity, orientation_in_entity=0,
                         mass=volume * density, moment_of_inertia=moment_of_inertia)
        self.radius = radius
        self.bounding_radius = radius
        self.color = color

    def draw(self, simulator):
        pygame.draw.circle(simulator.window, color=self.color,
                           center=(simulator.position_from_physical(self.get_global_position())).get(),
                           radius=self.radius * simulator.scale)

class Athmosphere(ComponentBase):
    def __init__(self, entity, position_in_entity, radius, density, color=(100, 100, 255)):
        super().__init__(entity, position_in_entity=position_in_entity, orientation_in_entity=0,
                         mass=0, moment_of_inertia=0)
        self.radius = radius
        self.density = density
        self.color = color

    def draw(self, simulator):
        pygame.draw.circle(simulator.window, color=self.color,
                           center=(simulator.position_from_physical(self.get_global_position())).get(),
                           radius=self.radius * simulator.scale)


class RocketBody(ComponentBase):
    def __init__(self, entity, position_in_entity, orientation_in_entity=0, mass=1, moment_of_inertia=0, lift_coeff=0.5, drag_coeff=0.5, lift_area=1, drag_area=1):
        super().__init__(entity, position_in_entity, orientation_in_entity,
                         input_functions=[],
                         mass=mass, moment_of_inertia=moment_of_inertia,
                         bounding_radius=None)
        self.lift_coeff = lift_coeff
        self.drag_coeff = drag_coeff
        self.lift_area = lift_area
        self.drag_area = drag_area
        self.induced_forces = [Vector()]

    # TODO: REWORK
    def _compute_induced_forces(self, relative_wind):
        relative_wind = relative_wind.rotate(-self.orientation_in_entity)
        lift = self.lift_coeff * relative_wind[1] * self.lift_area
        drag = self.drag_coeff * relative_wind[0] * self.drag_area
        self.induced_forces[0] = Vector(drag, lift)


class Thruster(ComponentBase):
    def __init__(self, entity, position_in_entity, orientation_in_entity, input_functions=[], mass=1, max_thrust=1):
        super().__init__(entity, position_in_entity, orientation_in_entity,
                         input_functions=input_functions,
                         mass=mass, moment_of_inertia=0,
                         bounding_radius=None)
        self.max_thrust = max_thrust
        self.original_angle = orientation_in_entity
        
    def _compute_control_inputs(self):
        if len(self.input_functions) > 0:
            throttle = self.input_functions[0]()
            self.thrust_forces = [Vector(throttle * self.max_thrust, 0).rotate(self.orientation_in_entity).rotate(self.entity.orientation)]
        if len(self.input_functions) > 1:
            self.orientation_in_entity = self.original_angle + self.input_functions[1]()

    def draw(self, simulator):
        thruster_polygon = [Vector(0, 0), Vector(0.6, 0.5), Vector(1, 1), Vector(-1, 1), Vector(-0.6, 0.5)]
        flame_polygon = [Vector(-0.5, 1), Vector(0, 1 + self.self.input_function[0]() * self.max_thrust)]
        scale_polygon(thruster_polygon, simulator.scale)
        scale_polygon(flame_polygon, simulator.scale)
        rotate_polygon(thruster_polygon, self.entity.orientation + self.orientation_in_entity)
        rotate_polygon(flame_polygon, self.entity.orientation + self.orientation_in_entity)
        translate_polygon(thruster_polygon, self.get_global_position() * simulator.scale)
        translate_polygon(flame_polygon, self.get_global_position() * simulator.scale)


class Airfoil(ComponentBase):
    def __init__(self, entity, mass, position_in_entity, orientation_in_entity, area, input_functions=[]):
        super().__init__(entity, mass, position_in_entity, orientation_in_entity, input_functions)
        self.area = area
        self.induced_forces = [Vector(), Vector()]
        ratio = 8
        scale = 0.5
        self.polygon_shape = [Vector(scale * area/3, scale * area/ratio),
                              Vector(scale * area/3, 0),
                              Vector(-2*scale * area/2, 0),
                              Vector(-2*scale * area/2, scale * area/ratio)]

    def _compute_control_inputs(self):
        self.orientation_in_entity = self.input_functions[0]()

    # TODO: REWORK
    def _compute_induced_forces(self, relative_wind):
        relative_wind = relative_wind.rotate(-self.orientation_in_entity)
        angle_of_attack = np.arctan2(relative_wind[1], -relative_wind[0])
        lift = get_lift_coeff(angle_of_attack) * relative_wind.norm() * self.area
        drag = get_drag_coeff(angle_of_attack) * relative_wind.norm() * self.area
        # print('{:5.3f}, {:5.3f}, {:5.3f}'.format(relative_wind.norm(), self.entity.velocity[1], self.entity.velocity[1]))
        self.induced_forces[0] = Vector(-drag, 0).rotate(-angle_of_attack)
        self.induced_forces[1] = Vector(0, lift).rotate(-angle_of_attack)

    def draw(self):
        # TODO: REWORK
        pass