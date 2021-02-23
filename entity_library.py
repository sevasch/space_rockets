from vector import Vector
from entity_base import EntityBase
from component_library import *

class Planet(EntityBase):
    def __init__(self, position_init: Vector=Vector(), radius=10, density=1, color=(0, 255, 0),
                 athmosphere_radius=1.5, athmosphere_density=1, athmosphere_color=(0, 0, 255)):
        super().__init__(position_init=position_init, orientation_init=0)
        self.components.append(Athmosphere(self, position_in_entity=Vector(), radius=athmosphere_radius, density=athmosphere_density, color=athmosphere_color))
        self.components.append(Sphere(self, position_in_entity=Vector(), radius=radius, density=density, color=color))

    def get_wind(self, position):
        # TODO: define function to get wind in global coordinates
        pass



class Rocket(EntityBase):
    def __init__(self, position_init: Vector=Vector(), mass=1000, height=10, diameter=2, color=(255, 0, 0)):
        super().__init__(position_init=position_init, orientation_init=0)
        self.components.append(RocketBody(self, position_in_entity=Vector(), orientation_in_entity=0,
                                          mass=mass/3,
                                          lift_coeff=0.5, drag_coeff=0.5, lift_area=1, drag_area=1))
        self.components.append(Thruster())