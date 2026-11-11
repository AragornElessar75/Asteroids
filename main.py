import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    asteroids = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()

    Asteroid.containers = (asteroids, drawable, updatable)
    AsteroidField.containers = updatable
    Player.containers = (drawable, updatable)
    Shot.containers = (drawable, shots, updatable)

    AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def check_collisions(player, asteroids, shots):
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                return False
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    break
        return True

    running = True
    while running:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        running = check_collisions(player, asteroids, shots)
        for drawable_obj in drawable:
            drawable_obj.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
