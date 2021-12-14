import pygame

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    # call the super class Sprite from pygame
    super().__init__()
  
    # load player sprite
    self.image = pygame.image.load('assets/images/player.png')
    
    # get player hitbox
    self.rect = self.image.get_rect()

    # set player position
    self.position: list = [x, y]

    # save last player position
    self.old_position = self.position.copy()

    # set player speed
    self.speed: int = 2

  # save last player position at each frame
  def save_location(self) -> None: 
    self.old_position = self.position.copy()

  ### move functions
  def move_right(self) -> None: 
    self.position[0] += self.speed

  def move_left(self) -> None: 
    self.position[0] -= self.speed
  
  def move_up(self) -> None: 
    self.position[1] -= self.speed

  def move_down(self) -> None: 
    self.position[1] += self.speed
  ###

  # move back to the last position if collide
  def move_back(self) -> None:
    self.position = self.old_position

  # update player position at each frame
  def update(self) -> None:
    self.rect.center = self.position