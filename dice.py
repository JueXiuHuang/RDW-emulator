import pygame as pyg
# import numpy as np

class Dice():
  # class attribute
  surface = None
  
  @classmethod
  def set_surface(cls, surface):
    cls.surface = surface
  
  def __init__(self, image, posx, posy, width, height):
    self.posx = posx
    self.posy = posy
    self.width = width
    self.height = height
    self.rect = pyg.Rect(posx, posy, width, height)
    self.star = 0
    
    self.set_content(image)
  
  def draw_content(self):
    image_rect = self.content.get_rect(center = self.rect.center)
    Dice.surface.blit(self.content, image_rect)
  
  def draw(self):
    self.draw_content()
    pyg.draw.rect(Dice.surface, pyg.Color("white"), self.rect, 1)
  
  def set_content(self, new_content):
    self.content = new_content
  
  def skill(self, **kwargs):
    return
  
  def merge(self):
    return


class NormalDice(Dice):
  def __init__(self, image, posx, posy, width, height):
    super().__init__(image, posx, posy, width, height)
    self.set_content(image)


class JokerDice(Dice):
  def __init__(self, image, posx, posy, width, height):
    super().__init__(image, posx, posy, width, height)
  
  def skill(self, **kwargs):
    changeTo = kwargs['changeTo']
    imageList = kwargs['imageList']
    
    return