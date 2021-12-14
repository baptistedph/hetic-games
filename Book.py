import pygame

class Book:
  def __init__(self, game, x, y) -> None:
    self.game = game

    # set book position
    self.position: list = [x, y]

    # load page sound
    self.page = pygame.mixer.Sound("assets/audio/page.mp3")

  # display or hide book
  def toggle_book(self):
    if self.game.display_book == False:
      pygame.mixer.Sound.play(self.page)
    self.game.display_book = not self.game.display_book