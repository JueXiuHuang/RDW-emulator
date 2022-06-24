import pygame as pyg
# import numpy as np

class Dice():
  # class attribute
  surface = None
  
  @classmethod
  def set_surface(cls, surface):
    cls.surface = surface
  
  def __init__(self, image, dice_type, posx, posy, width, height, draggable):
    self.original_x = posx
    self.original_y = posy
    self.width = width
    self.height = height
    self.rect = pyg.Rect(posx, posy, width, height)
    self.dice_type = dice_type
    self.dice_star = 0
    self.is_drag = False
    self.draggable = draggable
    
    self.set_content(image)
  
  def draw_content(self):
    image_rect = self.content.get_rect(center = self.rect.center)
    Dice.surface.blit(self.content, image_rect)
  
  def draw(self):
    self.draw_content()
    pyg.draw.rect(Dice.surface, pyg.Color("white"), self.rect, 1)

  def is_dice_select(self, mouse_pos):
    if self.rect.collidepoint(mouse_pos) and self.draggable:
      self.is_drag = True
    else:
      self.is_drag = False

  def reset_dice_loc(self):
    self.rect.x = self.original_x
    self.rect.y = self.original_y
    self.is_drag = False
  
  def update_loc(self, mouse_pos):
    rel_x, rel_y = mouse_pos
    self.rect.x += rel_x
    self.rect.y += rel_y

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