import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer
import pytmx
import pyscroll
from Player import Player
from Object import Object
from Brontis import Brontis
import time

class Game:
  def __init__(self) -> None:
    self.near_book = False
    self.near_phone = False
    self.wifi_pass = 'ErwinTheCat93'
    self.connected = False
    self.fullscreen = True
    self.question = None
    self.game_over = False
    self.initial_time = 0
    self.cooldown = 1
    self.download = 0
    self.current_screen = 1
    self.wifi_speed = 700

    # init window
    if self.fullscreen:
      self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
      self.screen = pygame.display.set_mode((1280, 720))
    self.screen_width = self.screen.get_width()
    self.screen_height = self.screen.get_height()
    pygame.display.set_caption('Hetic Games')

    # init fonts
    self.title = pygame.font.SysFont('freesansbold.ttf', 50)
    self.label = pygame.font.SysFont('freesansbold.ttf', 30)


    # create book text
    self.info_text = '© 2021 - HETIC GAMES'
    self.update_text(self.info_text)

    # create a question label
    self.question_text_surfaces = []

    # create a password input
    password_input_manager = TextInputManager(validator = lambda input: len(input) <= 22)
    self.password_input = TextInputVisualizer(manager = password_input_manager, cursor_blink_interval=500, cursor_color=(0, 0, 0), font_color=(0, 0, 0), font_object=self.title)

    # create a answer input
    answer_input_manager = TextInputManager(validator = lambda input: len(input) <= 1)
    self.answer_input = TextInputVisualizer(manager = answer_input_manager, cursor_blink_interval=500, cursor_color=(255, 255, 255), font_color=(255, 255, 255), font_object=self.title)

    # load answer button sprite
    self.answer_image = pygame.image.load('assets/images/validate.png')
    self.answer_image_rect = self.answer_image.get_rect()
    self.answer_image_rect.x = self.screen_width / 2 - self.answer_image_rect.width / 2
    self.answer_image_rect.y = 800

    # load start button sprite
    self.start_image = pygame.image.load('assets/images/start.png')
    self.start_image_rect = self.start_image.get_rect()
    self.start_image_rect.x = self.screen_width / 2 - self.start_image_rect.width / 2
    self.start_image_rect.y = 700

    # load restart button sprite
    self.restart_image = pygame.image.load('assets/images/restart.png')
    self.restart_image_rect = self.restart_image.get_rect()
    self.restart_image_rect.x = self.screen_width / 2 - self.restart_image_rect.width / 2
    self.restart_image_rect.y = 700

    # load logo image
    self.logo_image = pygame.image.load('assets/images/logo.png')

    # load submit button
    self.submit_button = pygame.image.load('assets/images/submit.png')
    self.submit_button_rect = self.submit_button.get_rect()
    self.submit_button_rect.x = self.screen_width / 2 - self.submit_button_rect.width / 2 + 190
    self.submit_button_rect.y = 380

    # load lives sprite
    self.lives_image = pygame.image.load('assets/images/lives/3.png')

    # load music
    audio = pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(0.0)

    # load map
    tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
    map_layer.zoom = 4
    
    # player spawn
    player_position = tmx_data.get_object_by_name('player')
    self.player = Player(player_position.x, player_position.y, 1.5, 'assets/images/player.png')

    # brontis spawn
    brontis_position = tmx_data.get_object_by_name('brontis')
    self.brontis = Brontis(self, brontis_position.x, brontis_position.y, 10, 'assets/images/brontis.png', self.player)

    # book position
    book_position = tmx_data.get_object_by_name('book')
    self.book = Object(book_position.x, book_position.y, 'assets/audio/page.mp3', 'assets/images/book.png')
    
    # phone position
    phone_position = tmx_data.get_object_by_name('phone')
    self.phone = Object(phone_position.x, phone_position.y, 'assets/audio/page.mp3', 'assets/images/phone.png')

    self.is_answering = False

    self.choices = []

    self.download_progress_text = self.label.render(f'Téléchargement du devoir en cours ({round(self.download * 100)}%)', False, (255, 255, 255))
  

    # collides
    self.walls = []
    for obj in tmx_data.objects:
      if obj.type == 'collide':
        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # create group of layers
    self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
    self.group.add(self.player)
    self.group.add(self.brontis)

  def update_text(self, text):
    self.info_text_surface = self.label.render(text, False, (255, 255, 255))

  def update_pages(self):
    # draw map
    if self.current_screen == 1:
      self.screen.fill('#402EA9')
      self.screen.blit(self.logo_image, (self.screen_width / 2 - self.logo_image.get_rect().width / 2, 100))
      
      # display start button
      self.screen.blit(self.start_image, self.start_image_rect)
    elif self.current_screen == 2:
      self.group.draw(self.screen)
      self.brontis.walk()
    elif self.current_screen == 3:
      self.screen.fill('#402EA9')
      title = self.title.render('Vous avez perdu', False, (255, 255, 255))
      self.screen.blit(title, (self.screen_width / 2 - title.get_rect().width / 2, 200))
    elif self.current_screen == 4:
      self.screen.fill('#402EA9')
      title = self.title.render('Vous avez réussi à télécharger votre devoir !', False, (255, 255, 255))
      self.screen.blit(title, (self.screen_width / 2 - title.get_rect().width / 2, 200))


    if self.current_screen == 3 or self.current_screen == 4:
      self.screen.blit(self.restart_image, self.restart_image_rect)
      



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
    radius = 20

    if (bookX - playerX < radius and bookX - playerX > -radius) and (bookY - playerY < radius and bookY - playerY > -radius):
      if not self.connected:
        self.info_text = '[E] ouvrir le livre.'
      else:
        self.info_text = 'Bravo ! Vous êtes connecté'
      self.near_book = True
    else:
      self.info_text = None
      self.book.is_displayed = False
      self.near_book = False

    if self.info_text:
      self.info_text_surface = self.label.render(self.info_text, False, (255, 255, 255))

  def check_answer(self):
    if self.answer_input.value.isdigit() and int(self.answer_input.value) > 0 and int(self.answer_input.value) <= len(self.question['choices']):
      answer = self.question['choices'][int(self.answer_input.value) - 1]
      if answer == self.question['answer']:
        self.wifi_speed += 300
      else:
        if self.player.lives > 1:
          self.player.lives -= 1
          self.wifi_speed -= 1000
          if self.wifi_speed < 0:
            self.wifi_speed = 0
          self.lives_image = pygame.image.load(f'assets/images/lives/{self.player.lives}.png')
        else:
          self.current_screen = 3
          self.game_over = True
      self.lives_image_width = self.lives_image.get_rect().width
      self.lives_image_height = self.lives_image.get_rect().height
      self.is_answering = False
      self.brontis.pause = False
      self.choices = []
      self.question_text_surfaces = []
      self.player.protected = True
      self.initial_time = time.time()



  def handle_answering(self, question):
    # create name input label
    self.book.is_displayed = False
    self.phone.is_displayed = False
    splited_question = self.question['question'].split('\n')
    for line in splited_question:
      self.question_text_surfaces.append(self.title.render(line, False, (255, 255, 225)))
    for choice in question['choices']:
      choice_text_surface = self.label.render(choice, False, (255, 255, 225))
      self.choices.append(choice_text_surface)

  # check if near of the phone  
  def is_near_of_the_phone(self) -> None:
      [phoneX, phoneY] = self.phone.position
      [playerX, playerY] = self.player.position
      radius = 30

      if (phoneX - playerX < radius and phoneX - playerX > -radius) and (phoneY - playerY < radius and phoneY - playerY > -radius):
        if not self.connected: 
          self.info_text = '[E] prendre le téléphone.'
        else:
          self.info_text = 'Bravo ! Vous êtes connecté'
        self.near_phone = True
      else:
        self.info_text = None
        self.phone.is_displayed = False
        self.near_phone = False

      if self.info_text:
        self.update_text(self.info_text)

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
      if not self.is_answering:
        self.handle_input()

      # loop through user events
      events = pygame.event.get()

      # check for collides
      self.update()

      self.update_pages()

      if self.current_screen == 1:
        self.screen.blit(self.info_text_surface, (self.screen_width - 300, self.screen_height - 100))
  

      # check if player is near of the book
      if self.current_screen == 2:

        self.is_near_of_the_book()
        self.is_near_of_the_phone()

        if not (self.near_book or self.near_phone):
          self.info_text = ''
          self.update_text(self.info_text)

        self.screen.blit(self.lives_image, (20, 20))

      if self.book.is_displayed:
        self.screen.blit(self.book.image, (self.screen_width / 2 - self.book.image_width / 2, self.screen_height / 2 - self.book.image_height / 2))

      if self.phone.is_displayed:
        self.screen.blit(self.phone.image, (self.screen_width / 2 - self.phone.image_width / 2, self.screen_height / 2 - self.phone.image_height / 2))
        self.screen.blit(self.password_input.surface, (self.screen_width / 2 - 235, 400))
        self.screen.blit(self.submit_button, self.submit_button_rect)
        self.password_input.update(events)

      if self.is_answering:
        for i, line in enumerate(self.question_text_surfaces):
          self.screen.blit(line, (self.screen_width / 2 - 400, self.screen_height / 2 - 200 + i * 50))
        for i, choice in enumerate(self.choices):
          self.screen.blit(choice, (self.screen_width / 2 - 400, self.screen_height / 2 - 100 + len(self.question_text_surfaces) * 50 + i * 50))

        self.screen.blit(self.answer_input.surface, (self.screen_width / 2 - self.answer_input.surface.get_rect().width / 2, self.screen_height / 2 - 100 + len(self.question_text_surfaces) * 50 + len(self.choices) * 50))
        self.answer_input.update(events)
        
        self.screen.blit(self.answer_image, self.answer_image_rect)

      current_time = time.time()

      if current_time - self.initial_time > self.cooldown:
        self.player.protected = False

      if self.connected and self.download <= 1:
            
          
        self.screen.blit(self.download_progress_text, (20, self.screen_height - 80))

        if not self.is_answering:
          # draw download bar
          pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(20, self.screen_height - 50, 500, 20))
          pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(20, self.screen_height - 50, 500 * self.download, 20))

          self.download_progress_text = self.label.render(f'Téléchargement du devoir en cours ({round(self.download * 100)}%) - {self.wifi_speed / 1000}Gbits/s', False, (255, 255, 255))
          
          self.download += self.wifi_speed / 10000000

      if self.download >= 1:
        self.current_screen = 4

      

      for event in events:
        # if user quit
        if event.type == pygame.QUIT:
          running = False

        # if user press key
        elif event.type == pygame.KEYDOWN:
          # e
          if event.key == pygame.K_e and not self.is_answering:
            if self.near_book:
              self.book.toggle_object()
            if self.near_phone and not self.phone.is_displayed:
              self.phone.toggle_object()
          if event.key == pygame.K_x and not self.is_answering:
            if self.near_book and self.book.is_displayed:
              self.book.toggle_object()
            if self.near_phone and self.phone.is_displayed:
              self.phone.toggle_object()
      

        # if user clicked on a button
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if self.start_image_rect.collidepoint(event.pos) and self.current_screen == 1:
            pygame.mixer.music.play(-1)
            self.current_screen = 2
          if self.submit_button_rect.collidepoint(event.pos) and self.current_screen == 2:
            if self.password_input.value == self.wifi_pass:
      
              self.connected = True
          
          if self.answer_image_rect.collidepoint(event.pos) and self.current_screen == 2:
            if not self.answer_input.value == '': 
              self.check_answer()

          if self.restart_image_rect.collidepoint(event.pos) and (self.current_screen == 3 or self.current_screen == 4):
            self.__init__()

      # refresh at each frame
      pygame.display.flip()

      clock.tick(60)
      
      if not self.current_screen == 2:
        pygame.display.update()

    pygame.quit()
