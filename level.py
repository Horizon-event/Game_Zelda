import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # создание групп видимых и невидимых элементов карты
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        # переменная для уничтожения оружия
        self.current_attack = None

        self.create_map()

        # пользовательский интерфейс
        self.ui = UI()

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
        # print(graphics)
        layouts = {
            'boundary': import_csv_layout('Load/5 - level graphics/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('Load/5 - level graphics/map/map_Grass.csv'),
            'object': import_csv_layout('Load/5 - level graphics/map/map_Objects.csv'),
        }

        graphics = {
            'grass': import_folder('Load/5 - level graphics/graphics/grass'),
            'object': import_folder('Load/5 - level graphics/graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):  # enumerate - счетчик элементов
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE  # преобразовали карту мира в положение...
                        y = row_index * TILESIZE
                        # отрисовываем разные уровни
                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['object'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', surf)

        self.player = Player((2000, 1440), [self.visible_sprites], self.obstacles_sprites, self.create_attack,
                             self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    # уничтожение оружия с экрана после атаки
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)  # отображение значений на экране
        self.visible_sprites.update()
        # debug(self.player.status) # отображение значений, в которых сомневаемся
        self.ui.display(self.player)


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
