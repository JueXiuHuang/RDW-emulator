import pygame as pyg
import numpy as np

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
  
  def click(self, dice_list):
    print('Summon new dice...')
    
    # no slot for summon new dice
    if np.sum([dice.dice_type == 0 for dice in dice_list]) == 0:
      print('No more space')
      return dice_list
    
    candidate = np.where([dice.dice_type == 0 for dice in dice_list])[0]
    loc = np.random.choice(candidate)
    dice_type = np.random.randint(1, 6)
    dice_list[loc].dice_type = dice_type
    dice_list[loc].dice_star += 1

    return dice_list

class ResetBtn(Button):
  def __init__(self, image, x, y, width, height):
    super().__init__(image, x, y, width, height, pyg.Color(0, 230, 77))
  
  def click(self, dice_list):
    print('Reset the game...')
    
    for dice in dice_list:
      dice.dice_type = 0
      dice.dice_star = 0
    
    return dice_list