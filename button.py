import pygame as pyg
import numpy as np

class Button():
  # class attribute
  surface = None
  
  @classmethod
  def set_surface(cls, surface):
    cls.surface = surface
  
  def __init__(self, x, y, width, height, normal_color=None, pressing_color=None):
    self.top_rect = pyg.Rect(x, y, width, height)
    self.top_color = normal_color
    self.pressing_color = pressing_color
    self.normal_color = normal_color
    
    self.pressed = False
  
  def draw(self):
    pyg.draw.rect(Button.surface, self.top_color, self.top_rect, border_radius=5)
  
  def click(self):
    return
  
  def color_change(self, color):
    self.top_color = color
  
  def check_click(self, mouse_pos):
    if self.top_rect.collidepoint(mouse_pos):
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
    super().__init__(x, y, width, height, pyg.Color(255, 209, 26), pyg.Color(255, 170, 0))
    self.image = image
    self.img_rect = self.image.get_rect(center=self.top_rect.center)
  
  def draw(self):
    super().draw()
    Button.surface.blit(self.image, self.img_rect)
  
  def click(self, board, stars):
    print('Summon new dice...')
    
    # no slot for summon new dice
    if np.sum((board == 0).astype(np.uint8)) == 0:
      return board, stars
    
    board = np.reshape(board, -1)
    stars = np.reshape(stars, -1)
    
    candidate = np.where(board == 0)[0]
    loc = np.random.choice(candidate)
    dice_type = np.random.randint(1, 6)
    board[loc] = dice_type
    stars[loc] += 1
    
    board = np.reshape(board, (3, 5))
    stars = np.reshape(stars, (3, 5))
    
    print(board)
    
    return board, stars

class ResetBtn(Button):
  def __init__(self, image, x, y, width, height):
    super().__init__(x, y, width, height, pyg.Color(0, 230, 77))
    self.image = image
    self.img_rect = self.image.get_rect(center=self.top_rect.center)
  
  def draw(self):
    super().draw()
    Button.surface.blit(self.image, self.img_rect)
  
  def click(self, b, s):
    print('Reset the game...')
    
    board = np.zeros((3, 5), dtype=np.int16)
    boardStar = np.zeros((3, 5), dtype=np.int16)
    
    print(board)
    
    return board, boardStar