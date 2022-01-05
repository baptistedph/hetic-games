from os import walk
from Player import Player
from time import sleep
from random import randint
from json import loads

class Brontis(Player):
  def __init__(self, game, x, y, speed, sprite, player):
    super().__init__(x, y, speed, sprite)
    self.x = x
    self.y = y
    self.game = game
    self.player = player
    self.speed = speed
    self.limits = [
      [265, 0, 0],
      [0, 240, 0],
      [-230, 0, 0],
      [130, -80, 0],
      [100, 0, 0],
      [0, 20, 0],
      [70, 0, 0],
      [0, -150, 0],
      [0, 0, 300],
      [70, 0, 0],
      [0, -30, 0],
      [-70, 0, 0],
      [0, 180, 0],
      [-50, 0, 0],
      [-50, -50, 0],
      [-130, 0, 0],
      [0, -30, 0],
      [130, 0, 0],
      [0, 30, 0],
      [0, -60, 0],
      [30, 0, 0],
      [0, -75, 0],
      [-265, 10, 0],
      [0, 0, 1000]
    ]
    self.questions = loads(open("questions.json", "r").read())
    self.floor = [[0, 0] for x in self.limits]
    self.current_walk_step = 0
    self.pause = False
    self.pause_current_time = 0
    self.adapt_limits()
    
  def adapt_limits(self):
    new_limits = []
    for limit_arr in self.limits:
      new_limit_array = []
      for limit in limit_arr:
        limit /= self.speed
        new_limit_array.append(limit)
      new_limits.append(new_limit_array)
    
    self.limits = new_limits

  def pick_a_random_question(self):
    i = randint(0, len(self.questions) - 1)
    return self.questions[i]

  def ask_question(self):
    question = self.pick_a_random_question()
    self.game.question = None
    self.game.is_answering = True
    self.pause = True
    self.game.question = question
    self.game.handle_answering(question)

  def is_near_of_the_player(self):
      radius = 30
      [playerX, playerY] = self.player.position
      [brontisX, brontisY] = self.position

      if (playerX - brontisX < radius and playerX - brontisX > -radius) and (playerY - brontisY < radius and playerY - brontisY > -radius):
        if not self.game.is_answering and not self.player.protected:
          self.ask_question()

  def walk(self):

    if self.limits[self.current_walk_step][2] > 0:
      if self.pause_current_time < self.limits[self.current_walk_step][2]:
        self.pause_current_time += 1
        self.pause = True
      else:
        self.pause = False
        self.pause_current_time = 0

    if not self.pause:
      if abs(self.floor[self.current_walk_step][0]) < abs(self.limits[self.current_walk_step][0]) or abs(self.floor[self.current_walk_step][1]) < abs(self.limits[self.current_walk_step][1]):
        if abs(self.floor[self.current_walk_step][0]) < abs(self.limits[self.current_walk_step][0]):
          if self.limits[self.current_walk_step][0] > 0:
            super().move_right()
            self.floor[self.current_walk_step][0] += 1
          else:
            super().move_left()
            self.floor[self.current_walk_step][0] -= 1

        if abs(self.floor[self.current_walk_step][1]) < abs(self.limits[self.current_walk_step][1]):
          if self.limits[self.current_walk_step][1] > 0:
            super().move_up()
            self.floor[self.current_walk_step][1] += 1
          else:
            super().move_down()
            self.floor[self.current_walk_step][1] -= 1
      else:
        if self.current_walk_step < len(self.limits) - 1:
          self.current_walk_step += 1
        else:
          self.current_walk_step = 0
          self.floor = [[0, 0] for x in self.limits]
          
    

    self.is_near_of_the_player()



  











