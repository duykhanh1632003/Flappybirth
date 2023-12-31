import pygame
from settings import *
from random import choice , randint

class BG(pygame.sprite.Sprite):
	
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.bg_image = pygame.image.load('Graphics/environment/background.png').convert()
        full_height = self.bg_image.get_height() * scale_factor
        full_width = self.bg_image.get_width() * scale_factor
        
        # Scale the background image to fit the game window
        self.full_sized_image = pygame.transform.scale(self.bg_image, (full_width, full_height))
        self.image = pygame.Surface((full_width * 2, full_height))
        
        # Create two instances of the full-sized image side by side for scrolling
        self.image.blit(self.full_sized_image, (0, 0))
        self.image.blit(self.full_sized_image, (full_width, 0))
        
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.pos.x <= -self.rect.width / 2:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
class GROUND(pygame.sprite.Sprite):
    def __init__(self, groups , scale_factor):
        super().__init__(groups)
        self.ground_surf = pygame.image.load('Graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.ground_surf,pygame.math.Vector2(self.ground_surf.get_size()) * scale_factor) 
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)
    def update(self,dt):
        self.pos.x -=  360*dt
        if self.rect.centerx <= 0:
            self.pos.x= 0
        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self,groups, scale_factor):
        super().__init__(groups)

        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/20,WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.gravity = 600
        self.direction = 0


    def import_frames(self,scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(f'Graphics/plane/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)
    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
    def jump(self):
        self.direction =  -400
    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction *0.06, 1)
        self.image =  rotated_plane

    
    def update(self,dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups,scale_factor):
        super().__init__(groups)

        orientation = choice(('up','down'))
        surf = pygame.image.load(f'Graphics/obstacles/{choice((0,1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)

        x = WINDOW_WIDTH + randint(40,100)

        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10,50)
            self.rect = self.image.get_rect(midbottom = (x,y))
        else:
            y = randint(-50,-10)
            self.image = pygame.transform.flip(self.image,False, True)
            self.rect  = self.image.get_rect(midtop = (x,y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.pos = pygame.math.Vector2(self.rect.topleft)
    def update(self,dt):
        self.pos.x -= 400 *dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()


             
