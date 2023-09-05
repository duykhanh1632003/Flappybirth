import pygame
import sys
import time
from settings import *
from sprites import BG, GROUND, Plane, Obstacle


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        # Initialize game-related variables
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        bg_height = pygame.image.load(
            'Graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # Create game objects
        BG(self.all_sprites, self.scale_factor)
        GROUND([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Initialize font for the score
        self.font = pygame.font.Font('Graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) \
                or self.plane.rect.top <= 0:
            pygame.quit()
            sys.exit()

    def display_score(self):
        self.score = pygame.time.get_ticks() // 1000  # Convert milliseconds to seconds
        score_surf = self.font.render(f'Score: {self.score}', True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.plane.jump()
                if event.type == self.obstacle_timer:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            dt = time.time() - last_time
            last_time = time.time()

            self.display_surface.fill('black')
            self.display_score()
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.collisions()
            pygame.display.flip()
            self.clock.tick(FRAMERATE)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
