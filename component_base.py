import numpy as np
from vector import Vector
from abc import ABC, abstractmethod


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

    def _compute_control_inputs(self):
        pass

    def _compute_aerodynamic_forces(self, wind_in_global):
        pass

    def get_global_position(self):
        return self.entity.position + self.position_in_entity.rotate(self.entity.orientation)

    def get_total_force(self):
        total_force = Vector()
        for gravitational_force in self.gravitational_forces:
            total_force += gravitational_force
        for aerodynamic_force in self.aerodynamic_forces:
            total_force += aerodynamic_force
        for propulsion_force in self.propulsion_forces:
            total_force += propulsion_force
        return total_force

    def update(self, simulator):
        self._compute_control_inputs()

        # check for interaction with environment
        self._reset_forces()
        for entity in simulator.entities:
            for component in entity.components:
                if not component == self:
                    d_position = component.get_global_position() - self.get_global_position()

                    # update gravitational forces
                    gravitational_force = 3e5 * 6.67 * np.power(10., -11) * (self.mass * component.mass) / max(np.power(d_position.norm(), 2), 1e-3)
                    self.gravitational_forces.append(d_position.unit_length() * gravitational_force)

                    # update aerodynamic forces
                    if callable(getattr(entity, 'get_wind', None)):
                        self._compute_aerodynamic_forces(entity.get_wind(self))

                    # get contact between planets
                    if self.bounding_radius and component.bounding_radius:
                        distance = d_position.norm() - (self.bounding_radius + component.bounding_radius)
                        if distance < 0:
                            contact_force = d_position.unit_length() * np.abs(distance)**4
                            self.contact_forces.append(contact_force)
                            # print(distance, contact_force, gravitational_force)



    def draw(self, simulator):
        pass
