import numpy as np
import os
from dice import *

class Board():
  dice_list = []
  imgs = []
  gridsize = 80
  dicesize = 70
  board_h = 3
  board_w = 5
  SP = 200

  @staticmethod
  def get_board_info():
    return

  @staticmethod
  def generate_random_dice():
    dice_type = np.random.randint(1, 6)
    image = Board.imgs[dice_type]

    if dice_type == 1:
      new_dice = GrowthDice(image, dice_type, 0, 0, Board.dicesize, Board.dicesize, (dice_type != 0))
    elif dice_type == 2:
      new_dice = JokerDice(image, dice_type, 0, 0, Board.dicesize, Board.dicesize, (dice_type != 0))
    elif dice_type == 3:
      new_dice = NormalDice(image, dice_type, 0, 0, Board.dicesize, Board.dicesize, (dice_type != 0))
    elif dice_type == 4:
      new_dice = NormalDice(image, dice_type, 0, 0, Board.dicesize, Board.dicesize, (dice_type != 0))
    elif dice_type == 5:
      new_dice = NormalDice(image, dice_type, 0, 0, Board.dicesize, Board.dicesize, (dice_type != 0))
    
    return new_dice

  @staticmethod
  def generate_empty_dice():
    dice_type = 0
    image = Board.imgs[dice_type]
    new_dice = NormalDice(image, dice_type, 0, 0, Board.dicesize, Board.dicesize, (dice_type != 0))
    return new_dice

  @staticmethod
  def summon_dice():
    # no slot for summon new dice
    if np.sum([dice.dice_type == 0 for dice in Board.dice_list]) == 0:
      print('No more space')
      return
    
    new_dice = Board.generate_random_dice()

    candidate = np.where([dice.dice_type == 0 for dice in Board.dice_list])[0]
    loc = np.random.choice(candidate)

    new_dice = Board.dice_list[loc].copy_info(new_dice, need_cp_star=True)
    new_dice.dice_star += 1
    Board.dice_list[loc] = new_dice

  @staticmethod
  def reset_game():
    for dice in Board.dice_list:
      dice.dice_type = 0
      dice.dice_star = 0
    
  def __init__(self):
    self.initialization()

  def initialization(self):
    self.load_img_from_disk()
    self.init_board()

  def load_img_from_disk(self):
    img_names = ['Blank.png', 'Growth.png', 'Joker.png',
                  'Golem.png', 'Typhoon.png', 'Wind.png']
    
    for img in img_names:
      path = os.path.join('./img', img)
      _img = pyg.image.load(path)
      _img = pyg.transform.scale(_img, (self.dicesize, self.dicesize))
      Board.imgs.append(_img)

  def merge_check(self, pos):
    # search the dice which can be merged
    dice_a_idx = None
    dice_b_idx = None
    
    for idx in range(len(Board.dice_list)):
      dice = Board.dice_list[idx]
      if dice.is_drag:
        dice_a_idx = idx
        dice.is_drag = False
      elif dice.rect.collidepoint(pos) and dice.dice_type != 0:
        dice_b_idx = idx
      dice.reset_dice_loc()
    
    if dice_a_idx != None and dice_b_idx != None:
      # merge dice
      self.merge_dice(dice_a_idx, dice_b_idx)
  
  def check_skill(self):
    for idx in range(len(Board.dice_list)):
      can_activate = Board.dice_list[idx].check_skill_tick()
      if can_activate:
        new_dice = Board.dice_list[idx].skill(Board.generate_random_dice)
        if new_dice:
          Board.dice_list[idx] = new_dice

  def merge_dice(self, loc_a, loc_b):
    new_dice_a = Board.generate_empty_dice()
    new_dice_b = Board.generate_random_dice()
    new_dice_a = Board.dice_list[loc_a].after_merge(new_dice_a, Board.dice_list[loc_b])
    new_dice_b = Board.dice_list[loc_a].merge(new_dice_b, Board.dice_list[loc_b])
    Board.dice_list[loc_a] = new_dice_a
    Board.dice_list[loc_b] = new_dice_b

  def check_dice_select(self, pos):
    for dice in Board.dice_list:
      dice.is_dice_select(pos)
  
  def update(self, pos=None):
    for dice in Board.dice_list:
      if dice.is_drag and pos:
        dice.update_loc(pos)
      dice_type = dice.dice_type
      dice.draggable = dice_type != 0
      dice.set_content(self.imgs[dice_type])

  def draw(self):
    for dice in Board.dice_list:
      dice.draw()

  def init_board(self):
    for y in range(Board.board_h):
      for x in range(Board.board_w):
        posx = x*Board.gridsize + 50
        posy = y*Board.gridsize + 50
        dice = Board.generate_empty_dice()
        dice.original_x = posx
        dice.original_y = posy
        dice.reset_dice_loc()

        Board.dice_list.append(dice)