import pygame

class Object:
  def __init__(self, x, y, sound, sprite_path) -> None:

    # set book position
    self.position: list = [x, y]

    self.is_displayed = False

    self.image = pygame.image.load(sprite_path)
    self.image_width = self.image.get_rect().width
    self.image_height = self.image.get_rect().height

    # load page sound
    self.page = pygame.mixer.Sound(sound)

  # display or hide book
  def toggle_object(self):
    if self.is_displayed == False:
      pygame.mixer.Sound.play(self.page)
    self.is_displayed = not self.is_displayed
