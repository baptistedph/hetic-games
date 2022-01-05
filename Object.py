import pygame

class Object:
  # constructor init
  def __init__(self, x, y, sound, sprite_path) -> None:
    self.position: list = [x, y]
    self.is_displayed: bool = False
    self.image = pygame.image.load(sprite_path)
    self.image_width: float = self.image.get_rect().width
    self.image_height: float = self.image.get_rect().height
    self.page = pygame.mixer.Sound(sound)

  # display or hide object
  def toggle_object(self) -> None:
    if self.is_displayed == False:
      pygame.mixer.Sound.play(self.page)
    self.is_displayed = not self.is_displayed
