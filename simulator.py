import pygame
from vector import Vector


class Simulator:
    def __init__(self, window_size=(100, 100), scale_init: float = 1):
        self.entities = []
        self.camera_center = Vector()
        self.window_size = window_size
        self.scale = scale_init

    def add_entity(self, entity):
        self.entities.append(entity)

    def position_from_physical(self, vec: Vector):
        return (vec - self.camera_center) * self.scale + Vector(self.window_size[0], self.window_size[1]) / 2

    def polygon_from_physical(self, pts: []):
        return [self.position_from_physical(pt) for pt in pts]

    def run(self):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.window = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
        clock = pygame.time.Clock()
        running = True
        while running:
            time_step = clock.tick(20) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_PERIOD]:
                self.scale *= 1.2

            if keys[pygame.K_COMMA]:
                self.scale /= 1.2

            if keys[pygame.K_UP]:
                self.camera_center -= Vector(0, 1) / self.scale * 5

            if keys[pygame.K_DOWN]:
                self.camera_center += Vector(0, 1) / self.scale * 5

            if keys[pygame.K_LEFT]:
                self.camera_center -= Vector(1, 0) / self.scale * 5

            if keys[pygame.K_RIGHT]:
                self.camera_center += Vector(1, 0) / self.scale * 5

            self.window.fill((0, 0, 0))
            for entity in self.entities:
                entity.update_and_draw(self, time_step)
            pygame.display.update()