import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('Load/5 - level graphics/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # уменьшает значение персонажа сверху и снизу по y
        self.direction = pygame.math.Vector2()  # определяется позиция игрока (начальная)
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        # управление клавишами
        if keys[pygame.K_UP]:
            self.direction.y = - 1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = - 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:  # нормализация движения во все стороны и по диагонали (без по диагонали быстрее)
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')  # ограничение персонажа по горизонтали
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')  # ограничение персонажа по вертикали
        self.rect.center = self.hitbox.center

        # self.rect.center += self.direction * speed

    # функция для контрорля ударений о стену
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # движение справа
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # движение слева
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # движение вниз
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # движение вверх
                        self.hitbox.top = sprite.hitbox.bottom

    # обновление экрана, иначе двигаться не будет.
    def update(self):
        self.input()
        self.move(self.speed)
