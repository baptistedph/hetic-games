import pygame
import pygame_textinput
import pytmx
import pyscroll
from Player import Player
from Book import Book

class Game:
  def __init__(self) -> None:
    self.is_playing = False
    self.near_book = False
    self.display_book = False

    # init window
    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    self.screen_width = self.screen.get_width()
    self.screen_height = self.screen.get_height()
    pygame.display.set_caption('Hetic Games')

    # create book text
    self.info_text = pygame.font.SysFont('freesansbold.ttf', 30)
    self.info_text_surface = self.info_text.render('© 2021 - HETIC GAMES', False, (255, 255, 255))

    # crete name input label
    self.label_text = pygame.font.SysFont('freesansbold.ttf', 30)
    self.label_text_surface = self.info_text.render('Enter your name', False, (185, 179, 225) )

    # create a name input
    name_input_font = pygame.font.SysFont('freesansbold.ttf', 50)
    self.name_input = pygame_textinput.TextInputVisualizer(cursor_blink_interval=500, cursor_color=(255, 255, 255), font_color=(255, 255, 255), font_object=name_input_font)
    
    # load start button sprite
    self.start_image = pygame.image.load('assets/images/start.png')
    self.start_image_rect = self.start_image.get_rect()
    self.start_image_rect.x = self.screen_width / 2 - self.start_image_rect.width / 2
    self.start_image_rect.y = 700

    # load book image
    self.book_image = pygame.image.load('assets/images/book.png')
    self.book_image_width = self.book_image.get_rect().width
    self.book_image_height = self.book_image.get_rect().height

    # load logo image
    self.logo_image = pygame.image.load('assets/images/logo.png')
    self.logo_image_width = self.logo_image.get_rect().width
    self.logo_image_height = self.logo_image.get_rect().height

    # load music
    audio = pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(0.1)

    # load map
    tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
    map_layer.zoom = 3
    
    # player spawn
    player_position = tmx_data.get_object_by_name('player')
    self.player = Player(player_position.x, player_position.y)

    # book position
    book_position = tmx_data.get_object_by_name('book')
    self.book = Book(self, book_position.x, book_position.y)

    # collides
    self.walls = []
    for obj in tmx_data.objects:
      if obj.type == 'collision':
        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # create group of layers
    self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
    self.group.add(self.player)


  def update_pages(self):
    # draw map
    if self.is_playing:
      self.group.draw(self.screen)
    else:
      self.screen.fill('#402EA9')
      self.screen.blit(self.logo_image, (self.screen_width / 2 - self.logo_image_width / 2, 100))
      
      # display name input
      self.screen.blit(self.label_text_surface, (self.screen_width / 2 - 200, 560))
      self.screen.blit(self.name_input.surface, (self.screen_width / 2 - 200, 600))

      # display start button
      self.screen.blit(self.start_image, self.start_image_rect)

  # listen on keypress
  def handle_input(self) -> None:
    pressed = pygame.key.get_pressed()

    # z or arrow up
    if pressed[pygame.K_z] or pressed[pygame.K_UP]:
      self.player.move_up()

    # s or arrow down
    elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
      self.player.move_down()

    # q or arrow left     
    elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
      self.player.move_left()

    # d or arrow right          
    elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
      self.player.move_right()

  # check if near of the book
  def is_near_of_the_book(self) -> None:
    [bookX, bookY] = self.book.position
    [playerX, playerY] = self.player.position

    if (bookX - playerX < 50 and bookX - playerX > -50) and (bookY - playerY < 50 and bookY - playerY > -50):
      self.text_info = '[E] open the book.'
      self.near_book = True
    else:
      self.text_info = ''
      self.near_book = False
    
    self.info_text_surface = self.info_text.render(self.text_info, False, (255, 255, 255))
  
  # check for collides
  def update(self) -> None:
    self.group.update()
    if self.player.rect.collidelist(self.walls) > -1:
      self.player.move_back()
      
  # main loop function
  def run(self) -> None:
    clock = pygame.time.Clock()
    running: bool = True
    while running:
      # save last player location
      self.player.save_location()

      # center the camera on the player
      self.group.center(self.player.rect.center)

      # listen on keypress
      self.handle_input()

      # check if player is near of the book
      if self.is_playing:
        self.is_near_of_the_book()

      # check for collides
      self.update()

      self.update_pages()

      # display book is display book variable set to true
      if self.display_book:
        self.screen.blit(self.book_image, (self.screen_width / 2 - self.book_image_width / 2, self.screen_height / 2 - self.book_image_height / 2))

      # display book text
      self.screen.blit(self.info_text_surface, (self.screen_width - 300, self.screen_height - 100))
      
      # loop through user events
      events = pygame.event.get()

      self.name_input.update(events)

      # refresh at each frame
      pygame.display.flip()
    
      for event in events:
        # if user quit
        if event.type == pygame.QUIT:
          running = False

        # if user press key
        elif event.type == pygame.KEYDOWN:
          # e
          if event.key == pygame.K_e:
            if self.near_book:
              self.book.toggle_book()

        # if user clicked on a button
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if self.start_image_rect.collidepoint(event.pos):
            pygame.mixer.music.play(-1)
            self.is_playing = True

      clock.tick(60)
      
      if not self.is_playing:
        pygame.display.update()

    pygame.quit()