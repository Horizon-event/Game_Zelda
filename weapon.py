import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        # направление
        direction = player.status.split('_')[0]  # метод сплит отделяет все после '_' и возвращает первую часть


        # графика оружия
        full_path = f'Load/5 - level graphics/graphics/weapons/{player.weapon}/{direction}.png'
        # self.image = pygame.Surface((40, 40)) отрисовывается прямоугольный квадрат
        self.image = pygame.image.load(full_path).convert_alpha()

        # размещение оружия на карте
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 16))
        else:
            self.rect = self.image.get_rect(center=player.rect.center)
