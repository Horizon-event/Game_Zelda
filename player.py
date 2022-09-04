import pygame
from settings import *
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('Load/5 - level graphics/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # уменьшает значение персонажа сверху и снизу по y
        self.direction = pygame.math.Vector2()  # определяется позиция игрока (начальная)

        # установка графики героя
        self.import_player_assets()

        # вид героя на карте
        self.status = 'down'
        self.frame_index = 0  # индекс положения игрока
        self.animation_speed = 0.15

        self.attacking = False  # начальное положение атаки
        self.attack_cooldown = 400  # задержка по времени между атаками
        self.attack_time = None  # начальное время атаки
        self.obstacle_sprites = obstacle_sprites

        # оружие
        self.create_attack = create_attack  # создание атаки
        self.destroy_attack = destroy_attack  # разрушение оружия на Экране
        self.weapon_index = 0
        # превращаем в список для возможности индексации оружия в руках игрока
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        # переключение оружия при нажатии на клавишу q
        self.can_switch_weapon = True
        self.weapon_switch_time = None  # отсчет времени для задержки
        self.switch_duration_cooldown = 200  # задержка нажатия кнопки при переключении (без нее несколько оружия)

        # статистика / интерфейс
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}  # начальная статистика
        self.health = self.stats['health'] *0.5 # текущая статистика
        self.energy = self.stats['energy']  # текущая статистика
        self.exp = 123  # текущая статистика
        self.speed = self.stats['speed']  # текущая статистика

    def import_player_assets(self):
        character_path = 'Load/5 - level graphics/graphics/player/'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': [],
        }
        # функция записывает пути к ключам словаря
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            # управление клавишами движение
            if keys[pygame.K_UP]:
                self.direction.y = - 1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = - 1
                self.status = 'left'
            else:
                self.direction.x = 0

            # атака
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # магия
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

            # выбор оружия по клавише q
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

    # функция, определяющая положение героя (его анимацию) при движении и атаки
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack', '')

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

    # функция задержки времени при атаке
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False  # меняет флажок на False, что дает возможность атаковать еще раз
                self.destroy_attack()
        # для постоянной возможности смены оружия
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index - цикл по индексу кадра
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # установка изображения
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    # обновление экрана, иначе двигаться не будет.
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
