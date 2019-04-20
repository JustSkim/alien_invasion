# -*- coding: utf-8 -*-


#创建外星人
import pygame
from pygame.sprite import Sprite
from pygame import font
import time
from time import sleep
import sys

class Alien(Sprite):
    '''表示单个外星人的类'''
    
    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置其起始位置'''
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像,并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
        
    def blitme(self):
        '''在指定位置绘制外星人'''
        self.screen.blit(self.image,self.rect)
        
    def check_edges(self):
        '''如果外星人位于屏幕边缘,就返回True'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
        
    def update(self):
        '''向左或向右移动外星人'''
        self.x += (self.ai_settings.alien_speed_factor * 
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

class Bullet(Sprite):
    '''一个对飞船发射的子弹进行管理的类'''
    
    def __init__(self,ai_settings,screen,ship):
        '''在飞船所处的位置创建一个子弹对象'''
        super(Bullet,self).__init__()
        self.screen = screen
        
        #在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        '''向上移动子弹'''
        #更新表示子弹位置的小数值
        self.y -= self.speed_factor
        #更新表示子弹的rect的位置
        self.rect.y = self.y
        
    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen,self.color,self.rect)

#创建一个play按钮
class Button():
    def __init__(self,ai_settings,screen,msg):
        '''初始化按钮的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        #设置按钮的尺寸和其他属性
        self.width,self.height = 200,50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)
        
        #创建按钮的rect对象,并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        
        #按钮的标签只需创建一次
        self.prep_msg(msg)
        
    def prep_msg(self,msg):
        '''将msg渲染为图像，并使其在按钮上居中'''
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
        
        		
		
		
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
    
    #创建一个用于存储游戏统计信息的实力
    stats = GameStats(ai_settings)
    
    pygame.display.set_caption("Alien Invasion")
    
    #创建play按钮
    play_button = Button(ai_settings,screen,'Play')
    
    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button)
        
run_game()
#运行该Alien game


#跟踪游戏统计信息
class GameStats():
    '''跟踪游戏的统计信息'''
    def __init__(self,ai_settings):
        '''初始化统计信息'''
        self.ai_settings = ai_settings
        self.reset_stats()
        
        #游戏刚启动时处于非活动状态
        self.game_active = False
        
    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left = self.ai_settings.ship_limit


		
class Settings():
    '''存储《外星人入侵》的所有设置的类'''
    def __init__(self):
        '''初始化游戏的设置'''
        #屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230,230,230)
        # 设置背景色 三位数字从左到右分别为R（红）G（绿）B(蓝)值
        
        #飞船的设置
        self.ship_speed_factor = 1.5
        #每次移动1.5像素
        self.ship_limit = 3
        
        #子弹设置
        self.bullet_speed_factor = 3
        #python性能可能拖慢子弹速度，因此需适当调快
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        #限制出现在屏幕中的子弹数量
        self.bullets_allowed = 3
        
        #外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        #fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1		



class Ship():
    def __init__(self,ai_settings,screen):
        '''初始化飞船并设置其初始位置'''
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #将每一艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #在飞船的属性center中存储小数值
        #注意，rect的centerx等属性只能存储整数值
        self.center = float(self.rect.centerx)
        
        #移动标志
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        '''根据移动标志调整飞船的位置'''
        #更新飞船的center值，而不是rect
        #防止飞船跑到屏幕外边缘
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        #根据self.center更新rect对象
        self.rect.centerx = self.center
        
    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)
        
    def center_ship(self):
        '''让飞船在屏幕上居中'''
        self.center = self.screen_rect.centerx
        
        
        		

		

#下面的是来自game_function.py的函数


def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹,并将其加入到编组bullets中
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)    
    #按Q键来关闭游戏    
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    '''响应松开,不如此设置会导致松开按键后飞船仍在移动'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False



def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
                            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,
                              aliens,bullets,mouse_x,mouse_y)

      
def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    '''玩家单击Play按钮时开始游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        if play_button.rect.collidepoint(mouse_x,mouse_y):
            stats.game_active = True
        
def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button):
    '''更新屏幕上的图像,并切换到新屏幕
       每次循环是都重新绘制屏幕'''
    screen.fill(ai_settings.bg_color)  
    #在飞船和外星人后面重新绘制所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    
    #让最近绘制的屏幕可见
    pygame.display.flip()  
    

def update_bullets(ai_settings,screen,ship,aliens,bullets):
    '''更新子弹的位置，并删除已经消失的子弹'''
    #更新子弹的位置
    bullets.update()
    
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #检查是否有子弹击中了外星人，若有则删除相应的子弹和外星人
    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)
    
def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
    '''响应子弹和外星人的碰撞'''
    #删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    if len(aliens) == 0:
        #删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)


def fire_bullet(ai_settings,screen,ship,bullets):
    '''如果还没有到达限制，就发射一颗子弹'''
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullets)


def get_number_aliens_x(ai_settings,alien_width):
    '''计算每行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width -2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
              #使用int👆确保外星人数量为整数
    return number_aliens_x


def get_number_rows(ai_settings,ship_height,alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - 
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
    
def create_fleet(ai_settings,screen,ship,aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,
                                  alien.rect.height)
    
    #创建外星人群
    for row_number in range(number_rows):
       for alien_number in range(number_aliens_x):
           create_alien(ai_settings,screen,aliens,alien_number,
                        row_number)
    
def check_fleet_edges(ai_settings,aliens):
    '''有外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人向下移动,并改变它们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    #利用 1*1=-1，-1²=1
    
    
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    #将ships_left减去1
    stats.ships_left -= 1
    if stats.ships_left > 0:
        #将ships_left减去1
        stats.ships_left -= 1
        
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
    
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
    
        #暂停一会儿
        sleep(0.5)
    else:#如果玩家没有飞船了
        stats.game_active = False
        pygame.mouse.set_visible(True)
        

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break
    
    
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):

#👆上面的是game_function.py的函数



