# -*- coding: utf-8 -*-
from tkinter import *
from random import randint, shuffle
from datetime import *
import os

def minus_players_points(player):
    # pro razeni. Radime sestupne podle bodu.
    # V pripade rovnosti vzestupne podle jmena.
    return (-player.points, player.name) 

class SnakeGame:
  def __init__(self, field_size, height, width, delay):
    self.field_size = field_size
    self.width = width
    self.height = height
    self.delay = delay
    self.window = Tk()
    self.window.title('snake')
    self.canvas=Canvas(
      self.window,
      width = (self.width + 1) * self.field_size,
      height = (self.height + 1) * self.field_size,
      bg = '#000000'
    )
    self.canvas.pack()
    self.keys = []
    self.window.bind('<KeyPress>', self.key_press)
    self.window.bind('<KeyRelease>', self.key_release)

    self.game_ended = False
    self.snakes = []
    self.dead = []
    self.food = []
    self.create_food()
    self.turn_number = 0

  def add_snake(self, snake):
    self.snakes.append(snake)

  def create_food(self):
    x = randint(0, self.width)
    y = randint(0, self.height)
    if (self.is_occupied(x, y)):
      self.create_food()
      return
    self.food.append([x, y])
    
  def key_press(self, event):
    if not event.keysym in self.keys:
      self.keys.append(event.keysym)
    for snake in self.snakes:
      snake.zmena_smeru(self.keys)

  def key_release(self, event):
    self.keys.remove(event.keysym)

  def evaluate_state(self):
    self.game_ended = False
    for snake in self.snakes:
      if (snake.points < -30):
        print('vyrazen hrac: ' + str(snake.name))
        self.snakes.remove(snake)
        snake.smrt()
        self.dead.append(snake)
      if (snake.points > 30):
        self.game_ended = True
    if (len(self.snakes) <= 1):
      self.game_ended = True
    if (self.game_ended):
      if not os.path.exists('vysledky'):
        os.makedirs('vysledky')
      file_name = 'vysledky/vysledek' + str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S')) + '.txt'
      with open(file_name,'w') as file:
        file.write(file_name + '\n')
        for snake in self.dead:
          file.write(str(snake.name) + ': ' + str(snake.points) + '\n')
        for snake in self.snakes:
          file.write(str(snake.name) + ': ' + str(snake.points) + '\n')
          print(str(snake.name) + ': ' + str(snake.points))
        print('Konec hry. Vysledek zapsan do ' + file_name)

  def akce(self):
    self.turn_number = self.turn_number + 1
    shuffle(self.snakes) # pohyb hadu se vyhodnoti v nahodnem poradi
    for snake in self.snakes:
      snake.akce()
    self.evaluate_state()
    self.rerender()
    for snake in self.snakes:
      if(isinstance(snake, player_AI)):
        snake.update(self.snakes)

    if (not self.game_ended):
      self.window.after(self.delay, self.akce)

  def rerender(self):
    self.canvas.delete(ALL)
    for snake in self.snakes:
      self.render_snake(snake)
    self.render_food()
    self.render_state()

  def render_food(self):
    for coordinates in self.food:
      x = coordinates[0]
      y = coordinates[1]
      field_size = self.field_size
      self.canvas.create_rectangle(x * field_size, y * field_size,
                                   (x+1) * field_size, (y + 1) * field_size,
                                   fill='#eeee88')

  def render_state(self):
    self.snakes.sort(key = minus_players_points)
    for i in range(len(self.snakes)):
      snake = self.snakes[i]
      self.canvas.create_text(
        20,
        (i + 1) * self.field_size,
        text = str(snake.name) + ' ' + str(snake.points),
        fill=snake.color,
      )

  def render_snake(self, snake):
    for coordinates in snake.tail:
      x = coordinates[0]
      y = coordinates[1]
      size = self.field_size
      self.canvas.create_rectangle(
        x * size, y * size,
        (x + 1) * size, (y + 1) * size,
        fill = snake.color,
      )

  def is_occupied(self, x, y):
    if x >= self.width:
      return True
    if x < 0:
      return True
    if y >= self.height:
      return True
    if y < 0:
      return True
    for snake in self.snakes:
      for clanek in snake.tail:
        if (clanek == [x,y]):
          return True
    return False

class Snake(object):
  def __init__(self, app, length, color, name, klavesy_pohyb):
    self.a = app
    self.length = length
    self.color=color
    self.name=name
    self.keys_pohyb = klavesy_pohyb
    self.points = 0
    self.time_of_death = -1
    self.revive()

  def collision(self):
    self.points = self.points - 10
    self.revive()

  def move(self,smer):
    if smer == 0 and self.x < self.a.width:        # doprava
      self.x = self.x + 1
    elif smer == 1 and self.y > 0:                 # nahoru
      self.y = self.y - 1
    elif smer == 2 and self.x > 0:                 # doleva
      self.x = self.x - 1
    elif smer == 3 and self.y < self.a.height:      # dolu
      self.y = self.y + 1
    else:
      self.collision()
      return
    if (self.a.is_occupied(self.x,self.y)):
      self.collision()
    self.tail.append([self.x,self.y])
    for i in range(len(self.a.food)):
      clanek = self.a.food[i]
      if (clanek == [self.x,self.y]):
        self.food_eaten(i)
        return
    while(len(self.tail) > self.length):
      self.tail.pop(0) 

  def food_eaten(self,i):
    self.length = self.length + 3
    self.points = self.points + 1
    self.a.food.pop(i)
    self.a.create_food()
  
  def revive(self):
    self.x=randint(0, self.a.width)
    self.y=randint(0, self.a.height)
    self.smer=randint(0, 3)
    self.tail = [[self.x, self.y]]
    self.length = 5

  def zmena_smeru(self, klavesy):
    for i in range(4):
        if (self.keys_pohyb[i] in klavesy):
          self.smer = i
    print (self.smer)

  def akce(self):
    self.move(self.smer)
  
  def smrt(self):
    self.time_of_death = self.a.turn_number

class Snake_AI(Snake):
  def __init__(self,aplikace, length, color, name, klavesy, ai):
    Snake.__init__(self,aplikace, length, color, name, klavesy)
    self.ai = ai

  def zmena_smeru(self, klavesy):
    for i in range(4):
        if (self.keys_pohyb[i] in klavesy):
          self.smer = i

  def update(self, snakes):
      self.smer = self.ai.novy_smer(self, snakes)