import pygame as pyg
import numpy as np
import os
import cv2


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
  def __init__(self, image, posx, posy, width, height)
    super().__init__(image, posx, posy, width, height)
    self.set_content(image)


class JokerDice(Dice):
  def __init__(self, image, posx, posy, width, height)
    super().__init__(image, posx, posy, width, height)
  
  def skill(self, **kwargs):
    changeTo = kwargs['changeTo']
    imageList = kwargs['imageList']
    
    return

class Game():
  def __init__(self, surface):
    # changeable parameters
    self.gridsize = 80
    self.dicesize = 70
    
    self.running = True
    self.surface = surface
    self.board = np.zeros((3, 5), dtype=np.int16)
    self.boardStar = np.zeros((3, 5), dtype=np.int16)
    self.load_img_from_disk()
    Dice.set_surface(self.surface)
    Button.set_surface(self.surface)
    self.init_btn()
    self.init_board()
  
  def load_img_from_disk(self):
    img_names = ['Blank.png', 'Growth.png', 'Joker.png',
                  'Golem.png', 'Typhoon.png', 'Wind.png']
    self.imgs = []

    for img in img_names:
      path = os.path.join('./img', img)
      _img = pyg.image.load(path)
      _img = pyg.transform.scale(_img, (self.dicesize, self.dicesize))
      self.imgs.append(_img)
  
  def event_handler(self):
    for event in pyg.event.get():
      if event.type == pyg.QUIT:
        self.running = False
      elif event.type == pyg.MOUSEBUTTONDOWN:
        if event.button == 1:
          for btn in self.BtnList:
            btn.check_click(event.pos)
      elif event.type == pyg.MOUSEBUTTONUP:
        for btn in self.BtnList:
          if btn.check_click(event.pos):
            self.board, self.boardStar = btn.click(self.board, self.boardStar)
  
  def play(self):
    while self.running:
      self.event_handler()
      if not self.running:
        break
      # print(self.board)
      self.update()
      self.draw()
      pyg.display.flip()
  
  def draw(self):
    for dice in self.DiceList:
      dice.draw()
    
    for btn in self.BtnList:
      btn.draw()
  
  def init_btn(self):
    self.BtnList = []
    
    # Create Summon button
    path = 'img/Summon.png'
    image = pyg.image.load(path)
    image = pyg.transform.scale(image, (self.dicesize-5, self.dicesize-5))
    x = self.gridsize*5.2 + 50
    y = self.gridsize*0.5 + 50
    h = self.gridsize*2.3
    btn = SummonBtn(image, x, y, self.dicesize+5, h)
    self.BtnList.append(btn)
    
    # Create Reset button
    path = 'img/Reset.png'
    image = pyg.image.load(path)
    image = pyg.transform.scale(image, (30, 30))
    x = self.gridsize*5.2 + 50
    y = self.gridsize*3.2 + 50
    h = self.gridsize*0.6
    btn = ResetBtn(image, x, y, self.dicesize+5, h)
    self.BtnList.append(btn)
  
  def init_board(self):
    self.DiceList = []
    
    for y in range(len(self.board)):
      for x in range(len(self.board[y])):
        posx = x*self.gridsize + 50
        posy = y*self.gridsize + 50
        
        dice = Dice(posx, posy, self.dicesize, self.dicesize)
        dice.set_content(self.imgs[self.board[y][x]])
        
        self.DiceList.append(dice)
  
  def update(self):
    self.update_button()
    self.update_board()
  
  def update_button(self):
    return
  
  def update_board(self):
    for y in range(len(self.board)):
      for x in range(len(self.board[y])):
        dice = self.DiceList[5*y+x]
        dice.set_content(self.imgs[self.board[y][x]])
    
    return

def main():
  # Initialize pygame
  pyg.init()
  
  # Create display screen
  screen = pyg.display.set_mode((600, 400))
  pyg.display.set_caption('Random Dice Wars Emulator')
  icon = pyg.image.load('img/AppIcon.png')
  pyg.display.set_icon(icon)
  
  # Initialize game
  game = Game(screen)
  
  # Start the game
  game.play()
  
  # Quit
  pyg.quit()

if __name__ == '__main__':
    main()