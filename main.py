import pygame as pyg
import numpy as np
import os
import cv2

from dice import *
from button import *
from board import *
from displayer import *

class Game():
  def __init__(self, surface, font):
    # changeable parameters
    self.surface = surface
    self.font = font
    Dice.set_font_and_surface(font, surface)
    Button.set_font_and_surface(font, surface)
    Displayer.set_font_and_surface(font, surface)
    self.running = True
    self.gridsize = Board.gridsize
    self.dicesize = Board.dicesize
    self.board = Board()
    self.init_btn()
    self.init_displayer()
    self.tick_sec_ratio = 1300

  def play(self):
    tick = 1
    while self.running:
      self.board.check_skill()
      self.event_handler()
      if not self.running:
        break
      self.surface.fill(pyg.Color("black"))
      self.update()
      self.draw()
      pyg.display.flip()

      tick += 1
      if tick % self.tick_sec_ratio == 0:
        Board.wave += 1
        idx = np.sum([Board.wave >= wave for wave in Board.SP_level_wave])
        Board.SP += Board.SP_list[idx]

      if Board.wave > 30:
        self.running = False
  
  def event_handler(self):
    for event in pyg.event.get():
      if event.type == pyg.QUIT:
        self.running = False
      elif event.type == pyg.MOUSEBUTTONDOWN:
        if event.button == 1:
          for btn in self.BtnList:
            btn.check_click(event.pos)
          self.board.check_dice_select(event.pos)
      elif event.type == pyg.MOUSEBUTTONUP:
        for btn in self.BtnList:
          if btn.check_click(event.pos):
            btn.click()
        self.board.merge_check(event.pos)
      elif event.type == pyg.MOUSEMOTION:
        self.board.update(event.rel)
  
  def draw(self):
    self.board.draw()
    for dp in self.displayer_list:
      dp.draw()
    
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

    for i in range(1, 6):
      x = self.gridsize*(i-1) + 50
      y = self.gridsize*3.4 + 50
      h = self.gridsize*0.6
      btn = LvlUpBtn(i, x, y, self.dicesize+5, h)
      self.BtnList.append(btn)

  def init_displayer(self):
    self.displayer_list  = []

    # Create Wave display button
    x = self.gridsize*1.4 + 50
    y = self.gridsize*0
    h = self.gridsize*0.4
    wd = WaveDisplayer(x, y, self.dicesize*2.4, h)
    self.displayer_list.append(wd)

    # Create SP display button
    x = self.gridsize*5.2 + 50
    y = self.gridsize*0
    h = self.gridsize*0.4
    sd = SPDisplayer(x, y, self.dicesize*1, h)
    self.displayer_list.append(sd)
  
  def update(self):
    self.board.update()
    for dp in self.displayer_list:
      dp.update()
    for btn in self.BtnList:
      btn.update()
  
def main():
  # Initialize pygame
  pyg.init()
  
  # Create display screen
  screen = pyg.display.set_mode((600, 400))
  pyg.display.set_caption('Random Dice Wars Emulator')
  icon = pyg.image.load('img/AppIcon.png')
  pyg.display.set_icon(icon)
  font = pyg.font.Font(None, 30)
  
  # Initialize game
  game = Game(screen, font)
  
  # Start the game
  game.play()
  
  # Quit
  pyg.quit()

if __name__ == '__main__':
    main()