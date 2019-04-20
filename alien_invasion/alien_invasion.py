# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:37:52 2019

@author: longwen
"""
#外星人入侵  P112

import pygame
import alien
from alien import Alien
from pygame.sprite import Group
from settings import Settings
#引用另一个自定义settings.py文件中的Settings类
from ship import Ship #同理
import game_functions as gf
#无需直接导入sys，因为当前只在模块game_functions中使用了它
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    '''开始游戏项目的第一个函数！
    创建Pygame窗口以及响应用户输入'''
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    screen = pygame.display.set_mode(
    (ai_settings.screen_width,ai_settings.screen_height))
    #注意此处，传进去的代表屏幕宽高的必须是一个👆含两个参数的元组(tuple)
    pygame.display.set_caption('Alien Invasion')
    
    #创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #注意！不可在循环内部创建这样的编组，会严重拖慢进程
    #创建一个外星人编组
    aliens = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    
    #创建储存游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    
    pygame.display.set_caption("Alien Invasion")
    
    #创建play按钮
    play_button = Button(ai_settings,screen,'Play')
    
    
    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
        
run_game()
#运行该函数
