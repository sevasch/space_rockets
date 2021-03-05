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
                         mass=volume * density, moment_of_inertia=moment_of_inertia, bounding_radius=radius)
        self.radius = radius
        self.color = color

    def draw(self, simulator):
        pygame.draw.circle(simulator.window, color=self.color,
                           center=(simulator.position_from_physical(self.get_global_position())).get(),
                           radius=self.radius * simulator.scale)

class Athmosphere(ComponentBase):
    def __init__(self, entity, position_in_entity, radius, density, color=(100, 100, 255), max_wind=0):
        super().__init__(entity, position_in_entity=position_in_entity, orientation_in_entity=0,
                         mass=0, moment_of_inertia=0)
        self.radius = radius
        self.density = density
        self.color = color
        self.max_wind = max_wind

    def get_wind_emitted_to_component(self, component):
        d_position = component.get_global_position() - self.get_global_position()
        d_velocity = self.get_global_velocity() - component.get_global_velocity()
        distance_to_center = d_position.norm()
        if distance_to_center < self.radius:
            additional_wind_speed = self.max_wind / self.radius * distance_to_center
            return d_velocity + d_position.rotate(-np.pi/2).unit_length() * additional_wind_speed
        else:
            return Vector()


    def draw(self, simulator):
        pygame.draw.circle(simulator.window, color=self.color,
                           center=(simulator.position_from_physical(self.get_global_position())).get(),
                           radius=self.radius * simulator.scale)

class LandingLeg(ComponentBase):
    def __init__(self, entity, position_in_entity, orientation_in_entity, length, width, mass=0):
        super().__init__(entity, position_in_entity=position_in_entity, orientation_in_entity=orientation_in_entity,
                         mass=mass, moment_of_inertia=0, bounding_radius=width/2)
        self.length = length
        self.width = width

    def draw(self, simulator):
        leg_polygon = [Vector(-self.width/2, 0),
                       Vector(-self.width/2, self.width/4),
                       Vector(-self.width/6, self.width/4),
                       Vector(-self.width/6, self.length),
                       Vector(self.width/6, self.length),
                       Vector(self.width/6, self.width/4),
                       Vector(self.width/2, self.width/4),
                       Vector(self.width/2, 0)]
        leg_polygon = rotate_polygon(leg_polygon, self.orientation_in_entity)
        leg_polygon = translate_polygon(leg_polygon, self.get_position_relative_to_center_of_gravity())
        leg_polygon = rotate_polygon(leg_polygon, self.entity.orientation)
        leg_polygon = translate_polygon(leg_polygon, self.entity.position_of_center_of_gravity)
        leg_polygon = simulator.polygon_from_physical(leg_polygon)
        pygame.draw.polygon(simulator.window, color=(0, 0, 0), points=make_pairs(leg_polygon))



class RocketBody(ComponentBase):
    def __init__(self, entity, position_in_entity, orientation_in_entity=0,
                 mass=1, moment_of_inertia=0,
                 height=10, diameter=2, rel_height_pressure_center=0.3,
                 lift_coeff=0.5, drag_coeff=0.5, lift_area=1, drag_area=1,
                 color=(255, 0, 0)):
        super().__init__(entity, position_in_entity, orientation_in_entity,
                         input_functions=[],
                         mass=mass, moment_of_inertia=moment_of_inertia,
                         bounding_radius=None)
        self.height = height
        self.diameter = diameter
        self.rel_height_pressure_center = rel_height_pressure_center
        self.lift_coeff = lift_coeff
        self.drag_coeff = drag_coeff
        self.lift_area = lift_area
        self.drag_area = drag_area
        self.induced_forces = [Vector()]
        self.color = color

        # self.bounding_radius = 2

    def _compute_aerodynamic_forces(self, wind_in_global):
        if wind_in_global.norm() > 0:
            relative_wind = (wind_in_global - self.get_global_velocity()).rotate(-self.entity.orientation).rotate(-self.orientation_in_entity)
        else:
            relative_wind = Vector()
        lift = self.lift_coeff * relative_wind[0] * self.lift_area
        drag = self.drag_coeff * relative_wind[1] * self.drag_area
        return Vector(lift, drag).rotate(self.orientation_in_entity).rotate(self.entity.orientation)

    def draw(self, simulator):
        rocket_polygon = [Vector(-self.diameter, 0),
                          Vector(-self.diameter/2, self.diameter),
                          Vector(-self.diameter/2, (self.height - self.diameter)),
                          Vector(0, self.height),
                          Vector(self.diameter/2, (self.height - self.diameter)),
                          Vector(self.diameter/2, self.diameter),
                          Vector(self.diameter, 0)]
        rocket_polygon = translate_polygon(rocket_polygon, Vector(0, -self.height * self.rel_height_pressure_center))
        rocket_polygon = rotate_polygon(rocket_polygon, self.orientation_in_entity)
        rocket_polygon = translate_polygon(rocket_polygon, self.get_position_relative_to_center_of_gravity())
        rocket_polygon = rotate_polygon(rocket_polygon, self.entity.orientation)
        rocket_polygon = translate_polygon(rocket_polygon, self.entity.position_of_center_of_gravity)
        rocket_polygon = simulator.polygon_from_physical(rocket_polygon)
        pygame.draw.polygon(simulator.window, color=self.color, points=make_pairs(rocket_polygon))
        # pygame.draw.circle(simulator, (0, 0, 0),
        #                    self.entity.position_of_center_of_gravity * simulator.scale
        #                    + (1-self.rel_height_pressure_center) * self.)

class Thruster(ComponentBase):
    def __init__(self, entity, position_in_entity, orientation_in_entity, input_functions=[], mass=1, max_thrust=1):
        super().__init__(entity, position_in_entity, orientation_in_entity,
                         input_functions=input_functions,
                         mass=mass, moment_of_inertia=0,
                         bounding_radius=None)
        self.max_thrust = max_thrust
        self.original_angle = orientation_in_entity
        self.throttle = 0
        
    def _compute_control_inputs(self):
        if len(self.input_functions) > 0:
            self.throttle = self.input_functions[0]()
            self.propulsion_forces.append(Vector(0, self.throttle * self.max_thrust).rotate(self.orientation_in_entity).rotate(self.entity.orientation))
        if len(self.input_functions) > 1:
            self.orientation_in_entity = self.original_angle + self.input_functions[1]()

    def draw(self, simulator):
        thruster_polygon = [Vector(0, 0), Vector(0.6, -0.5), Vector(1, -1), Vector(-1, -1), Vector(-0.6, -0.5)]
        flame_polygon = [Vector(-0.5, -1), Vector(0, -1 - self.throttle * self.max_thrust / 10), Vector(0.5, -1)]
        thruster_polygon = scale_polygon(thruster_polygon, self.max_thrust/200)
        flame_polygon = scale_polygon(flame_polygon, self.max_thrust/200)
        thruster_polygon = rotate_polygon(thruster_polygon, self.orientation_in_entity)
        flame_polygon = rotate_polygon(flame_polygon, self.orientation_in_entity)
        thruster_polygon = translate_polygon(thruster_polygon, self.get_position_relative_to_center_of_gravity())
        flame_polygon = translate_polygon(flame_polygon, self.get_position_relative_to_center_of_gravity())
        thruster_polygon = rotate_polygon(thruster_polygon, self.entity.orientation)
        flame_polygon = rotate_polygon(flame_polygon, self.entity.orientation)
        thruster_polygon = translate_polygon(thruster_polygon, self.entity.position_of_center_of_gravity)
        flame_polygon = translate_polygon(flame_polygon, self.entity.position_of_center_of_gravity)
        thruster_polygon = simulator.polygon_from_physical(thruster_polygon)
        flame_polygon = simulator.polygon_from_physical(flame_polygon)
        pygame.draw.polygon(simulator.window, color=(100, 100, 100), points=make_pairs(thruster_polygon))
        pygame.draw.polygon(simulator.window, color=(255, 136, 0), points=make_pairs(flame_polygon))

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