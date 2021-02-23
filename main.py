from simulator import Simulator
from entity_library import *
from component_library import *

# TODO: first, do rockets only, implement aerodynamics a bit later with athmosphere




if __name__ == '__main__':
    WINDOW_HEIGHT = 480
    WINDOW_WIDTH = 640

    s = Simulator(window_size=(WINDOW_WIDTH, WINDOW_HEIGHT), scale_init=0.01)
    s.camera_center = Vector(0, 0)
    s.add_entity(Planet(position_init=Vector(0, 0), radius=1000, density=5500, color=(0, 255, 0),
                        athmosphere_radius=7000, athmosphere_density=1, athmosphere_color=(100, 100, 255)))
    # s.add_entity(Planet(position_init=Vector(0, 6600), radius=1, density=1000, color=(255, 0, 0)))

    s.run()
