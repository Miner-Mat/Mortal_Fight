import pygame
from animations import anim_fight, anim_stay, anim_run
from constants_for_hero import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, *groups, direction='right'):
        super().__init__(*groups)
        self.anim_stay = anim_stay
        self.anim_stay_l = [pygame.transform.flip(el, True, False) for el in anim_stay]
        self.anim_fight = anim_fight
        self.anim_fight_l = [pygame.transform.flip(el, True, False) for el in anim_fight]
        self.anim_run = anim_run
        self.anim_run_l = [pygame.transform.flip(el, True, False) for el in anim_run]

        self.cur_frame_stay = 0
        self.cur_frame_fight = 0
        self.cur_frame_run = 0

        self.image = self.anim_stay[self.cur_frame_stay]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.is_stay = True
        self.is_run = False
        self.is_fight = False
        self.is_jump = False
        self.is_squat = False

        if direction == 'left':
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True

        self.speed = speed

        self.clock = pygame.time.Clock()

    def frame_swap(self):
        self.cur_frame_stay = (self.cur_frame_stay + 1) % len(self.anim_stay)
        self.cur_frame_run = (self.cur_frame_run + 1) % len(self.anim_run)
        if self.is_fight:
            self.cur_frame_fight += 1
            if self.cur_frame_fight == len(self.anim_fight):
                self.cur_frame_fight = 0
                self.is_fight = False

    def image_swap(self):
        if self.is_fight:
            self.image = self.anim_fight[self.cur_frame_fight]
        elif self.is_jump:
            pass
        elif self.is_squat:
            pass
        elif self.is_stay:
            self.image = self.anim_stay[self.cur_frame_stay]
        elif self.is_run:
            self.image = self.anim_run[self.cur_frame_run]

    def process_events(self, flags):
        if STAY in flags:
            self.is_stay = True
        else:
            self.is_stay = False

        if RUN in flags:
            self.is_run = True
        else:
            self.is_run = False

        # далее непрерываемые процессы
        if JUMP in flags:
            self.is_jump = True

        if SQUAT in flags:
            self.is_squat = True

        if FIGHT in flags:
            self.is_fight = True

        # направления
        if LEFT in flags:
            self.left = True
            self.right = False

        if RIGHT in flags:
            self.left = False
            self.right = True

    def move(self):
        t = self.clock.tick()
        if self.is_run:
            if self.left:
                self.rect = self.rect.move(self.speed * t / 1000, 0)
            else:
                self.rect = self.rect.move(-self.speed * t / 1000, 0)