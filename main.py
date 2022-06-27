import pygame as pyg
import numpy as np
import os
import cv2

from dice import *
from button import *
from board import *

class Game():
  def __init__(self, surface):
    # changeable parameters
    self.surface = surface
    Dice.set_surface(self.surface)
    Button.set_surface(self.surface)
    self.running = True
    self.gridsize = Board.gridsize
    self.dicesize = Board.dicesize
    self.board = Board()
    self.init_btn()
  
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
    self.board.draw()
    
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
  
  def update(self):
    self.update_button()
    self.board.update()
  
  def update_button(self):
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