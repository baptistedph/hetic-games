import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer
import pytmx
import pyscroll
from Player import Player
from Object import Object
from Brontis import Brontis
import time

class Game:
  # constructor init
  def __init__(self) -> None:
    self.near_book: bool = False
    self.near_phone: bool = False
    self.wifi_pass: str = 'ErwinTheCat93'
    self.connected: bool = False
    self.fullscreen: bool = True
    self.question = None
    self.game_over: bool = False
    self.initial_time: int = 0
    self.cooldown: int = 3
    self.download: int = 0
    self.current_screen: int = 1
    self.wifi_speed: int = 700
    self.is_answering: bool = False
    self.choices: list = []
    self.walls: list = []
    self.volume = 0.5
    self.synopsis = '''
Un étudiant venant d’arriver a hetic a pour quête de télécharger un fichier qui est le sujet de son devoir.\n
Il doit télécharger au plus vite le fichier pour pouvoir rendre le devoir dans les temps.\n
\n
Il doit donc dans un premier temps trouver le code du wifi !\n
Mais attention Brontis s’est levé du mauvais pied aujourd’hui et d’humeur dévastante.\n
Il faut à tout prix l’éviter car il pourrait te faire perdre des vies.\n
Si Brontis t’attrape tu devras répondre à ses questions barbantes sur la culture GEEK !!\n
\n
Bon courage !
    '''

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

    # create label text at the bottom right
    self.info_text: str = '© 2021 - HETIC GAMES'
    self.update_text(self.info_text)

    # create the question label
    self.question_text_surfaces: list = []

    # create a password input
    password_input_manager = TextInputManager(validator = lambda input: len(input) <= 22)
    self.password_input = TextInputVisualizer(manager = password_input_manager, cursor_blink_interval=500, cursor_color=(0, 0, 0), font_color=(0, 0, 0), font_object=self.title)

    # create a answer input
    answer_input_manager = TextInputManager(validator = lambda input: len(input) <= 1)
    self.answer_input = TextInputVisualizer(manager = answer_input_manager, cursor_blink_interval=500, cursor_color=(255, 255, 255), font_color=(255, 255, 255), font_object=self.title)

    # load logo image
    self.logo_image = pygame.image.load('assets/images/logo.png')

    # load answer button sprite
    self.answer_image = pygame.image.load('assets/images/validate.png')
    self.answer_image_rect = self.answer_image.get_rect()
    self.answer_image_rect.x = self.screen_width / 2 - self.answer_image_rect.width / 2
    self.answer_image_rect.y = 800

    # load start button sprite
    self.start_image = pygame.image.load('assets/images/start.png')
    self.start_image_rect = self.start_image.get_rect()
    self.start_image_rect.x = self.screen_width / 2 - self.start_image_rect.width / 2
    self.start_image_rect.y = 650

    # load restart button sprite
    self.restart_image = pygame.image.load('assets/images/restart.png')
    self.restart_image_rect = self.restart_image.get_rect()
    self.restart_image_rect.x = self.screen_width / 2 - self.restart_image_rect.width / 2
    self.restart_image_rect.y = 700

    # load synopsis button sprite
    self.synopsis_image = pygame.image.load('assets/images/synopsis.png')
    self.synopsis_image_rect = self.synopsis_image.get_rect()
    self.synopsis_image_rect.x = self.screen_width / 2 - self.synopsis_image_rect.width / 2
    self.synopsis_image_rect.y = 750

    # load submit button sprite
    self.menu_image = pygame.image.load('assets/images/menu.png')
    self.menu_image_rect = self.menu_image.get_rect()
    self.menu_image_rect.x = 50
    self.menu_image_rect.y = 800

    # load menu button sprite
    self.submit_image = pygame.image.load('assets/images/submit.png')
    self.submit_image_rect = self.submit_image.get_rect()
    self.submit_image_rect.x = self.screen_width / 2 - self.submit_image_rect.width / 2 + 190
    self.submit_image_rect.y = 380

    # load lives sprite
    self.lives_image = pygame.image.load('assets/images/lives/3.png')

    # load music
    audio = pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(self.volume)

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
    self.brontis = Brontis(self, brontis_position.x, brontis_position.y, 1.5, 'assets/images/brontis.png', self.player)

    # book position
    book_position = tmx_data.get_object_by_name('book')
    self.book = Object(book_position.x, book_position.y, 'assets/audio/page.mp3', 'assets/images/book.png')
    
    # phone position
    phone_position = tmx_data.get_object_by_name('phone')
    self.phone = Object(phone_position.x, phone_position.y, 'assets/audio/phone.mp3', 'assets/images/phone.png')

    # download progress label
    self.download_progress_text = self.label.render(f'Téléchargement du devoir en cours ({round(self.download * 100)}%)', False, (255, 255, 255))

    # collides mapping
    for obj in tmx_data.objects:
      if obj.type == 'collide':
        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # create group of layers
    self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
    self.group.add(self.player)
    self.group.add(self.brontis)

  # re-render the text when changes
  def update_text(self, text) -> None:
    self.info_text_surface = self.label.render(text, False, (255, 255, 255))

  # load components in function of the current page
  def update_pages(self) -> None:
    # splash screen
    if self.current_screen == 1:
      self.screen.fill('#402EA9')
      self.screen.blit(self.logo_image, (self.screen_width / 2 - self.logo_image.get_rect().width / 2, 100))
      self.screen.blit(self.start_image, self.start_image_rect)
      self.screen.blit(self.synopsis_image, self.synopsis_image_rect)
    # main screen
    elif self.current_screen == 2:
      self.group.draw(self.screen)
      self.brontis.walk()
    # game over screen
    elif self.current_screen == 3:
      self.screen.fill('#402EA9')
      title = self.title.render('Vous avez perdu...', False, (255, 255, 255))
      self.screen.blit(title, (self.screen_width / 2 - title.get_rect().width / 2, 200))
    # win screen
    elif self.current_screen == 4:
      self.screen.fill('#402EA9')
      title = self.title.render('Vous avez réussi à télécharger votre devoir !', False, (255, 255, 255))
      self.screen.blit(title, (self.screen_width / 2 - title.get_rect().width / 2, 200))
    # synopsis screen
    elif self.current_screen == 5:
      self.screen.fill('#402EA4')
      title = self.title.render('Synopsis', False, (255, 255, 255))
      self.screen.blit(title, (50, 100))
      splited_text = self.synopsis.split('\n')
      for i, line in enumerate(splited_text):
        text = self.label.render(line, False, (255, 255, 225))
        self.screen.blit(text, (50, 200 + i * 30))
      self.screen.blit(self.menu_image, self.menu_image_rect)
    
    # game over & win screens
    if self.current_screen == 3 or self.current_screen == 4:
      pygame.mixer.music.stop()
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

  # check if the player is near of the book
  def is_near_of_the_book(self) -> None:
    [bookX, bookY] = self.book.position
    [playerX, playerY] = self.player.position
    radius: int = 20

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

  # answer type validation and check if it's correct answer
  def check_answer(self) -> None:
    if self.answer_input.value.isdigit() and int(self.answer_input.value) > 0 and int(self.answer_input.value) <= len(self.question['choices']):
      answer: str = self.question['choices'][int(self.answer_input.value) - 1]
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

  # display the question and the choices, 
  def handle_answering(self, question) -> None:
    self.book.is_displayed = False
    self.phone.is_displayed = False
    splited_question = self.question['question'].split('\n')
    for line in splited_question:
      self.question_text_surfaces.append(self.title.render(line, False, (255, 255, 225)))
    for choice in question['choices']:
      choice_text_surface = self.label.render(choice, False, (255, 255, 225))
      self.choices.append(choice_text_surface)

  # check if the player is near of the phone  
  def is_near_of_the_phone(self) -> None:
      [phoneX, phoneY] = self.phone.position
      [playerX, playerY] = self.player.position
      radius: int = 30

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

      # switch page if asked
      self.update_pages()

      # display the bottom right text on the splash screen
      if self.current_screen == 1:
        self.screen.blit(self.info_text_surface, (self.screen_width - 300, self.screen_height - 100))
  
      # check if player is near of the book
      if self.current_screen == 2:
        # check is the player is close to one of these objects
        self.is_near_of_the_book()
        self.is_near_of_the_phone()
        # update the bottom right text to indicate the key to press to open either the phone or the book
        if not (self.near_book or self.near_phone):
          self.info_text = ''
          self.update_text(self.info_text)
        # display lives image (heart)
        self.screen.blit(self.lives_image, (20, 20))
  
      # display the book
      if self.book.is_displayed:
        self.screen.blit(self.book.image, (self.screen_width / 2 - self.book.image_width / 2, self.screen_height / 2 - self.book.image_height / 2))

      # display the phone
      if self.phone.is_displayed:
        self.screen.blit(self.phone.image, (self.screen_width / 2 - self.phone.image_width / 2, self.screen_height / 2 - self.phone.image_height / 2))
        self.screen.blit(self.password_input.surface, (self.screen_width / 2 - 235, 400))
        self.screen.blit(self.submit_image, self.submit_image_rect)
        self.password_input.update(events)

      # display the question
      if self.is_answering:
        for i, line in enumerate(self.question_text_surfaces):
          self.screen.blit(line, (self.screen_width / 2 - 400, self.screen_height / 2 - 200 + i * 50))
        for i, choice in enumerate(self.choices):
          self.screen.blit(choice, (self.screen_width / 2 - 400, self.screen_height / 2 - 100 + len(self.question_text_surfaces) * 50 + i * 50))

        self.screen.blit(self.answer_input.surface, (self.screen_width / 2 - self.answer_input.surface.get_rect().width / 2, self.screen_height / 2 - 100 + len(self.question_text_surfaces) * 50 + len(self.choices) * 50))
        self.answer_input.update(events)
        
        self.screen.blit(self.answer_image, self.answer_image_rect)

      # handle cooldown for player question
      current_time: float = time.time()

      if current_time - self.initial_time > self.cooldown:
        self.player.protected = False


      # handle connection progress bar
      if self.connected and self.download <= 1:
        self.screen.blit(self.download_progress_text, (20, self.screen_height - 80))

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(20, self.screen_height - 50, 500, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(20, self.screen_height - 50, 500 * self.download, 20))

        self.download_progress_text = self.label.render(f'Téléchargement du devoir en cours ({round(self.download * 100)}%) - {self.wifi_speed / 1000}Gbits/s', False, (255, 255, 255))

        if not self.is_answering:
          self.download += self.wifi_speed / 10000000
      # when the download is done, then we switch to the win screen
      if self.download >= 1:
        self.current_screen = 4

      
      # loop through each events
      for event in events:
        # if user quit
        if event.type == pygame.QUIT:
          running = False

        # if user press key
        elif event.type == pygame.KEYDOWN:
          # e
          # trigger the book or the phone
          if event.key == pygame.K_e and not self.is_answering:
            if self.near_book:
              self.book.toggle_object()
            if self.near_phone and not self.phone.is_displayed:
              self.phone.toggle_object()
          # close the book or the phone
          if event.key == pygame.K_x and not self.is_answering:
            if self.near_book and self.book.is_displayed:
              self.book.toggle_object()
            if self.near_phone and self.phone.is_displayed:
              self.phone.toggle_object()
      
        # if user clicked on a button
        elif event.type == pygame.MOUSEBUTTONDOWN:
          # user clicked on the start button
          if self.start_image_rect.collidepoint(event.pos) and self.current_screen == 1:
            # start music
            pygame.mixer.music.play(-1)
            self.current_screen = 2
          # user clicked on the synopsis button
          if self.synopsis_image_rect.collidepoint(event.pos) and self.current_screen == 1:
            self.current_screen = 5
          # user clicked the connect button
          if self.submit_image_rect.collidepoint(event.pos) and self.current_screen == 2:
            # check if the user input is the same as the wifi password
            if self.password_input.value == self.wifi_pass:
              self.connected = True
          # user clicked on validate answer
          if self.answer_image_rect.collidepoint(event.pos) and self.current_screen == 2:
            if not self.answer_input.value == '': 
              self.check_answer()
          # user clicked on restart
          if self.restart_image_rect.collidepoint(event.pos) and (self.current_screen == 3 or self.current_screen == 4):
            self.__init__()
          # user clicked on validate answer
          if self.menu_image_rect.collidepoint(event.pos) and self.current_screen == 5:
            self.current_screen = 1

      # refresh at each frame
      pygame.display.flip()

      # set to 60 fps
      clock.tick(60)
      
      if not self.current_screen == 2:
        pygame.display.update()

    pygame.quit()
