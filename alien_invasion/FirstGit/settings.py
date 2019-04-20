# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:55:49 2019

@author: JustSkim
"""

class Settings():
    '''存储《外星人入侵》的所有设置的类'''
    def __init__(self):
        '''初始化游戏的设置'''
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        # 设置背景色 三位数字从左到右分别为R（红）G（绿）B(蓝)值
        
        #飞船的设置
        #每次移动1.5像素
        self.ship_limit = 3
        
        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        #限制出现在屏幕中的子弹数量
        self.bullets_allowed = 3
        
        #外星人设置
        self.fleet_drop_speed = 10

        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #外星人点数的提高速度
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        #python性能可能拖慢子弹速度，因此需适当调快
        self.alien_speed_factor = 1
        
        #fleet_direction为1代表向右，为-1代表向左
        self.fleet_direction = 1
        
        #记分
        self.alien_points = 50
        
    def increase_speed(self):
        '''提高速度设置'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        #玩家每提高一个等级,提高各类速度
        
        self.alien_points = int(self.alien_points * self.score_scale)
        
        print(self.alien_points)
        #便于在控制台确认点数不断增加
        
        