from simulator import Simulator
from entity_library import *
from component_library import *

# TODO: first, do rockets only, implement aerodynamics a bit later with athmosphere




if __name__ == '__main__':
    WINDOW_HEIGHT = 1300
    WINDOW_WIDTH = 2000

    s = Simulator(window_size=(WINDOW_WIDTH, WINDOW_HEIGHT), scale_init=10)
    s.camera_center = Vector(0, 0)
    s.add_entity(Planet(position_init=Vector(0, 555), radius=500, density=5, color=(0, 255, 0),
                        athmosphere_radius=550, athmosphere_density=1, athmosphere_color=(100, 100, 255), max_wind=100))
    # s.add_entity(Planet(position_init=Vector(0, 6600), radius=1, density=1000, color=(255, 0, 0)))
    s.add_entity(rocket:=Rocket(position_init=Vector(0, 0), orientation_init=0,
                        mass=10, max_thrust=50,
                        height=2, diameter=0.3, rel_height_pressure_center=0.2,
                        throttle_fn=lambda: -1 * (s.joystick.get_axis(3) - 1) / 2, vector_fn=lambda:-s.joystick.get_axis(0)))
    s.track(rocket)
    s.run()
