import pygame
import numpy as np
from vector import Vector

class Simulator:
    def __init__(self, window_size=(100, 100), scale_init: float = 1):
        self.entities = []
        self.camera_center = Vector()
        self.window_size = window_size
        self.scale_min = 1
        self.scale_max = 1000
        self.scale = scale_init
        self.auto_scale = False
        self.tracked_entity = None

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('a_theme_for_space.mp3')

    def track(self, entity):
        self.tracked_entity = entity

    def add_entity(self, entity):
        self.entities.append(entity)

    def position_from_physical(self, vec: Vector):
        return (vec - self.camera_center) * self.scale + Vector(self.window_size[0], self.window_size[1]) / 2

    def polygon_from_physical(self, pts: []):
        return [self.position_from_physical(pt) for pt in pts]

    def zoom_in(self, factor=1.2):
        if self.scale < self.scale_max:
            self.scale *= factor

    def zoom_out(self, factor=1.2):
        if self.scale > self.scale_min:
            self.scale /= factor


    def run(self, fps=60):
        # pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely.
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.window = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
        clock = pygame.time.Clock()
        running = True
        while running:
            time_step = clock.tick(fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_PERIOD] or self.joystick.get_button(4):
                self.zoom_out()

            if keys[pygame.K_COMMA] or self.joystick.get_button(9):
                self.zoom_in()

            if keys[pygame.K_a]:
                self.auto_scale = True

            if keys[pygame.K_m]:
                self.auto_scale = False

            if keys[pygame.K_UP]:
                self.camera_center -= Vector(0, 1) / self.scale * 5

            if keys[pygame.K_DOWN]:
                self.camera_center += Vector(0, 1) / self.scale * 5

            if keys[pygame.K_LEFT]:
                self.camera_center -= Vector(1, 0) / self.scale * 5

            if keys[pygame.K_RIGHT]:
                self.camera_center += Vector(1, 0) / self.scale * 5

            if self.tracked_entity:
                self.camera_center = self.tracked_entity.position_of_center_of_gravity
                if self.auto_scale:
                    self.scale = min(self.scale_max / self.tracked_entity.velocity.norm()/10, self.scale_max/10)
                if self.tracked_entity.is_crashed:
                    pygame.font.init()  # you have to call this at the start,
                    # if you want to use this module.
                    myfont = pygame.font.SysFont('calibri', 50)
                    textsurface = myfont.render('You Crashed!', False, (50, 50, 50))
                    self.window.blit(textsurface, (self.window_size[0]/2-150, self.window_size[1]/6))
                    pygame.display.update()

                    pass

            self.window.fill((0, 0, 0))
            for entity in self.entities:
                # position_in_pygame = self.position_from_physical(entity.position_of_center_of_gravity)
                # if (self.camera_center - position_in_pygame).norm() < 2 * max(self.window_size):
                entity.update_and_draw(self, time_step)
            pygame.draw.circle(self.window, (255, 120, 0),
                               self.position_from_physical(Vector()).get(),
                               self.scale * 0.05)
            pygame.display.update()
