from simulator import Simulator
from entity_library import *
from component_library import *

# TODO: first, do rockets only, implement aerodynamics a bit later with athmosphere

if '__main__' == __name__:

    WINDOW_HEIGHT = 1300
    WINDOW_WIDTH = 2000

    s = Simulator(window_size=(WINDOW_WIDTH, WINDOW_HEIGHT), scale_init=100)
    s.camera_center = Vector(0, 0)

    s.add_entity(Planet(position_init=Vector(0, -300), radius=50, density=200, color=(0, 100, 255),
                        athmosphere_radius=100, athmosphere_density=1, athmosphere_color=(150, 180, 255), max_wind=0))
    s.add_entity(Planet(position_init=Vector(0, 100), radius=100, density=100, color=(0, 255, 0),
                        athmosphere_radius=200, athmosphere_density=1, athmosphere_color=(100, 100, 255), max_wind=0))
    s.add_entity(rocket := Rocket(position_init=Vector(0, -3), orientation_init=np.pi,
                                  mass=100, max_thrust=250, max_thrust_thrusters=100,
                                  height=2, diameter=0.3, rel_height_pressure_center=0.2,
                                  throttle_fn=lambda: -1 * (s.joystick.get_axis(3) - 1) / 2,
                                  vector_fn=lambda: -s.joystick.get_axis(0) + rocket.velocity_angular,
                                  thruster_left_fn=lambda: s.joystick.get_button(2),
                                  thruster_right_fn=lambda: s.joystick.get_button(3)))

    s.track(rocket)
    s.run(60)
