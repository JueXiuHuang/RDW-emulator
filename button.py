import pygame as pyg
import numpy as np

from board import *

class Button():
  # class attribute
  surface = None
  
  @classmethod
  def set_surface(cls, surface):
    cls.surface = surface
  
  def __init__(self, image, x, y, width, height, normal_color=None, pressing_color=None):
    self.color = normal_color
    self.pressing_color = pressing_color
    self.normal_color = normal_color
    self.image = image
    self.rect = pyg.Rect(x, y, width, height)
    self.img_rect = self.image.get_rect(center=self.rect.center)
    
    self.pressed = False
  
  def draw(self):
    pyg.draw.rect(Button.surface, self.color, self.rect, border_radius=5)
    Button.surface.blit(self.image, self.img_rect)
  
  def click(self):
    return
  
  def color_change(self, color):
    self.color = color
  
  def check_click(self, mouse_pos):
    if self.rect.collidepoint(mouse_pos):
      # mouse left pressed
      if pyg.mouse.get_pressed()[0]:
        self.pressed = True
        if self.pressing_color != None:
          self.color_change(self.pressing_color)
        return False
      else:
        if self.pressed:
          self.pressed = False
          self.color_change(self.normal_color)
          
          # execute click method when return true
          return True
    else:
      if self.pressed:
        self.pressed = False
      self.color_change(self.normal_color)
      return False

class SummonBtn(Button):
  def __init__(self, image, x, y, width, height):
    super().__init__(image, x, y, width, height, pyg.Color(255, 209, 26), pyg.Color(255, 170, 0))
  
  def click(self):
    print('Summon new dice...')
    Board.summon_dice()
    
class ResetBtn(Button):
  def __init__(self, image, x, y, width, height):
    super().__init__(image, x, y, width, height, pyg.Color(0, 230, 77))
  
  def click(self):
    print('Reset the game...')
    Board.reset_game()

class LvlUpBtn(Button):
  def __init__(self, image, x, y, width, height):
    super().__init__(image, x, y, width, height, pyg.Color(0, 230, 77))