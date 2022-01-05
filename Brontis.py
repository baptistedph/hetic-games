from os import walk
from Player import Player
from time import sleep
from random import randint
from json import loads

class Brontis(Player):
  # constructor init
  def __init__(self, game, x, y, speed, sprite, player):
    super().__init__(x, y, speed, sprite)
    self.x: int = x
    self.y: int = y
    self.game = game
    self.player = player
    self.speed: int = speed
    self.coords: list = [
      [265, 0, 0],
      [0, 240, 0],
      [-210, 0, 0],
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
      [0, 0, 600]
    ]
    self.questions: str = loads(open("questions.json", "r").read())
    self.floor: list = [[0, 0] for x in self.coords]
    self.current_walk_step: int = 0
    self.pause: bool = False
    self.pause_current_time: int = 0
    self.adapt_limits()
    
  # adapt coors in function of the speed, to prevent coords from being multiplied
  def adapt_limits(self) -> None:
    new_limits: list = []
    for limit_arr in self.coords:
      new_limit_array = []
      for limit in limit_arr:
        limit /= self.speed
        new_limit_array.append(limit)
      new_limits.append(new_limit_array)
    
    self.coords = new_limits

  # pick a question among the questions.json file
  def pick_a_random_question(self) -> dict:
    i: int = randint(0, len(self.questions) - 1)
    return self.questions[i]

  # trigger game states and functions to handle the rest of the questions part
  def ask_question(self) -> None:
    question = self.pick_a_random_question()
    self.game.question = None
    self.game.is_answering = True
    self.pause = True
    self.game.question = question
    self.game.handle_answering(question)

  # check if brontis is next to the player
  def is_near_of_the_player(self) -> None:
      radius: int = 50
      [playerX, playerY] = self.player.position
      [brontisX, brontisY] = self.position

      if (playerX - brontisX < radius and playerX - brontisX > -radius) and (playerY - brontisY < radius and playerY - brontisY > -radius):
        if not self.game.is_answering and not self.player.protected:
          self.ask_question()

  # brontis moves
  def walk(self) -> None:
    # the third value from the coords means there is a break time to move to next coord
    if self.coords[self.current_walk_step][2] > 0:
      if self.pause_current_time < self.coords[self.current_walk_step][2]:
        self.pause_current_time += 1
        self.pause = True
      else:
        if self.game.is_answering == False:
          self.pause = False
        self.pause_current_time = 0

    if not self.pause:
      # we use the abs function to handle negative values to be intepreted as a move_left() or a move_down() but without interfering with the floor which is always increasing
      if abs(self.floor[self.current_walk_step][0]) < abs(self.coords[self.current_walk_step][0]) or abs(self.floor[self.current_walk_step][1]) < abs(self.coords[self.current_walk_step][1]):
        if abs(self.floor[self.current_walk_step][0]) < abs(self.coords[self.current_walk_step][0]):
          if self.coords[self.current_walk_step][0] > 0:
            super().move_right()
            self.floor[self.current_walk_step][0] += 1
          else:
            super().move_left()
            self.floor[self.current_walk_step][0] -= 1

        if abs(self.floor[self.current_walk_step][1]) < abs(self.coords[self.current_walk_step][1]):
          if self.coords[self.current_walk_step][1] > 0:
            super().move_up()
            self.floor[self.current_walk_step][1] += 1
          else:
            super().move_down()
            self.floor[self.current_walk_step][1] -= 1
      else:
        if self.current_walk_step < len(self.coords) - 1:
          self.current_walk_step += 1
        else:
          self.current_walk_step = 0
          self.floor = [[0, 0] for x in self.coords]
          
    
    self.is_near_of_the_player()



  











