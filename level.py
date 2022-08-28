import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # создание групп видимых и невидимых элементов карты
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        # старая карта
        # for row_index, row in enumerate(WORLD_MAP):  # enumerate - счетчик элементов
        #     for col_index, col in enumerate(row):
        #         x = col_index * TILESIZE  # преобразовали карту мира в положение...
        #         y = row_index * TILESIZE
        #         if col == 'x':
        #             Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
        #         if col == 'p':
        #             self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
        self.player = Player((2000, 1440), [self.visible_sprites], self.obstacles_sprites)
    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)  # отображение значений на экране
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    # класс определяет движение камеры, а не персонажа
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(0, 0)  # смещает начало экрана

        # создание уровней
        self.floor_surf = pygame.image.load('Load/5 - level graphics/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width  # определяем координаты персонажа по центру
        self.offset.y = player.rect.centery - self.half_height  # определяем координаты персонажа по центру

        # отрисовка уровня
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)  # отрисовка элементов
