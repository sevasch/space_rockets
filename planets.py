import numpy as np
# import pygame module in this program
import pygame
import matplotlib.pyplot as plt


def draw_planet(radius, base_color=(183, 65, 14), texture = 0.1):
    base_planet = np.ones((2 * radius, 2 * radius, 3)) * base_color / 255 \
                  + texture * (np.random.random((2 * radius, 2 * radius, 3)) - 0.5)
    for i in range(base_planet.shape[0]):
        for j in range(base_planet.shape[1]):
            if np.sqrt((i-radius)**2 + (j-radius)**2) > base_planet.shape[0] / 2:
                base_planet[i, j] = (0, 0, 0)

    return base_planet * 255


if __name__ == '__main__':
    pygame.init()

    planet = draw_planet(150)
    # plt.imshow(planet), plt.show()
    white = (255, 255, 255)

    X = 1000
    Y = 1000

    display_surface = pygame.display.set_mode((X, Y))
    surf = pygame.surfarray.make_surface(planet)
    surf = pygame.transform.scale(surf, (150//2, 150//2))

    pygame.display.set_caption('Image')
    while True:
        display_surface.fill(white)
        display_surface.blit(surf, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

                quit()

            pygame.display.update()