import pygame as pyg
import numpy as np
import os
import cv2

from dice import *
from button import *

class Game():
  def __init__(self, surface):
    # changeable parameters
    self.gridsize = 80
    self.dicesize = 70
    
    self.running = True
    self.surface = surface
    self.board_w = 5
    self.board_h = 3
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
          for dice in self.DiceList:
            dice.is_dice_select(event.pos)
      elif event.type == pyg.MOUSEBUTTONUP:
        for btn in self.BtnList:
          if btn.check_click(event.pos):
            self.DiceList = btn.click(self.DiceList)
        for dice in self.DiceList:
          if dice.is_drag:
            dice.reset_dice_loc()
      elif event.type == pyg.MOUSEMOTION:
        for dice in self.DiceList:
          if dice.is_drag:
            dice.update_loc(event.rel)
  
  def play(self):
    while self.running:
      self.event_handler()
      if not self.running:
        break
      self.surface.fill(pyg.Color("black"))
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
    
    for y in range(self.board_h):
      for x in range(self.board_w):
        dice_type = 0
        posx = x*self.gridsize + 50
        posy = y*self.gridsize + 50
        image = self.imgs[dice_type]
        dice = Dice(image, dice_type, posx, posy, self.dicesize, self.dicesize, (dice_type != 0))
        dice.set_content(self.imgs[dice_type])
        
        self.DiceList.append(dice)
  
  def update(self):
    self.update_button()
    self.update_board()
  
  def update_button(self):
    return
  
  def update_board(self):
    for y in range(self.board_h):
      for x in range(self.board_w):
        dice = self.DiceList[5*y+x]
        dice_type = dice.dice_type
        dice.draggable = dice_type != 0
        dice.set_content(self.imgs[dice_type])
    
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