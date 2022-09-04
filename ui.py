import pygame
from settings import *


class UI:
    def __init__(self):
        # основное
        self.display_surface = pygame.display.get_surface()  # создаем поверхность
        self.font = pygame.font.Font(UI_FRONT, UI_FONT_SIZE)  # создаем тип и размер шрифта

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)  # 10, 10 начальные значения
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    # простой вариант отрисовки
    # def display(self, player):
    #     # pygame.draw.rect(surface, color, rect) # что должно быть
    #     pygame.draw.rect(self.display_surface, HEALTH_COLOR, self.health_bar_rect, 0, 5)
    #     pygame.draw.rect(self.display_surface, ENERGY_COLOR, self.energy_bar_rect, 0, 5)

    # другой вариант
    def show_bar(self, current, max_amount, bg_rect, color):
        # отрисовка на экране фон черный!
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # количество жизни
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # отрисовка жизни фон под цвет
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    # отрисовка опыта
    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20  # положение текста по Х со смещением 20
        y = self.display_surface.get_size()[1] - 20  # положение текста по У со смещением 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))  # отрисовка фона на text_rect (exp), inflate - раздуть на 20

        self.display_surface.blit(text_surf, text_rect)  # отрисовка текста exp
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)  # отрисовка ободка

    # отрисовка оружия
    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    # отрисовка оружия в окне
    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)  # выводим на экран показания оружия
        weapon_surf = self.weapon_graphics[weapon_index]  # получение индекса оружия
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)  # место отрисовки оружия
        self.display_surface.blit(weapon_surf, weapon_rect)  # отрисовка оружия

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)  # выводим на экран показания опыта

        self.weapon_overlay(player.weapon_index,
                            not player.can_switch_weapon)  # not позволяет не отрисовывать обод на постоянной основе, тольбко при выборе оружия

        # self.selection_box(85, 635)  # выводим на экран показания магии
