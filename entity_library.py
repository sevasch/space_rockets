from vector import Vector
from entity_base import EntityBase
from component_library import *


class Planet(EntityBase):
    def __init__(self, position_init: Vector = Vector(),
                 radius=10, density=1, color=(0, 255, 0),
                 athmosphere_radius=1.5, athmosphere_density=1, athmosphere_color=(0, 0, 255), max_wind=0):
        super().__init__(position_init=position_init, orientation_init=0, fixed=True, can_crash=False)
        self.components.append(
            Athmosphere(self, position_in_entity=Vector(), radius=athmosphere_radius, density=athmosphere_density,
                        color=athmosphere_color, max_wind=max_wind))
        self.components.append(Sphere(self, position_in_entity=Vector(), radius=radius, density=density, color=color))


class Rocket(EntityBase):
    def __init__(self, position_init: Vector = Vector(), orientation_init=0,
                 mass=1000, max_thrust=10000, max_thrust_thrusters=100,
                 height=10, diameter=2, rel_height_pressure_center=0.3,
                 color=(251, 55, 69),#(211, 211, 211),
                 throttle_fn=lambda: 1, vector_fn=lambda: 0,
                 thruster_left_fn=lambda: 0, thruster_right_fn=lambda: 0):
        super().__init__(position_init=position_init, orientation_init=orientation_init, can_crash=True)
        self.components.append(RocketBody(self, position_in_entity=Vector(0, 0), orientation_in_entity=0,
                                          mass=mass / 10 * 2, moment_of_inertia=0,
                                          height=height, diameter=diameter,
                                          rel_height_pressure_center=rel_height_pressure_center,
                                          lift_coeff=0.5, drag_coeff=0.5, lift_area=height * diameter,
                                          drag_area=np.pi * diameter ** 2 / 4,
                                          color=color))
        self.components.append(
            Thruster(self, position_in_entity=Vector(0, -height * rel_height_pressure_center), orientation_in_entity=0,
                     input_functions=[throttle_fn, vector_fn],
                     mass=mass / 10, max_thrust=max_thrust))
        self.components.append(Mass(self, position_in_entity=Vector(0, height * (1 - rel_height_pressure_center - 0.5)),
                                    mass=mass / 10 * 2, moment_of_inertia=0))
        self.components.append(
            Thruster(self, position_in_entity=Vector(-diameter / 2, 0.65 * height), orientation_in_entity=-np.pi / 2,
                     input_functions=[thruster_left_fn],
                     mass=mass / 10, max_thrust=max_thrust_thrusters))
        self.components.append(
            Thruster(self, position_in_entity=Vector(diameter / 2, 0.65 * height), orientation_in_entity=np.pi / 2,
                     input_functions=[thruster_right_fn],
                     mass=mass / 10, max_thrust=max_thrust_thrusters))
        self.components.append(
            LandingLeg(self, position_in_entity=Vector(-diameter, -height * rel_height_pressure_center - 0.4),
                       orientation_in_entity=-0.2, length=0.4, width=0.2))
        self.components.append(
            LandingLeg(self, position_in_entity=Vector(diameter, -height * rel_height_pressure_center - 0.4),
                       orientation_in_entity=0.2, length=0.4, width=0.2))
