import pygame
import numpy as np
from vector import Vector
from abc import ABC, abstractmethod
from polygon_shapes import *

class ComponentBase(ABC):
    def __init__(self, entity, position_in_entity: Vector, orientation_in_entity,
                 input_functions=[],
                 mass=0, moment_of_inertia=0,
                 bounding_radius=None):
        self.entity = entity  # reference to entity component is part of
        self.position_in_entity = position_in_entity
        self.orientation_in_entity = orientation_in_entity
        self.input_functions = input_functions

        self.mass = mass
        self.moment_of_inertia = moment_of_inertia

        self.gravitational_forces = []
        self.aerodynamic_forces = []
        self.propulsion_forces = []
        self.contact_forces = []

        self.bounding_radius = bounding_radius

    def _reset_forces(self):
        self.gravitational_forces = []
        self.aerodynamic_forces = []
        self.propulsion_forces = []
        self.contact_forces = []

    def get_position_relative_to_center_of_gravity(self):
        return self.position_in_entity - self.entity.get_center_of_gravity()

    def _compute_control_inputs(self):
        pass

    def _compute_aerodynamic_forces(self, wind_in_global):
        return Vector()

    def get_global_position(self):
        return self.entity.position_of_center_of_gravity + self.get_position_relative_to_center_of_gravity().rotate(self.entity.orientation)

    def get_global_velocity(self):
        return self.entity.velocity \
               + Vector(-np.sin(self.entity.orientation + self.orientation_in_entity),
                         np.cos(self.entity.orientation + self.orientation_in_entity))\
               * self.get_position_relative_to_center_of_gravity().rotate(self.entity.orientation).norm()\
               * self.entity.velocity_angular

    def get_relative_position_of(self, component):
        return component.get_global_position() - self.get_global_position()

    def get_relative_velocity_of(self, component):
        return component.get_global_velocity() - self.get_global_velocity()

    def get_distance_to(self, component):
        return self.get_relative_position_of(component).norm()

    def get_wind_emitted_to_component(self, component):
        # describes the wind emitted to other components in global coordinate system
        return Vector()

    def get_total_force(self):
        total_force = Vector()
        for gravitational_force in self.gravitational_forces:
            total_force += gravitational_force
        for aerodynamic_force in self.aerodynamic_forces:
            total_force += aerodynamic_force
        for propulsion_force in self.propulsion_forces:
            total_force += propulsion_force
        for contact_force in self.contact_forces:
            total_force += contact_force
        return total_force

    def update(self, simulator):
        total_forces_on_entity_old = self.entity._get_total_force()

        # check for interaction with environment
        self._reset_forces()
        self._compute_control_inputs()

        for entity in simulator.entities:
            if not entity == self.entity:
                for component in entity.components:
                    if not component == self:
                        d_position = self.get_relative_position_of(component)
                        d_velocity = self.get_relative_velocity_of(component)

                        # update gravitational forces
                        gravitational_force = 5e5 * 6.67 * np.power(10., -11) * (self.mass * component.mass) / max(np.power(d_position.norm(), 2), 1)
                        self.gravitational_forces.append(d_position.unit_length() * gravitational_force)

                        # update aerodynamic forces
                        aerodynamic_force = self._compute_aerodynamic_forces(component.get_wind_emitted_to_component(self))
                        self.aerodynamic_forces.append(aerodynamic_force)

                        # get contact between components
                        if self.bounding_radius and component.bounding_radius:
                            bounding_distance = self.get_distance_to(component)  - (self.bounding_radius + component.bounding_radius)
                            penetration_depth = np.abs(bounding_distance) if bounding_distance < 0 else 0

                            velocity_radial = d_velocity.dot(d_position) / d_position.norm()
                            # velocity_tangential = d_velocity.dot(d_position.rotate(np.pi/2)) / d_position.norm()

                            # if hasattr(self, 'length'):
                            #     print(self.get_global_position(), bounding_distance)
                            if penetration_depth > 0 and d_velocity.norm() > 10:
                                print('crash')
                            elif penetration_depth > 0:
                                normal_force = -d_position.unit_length() * 100 * self.entity.get_total_mass() * (penetration_depth - 1e-2 * velocity_radial)
                                # TODO: implement friction force
                                # if hasattr(self, 'height'):
                                #     # self.contact_forces.append(Vector)
                                #     print(penetration_depth, d_velocity.norm(), normal_force)
                                self.contact_forces.append(normal_force)




                                # self.contact_forces.append(contact_force)


    def _draw_geometry(self, simulator):
        pass

    def _draw_forces(self, simulator):
        pass


        # for aerodynamic_force in self.aerodynamic_forces:
        #     total_force += aerodynamic_force
        # for propulsion_force in self.propulsion_forces:
        #     total_force += propulsion_force


    def draw(self, simulator):
        self._draw_geometry(simulator)
        self._draw_forces(simulator)
