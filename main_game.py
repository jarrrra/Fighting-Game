# -*- coding: utf-8 -*-
import random
import sys
import time
import os

#-----------------------------------------------------------------------

#Main class for all characters
class Customer:
  #Construtor
  def __init__(self, name, age, inventory, lang, s_dmg):
    self.__name__ = name
    self.__age__ = age
    self.__lang__ = lang
    self.__s_dmg__ = s_dmg
    self.__anger__ = 0
    self.__dmg__ = 0
    self.inventory = inventory
    self.hp = 100

  #**************************

  #Get name
  def get_name(self):
    return self.__name__

  #Get age
  def get_age(self):
    return self.__age__

  #Get anger
  def get_anger(self):
    return self.__anger__

  #Set anger
  def set_anger(self, anger):
    self.__anger__ = anger

  #Get damage
  def get_dmg(self):
    return self.__s_dmg__

  #Set damage
  def set_dmg(self, dmg):
    self.__s_dmg__ = dmg

  #**************************

  #Set health based on age
  def health(self):
    if self.__age__ > 50:
      self.hp -= 15
    elif self.__age__ < 30:
      self.hp += 15
    self.hp_saver = self.hp

  #Increase anger
  def get_angrier(self, a):
    self.__anger__ += a

  #Decrease anger
  def calm_down(self, a):
    self.__anger__ -= a

  #**************************

  #Define kick attack
  def kick(self, person):
    global target
    global action
    global amount

    if self.__anger__ >= 10:
      self.__dmg__ = 20
    elif self.__anger__ >= 5:
      self.__dmg__ = 15
    else:
      self.__dmg__ = 10
    self.__dmg__ += self.__s_dmg__

    if self == target and action != "":
      if action == "DMG+":
        self.__dmg__ += amount
      if action == "DMG*":
        self.__dmg__ *= amount

    if self.__lang__ == 0:
      print(self.__name__, ' пнул(а) персонажа ', person.get_name(),
            ' и нанес(ла) ', self.__dmg__, ' урона!')
    else:
      print(self.__name__, ' just kicked ', person.get_name(), ' and dealt ',
            self.__dmg__, ' damage!')
    return self.__dmg__

  #**************************

  #Define slap attack
  def slap(self, person):
    global target
    global action
    global amount

    if self.__anger__ >= 10:
      self.__dmg__ = 15
    elif self.__anger__ >= 5:
      self.__dmg__ = 10
    else:
      self.__dmg__ = 5
    self.__dmg__ += self.__s_dmg__

    if self == target:
      if action == "DMG+":
        self.__dmg__ += amount
      elif action == "DMG*":
        self.__dmg__ *= amount

    if self.__lang__ == 0:
      print(self.__name__, ' дал(а) пощёчину персонажу ', person.get_name(),
            ' и нанес(ла) ', self.__dmg__, ' урона!')
    else:
      print(self.__name__, ' just slapped ', person.get_name(), ' and dealt ',
            self.__dmg__, ' damage!')
    return self.__dmg__

  #**************************

  #Define punch attack
  def punch(self, person):
    global target
    global action
    global amount

    if self.__anger__ >= 10:
      self.__dmg__ = 25
    elif self.__anger__ >= 5:
      self.__dmg__ = 20
    else:
      self.__dmg__ = 15
    self.__dmg__ += self.__s_dmg__

    if self == target:
      if action == "DMG+":
        self.__dmg__ += amount
      elif action == "DMG*":
        self.__dmg__ *= amount

    if self.__lang__ == 0:
      print(self.__name__, ' ударил(а) персонажа ', person.get_name(),
            ' и нанес(ла) ', self.__dmg__, ' урона!')
    else:
      print(self.__name__, ' just punched ', person.get_name(), ' and dealt ',
            self.__dmg__, ' damage!')
    return self.__dmg__

  #**************************

  #Define missed attack
  def miss(self, person):
    if self.__lang__ == 0:
      print(self.__name__, ' промахнулся(ась)!')
    else:
      print(self.__name__, ' just missed!')
    self.__dmg__ = 0
    return self.__dmg__

  #**************************

  #Define counterattack
  def counterattack(self, dm):
    chance = random.choice([1, 2, 2, 1, 1, 2])
    if chance == 1 and dm != 0:
      dm = dm // 2
      dm = random.choice([dm, dm + 2, dm + 1, dm, dm + 4, dm + 3, dm])
      return dm
    else:
      self.__dmg__ = 0
      return self.__dmg__

  #**************************

  #Choosing which attack happens
  def technique(self, person):
    if self.hp >= 85:
      tech_choice = random.uniform(0, 1)
      if action != "":
        if tech_choice <= 0.05:
          self.tech = self.miss
        elif tech_choice <= 0.55:
          self.tech = self.kick
        else:
          self.tech = random.choice([self.slap, self.punch])
      else:
        if tech_choice <= 0.1:
          self.tech = self.miss
        elif tech_choice <= 0.4:
          self.tech = self.kick
        else:
          self.tech = random.choice([self.slap, self.punch])
    if self.hp >= 50:
      tech_choice = random.uniform(0, 1)
      if tech_choice <= 0.15:
        self.tech = self.miss
      elif tech_choice <= 0.4:
        self.tech = self.kick
      else:
        self.tech = random.choice([self.slap, self.punch])
    if self.hp < 50:
      tech_choice = random.uniform(0, 1)
      if tech_choice <= 0.25:
        self.tech = self.miss
      elif tech_choice <= 0.4:
        self.tech = self.kick
      else:
        self.tech = random.choice([self.slap, self.punch])

    self.tech(person)

    if self.tech == self.miss:
      if self.hp <= 35:
        self.get_angrier(4)
      else:
        self.get_angrier(2)
    else:
      if self.hp <= 35:
        self.get_angrier(2)
      else:
        self.get_angrier(1)
    return self.__dmg__

#-----------------------------------------------------------------------

#Class for player character, inheriting from Customer class
class Player(Customer):

  #Construtor
  def __init__(self, name, age, inventory, lang, s_dmg):
    super().__init__(name, age, inventory, lang, s_dmg)

  #**************************

  #Define heal screen
  def heal(self):
    if self.__lang__ == 0:
      self.__inv__ = [{
          'name': 'Яблоко',
          'hp': 10,
          'price': 1
      }, {
          'name': 'Тост с маслом',
          'hp': 15,
          'price': 2
      }, {
          'name': 'Куриная грудка',
          'hp': 25,
          'price': 3
      }, {
          'name': 'Торт (полностью восстанавливает здоровье)',
          'hp': self.hp_saver - self.hp,
          'price': 10
      }]
    else:
      self.__inv__ = [{
          'name': 'Apple',
          'hp': 10,
          'price': 1
      }, {
          'name': 'Toast with butter',
          'hp': 15,
          'price': 2
      }, {
          'name': 'Chicken breast',
          'hp': 25,
          'price': 3
      }, {
          'name': 'Cake (restores full hp)',
          'hp': self.hp_saver - self.hp,
          'price': 10
      }]
    ch = 0
    if self.__lang__ == 0:
      print('\n\nВыберите способ лечения (0 для выхода)')
    else:
      print('\n\nChoose how you want to heal (0 to exit):')
    if self.__anger__ == 0:
      if self.__lang__ == 0:
        print('\n\nНедостаточно злости')
      else:
        print('\n\nNot enough anger')
      return ch
    print('\n\n')
    n = 1
    for item in self.__inv__:
      if self.__lang__ == 0:
        print(n, '.', item['name'], ' восстанавливает ', item['hp'],
              ' и стоит ', item['price'], ' злости')
      else:
        print(n, '.', item['name'], ' restores ', item['hp'], ' and costs ',
              item['price'], ' of anger')
      n += 1
    ch = int(input().strip())
    if ch == 0:
      return ch
    if ch > len(self.__inv__) or ch < 0:
      if self.__lang__ == 0:
        print('Неверный ответ')
      else:
        print('Answer is incorrect')
      return self.heal()
    else:
      time.sleep(1)
      clean()
      if (self.__anger__ - self.__inv__[ch - 1]['price']) >= 0:
        self.hp += self.__inv__[ch - 1]['hp']
        self.__anger__ -= self.__inv__[ch - 1]['price']
        if self.__lang__ == 0:
          print('Вы восстановили ', self.__inv__[ch - 1]['hp'],
                ' здоровья')
          print('Ваше здоровье:', self.hp)
        else:
          print('You healed ', self.__inv__[ch - 1]['hp'], ' hp')
          print('Your health:', self.hp, ' hp')
      else:
        if self.__lang__ == 0:
          print('\n\nНедостаточно злости')
        else:
          print('\n\nNot enough anger')
        ch = 0
        return ch

  #**************************

  #Health restore
  def increase_health(self, characters, type_of_action, amount_to_increase,
                      amount_to_loose, timer):
    if self.__lang__ == 0:
      print('\nВы восстановили здоровье!')
    else:
      print('\nYou healed!')
    if type_of_action == "+":
      self.hp = int(self.hp+amount_to_increase)
      int(self.hp)
      return "HP+", amount_to_loose, timer, self
    if type_of_action == "*":
      self.hp = int(self.hp*amount_to_increase)
      return "HP*", amount_to_loose, timer, self
    if type_of_action == "sofa":
      self.hp = int(self.hp*amount_to_increase)
      global sofa_timer
      sofa_timer += 1
      return "SOFA", amount_to_loose, timer, self

  #**************************

  #Temporarily increase anger
  def increase_anger(self, characters, type_of_action, amount_to_increase,
                     amount_to_loose, timer):
    if self.__lang__ == 0:
      print('\nВаш уровень злости повысился!')
    else:
      print('\nYour anger level raised!')
    if type_of_action == "+":
      self.__anger__ = int(self.__anger__+amount_to_increase)
      return "ANGER+", amount_to_loose, timer, self
    if type_of_action == "*":
      self.__anger__ = int(self.__anger__*amount_to_increase)
      return "ANGER*", amount_to_loose, timer, self

  #**************************

  #Temporarily incrase damage
  def increase_damage(self, characters, type_of_action, amount_to_increase,
                      amount_to_loose, timer):
    if self.__lang__ == 0:
      print('Ваш урон повысился!')
    else:
      print('Your damage increased!')
    if type_of_action == "+":
      return "DMG+", amount_to_loose, timer, self
    if type_of_action == "*":
      return "DMG*", amount_to_loose, timer, self

  #**************************

  #Freeze a random character
  def freeze(self, characters, type_of_action, amount_to_increase,
             amount_to_loose, timer):
    character = random.choice(characters)
    while character == characters[0]:
      character = random.choice(characters)

    if self.__lang__ == 0:
      print(character.get_name(), ' заморожен!')
    else:
      print(character.get_name(), ' is freezed!')
    return "FREEZE", amount_to_loose, timer, character

  #**************************

  #Add burn effect to a random character
  def burn(self, characters, type_of_action, amount_to_increase,
           amount_to_loose, timer):
    character = random.choice(characters)
    while character == characters[0]:
      character = random.choice(characters)

    if self.__lang__ == 0:
      print(character.get_name(), ' пылает!')
    else:
      print(character.get_name(), ' is on fire!')
    return "BURN", amount_to_loose, timer, character

  #**************************

  #Up defense of the player character
  def add_defense(self, characters, type_of_action, amount_to_increase,
                  amount_to_loose, timer):
    if self.__lang__ == 0:
      print('У Вас появилась защита!')
    else:
      print('You\'ve gained defense!')
    return "DEF", amount_to_increase, timer, self

  #**************************

  #Swap health of player and character with max health
  def swap(self, characters, type_of_action, amount_to_increase,
           amount_to_loose, timer):
    hp_holder = self.hp
    self.hp = characters.hp
    characters.hp = hp_holder

    if self.__lang__ == 0:
      print('Вы теперь человек с самым большим здоровьем!')
    else:
      print('You\'re now the person with the most hp!')
    return "SWAP", -1, 0, self

  #**************************

  #Define inventory screen
  def open_inventory(self, characters):
    global sofa_timer
    global fork

    if self.__lang__ == 0:
      self.__reaction__ = {
          'телевизор': [
              self.increase_anger,
              "Увеличивает злость на 10 единиц на 2 хода. По истечению времени злость уменьшается на 10 единиц.",
              characters, "+", 10, 10, 2
          ],
          'тостер': [
              self.increase_damage, "Увеличивает урон в 2 раза на 5 ходов.",
              characters, "*", 2, 2, 5
          ],
          'телефон': [
              self.increase_anger,
              "Увеличивает злость на 5 единиц на 2 хода. По истечению времени злость уменьшается на 5 единиц.",
              characters, "+", 5, 5, 2
          ],
          'холодильник': [
              self.freeze,
              "Замораживает рандомного персонажа на 3 хода и он(а) теряет 10 единиц здоровья. Во время заморозки персонаж не может атаковать.",
              characters, "", 0, 10, 3
          ],
          'бургер': [
              self.increase_health,
              "Восстанавливает 10% от всего здоровья.", characters, "+",
              0.1*self.hp_saver, -1, 0
          ],
          'гриль': [
              self.increase_health,
              "Восстанавливает 50% от всего здоровья.", characters, "+",
              0.5*self.hp_saver, -1, 0
          ],
          'картина': [
              self.swap,
              "Меняет местами здоровье игрока с персонажем с самым большим здоровьем.",
              max(characters, key=lambda x: x.hp), "", -1, 0, 0
          ],
          'книга': [
              self.increase_damage, "Увеличивает урон в 1.5 раз на 2 хода.",
              characters, "*", 1.5, 1.5, 3
          ],
          'диван': [
              self.increase_health,
              "Восстанавливает 60% от текущего здоровья, но игрок пропускает "
              + str(sofa_timer + 1) +
              " хода. Можно использовать бесконечное количество раз, но каждое использование прибавляет 1 к пропускаемым ходам.",
              characters, "sofa", 1.6, -1, sofa_timer
          ],
          'подушка': [
              self.add_defense,
              "Снижает получаемый урон на 2 единицы, держится 5 ударов.",
              characters, "", 2, 0, 5
          ],
          'стол': [
              self.increase_damage, "Увеличивает урон в 4 раза на 2 хода.",
              characters, "*", 4, 4, 2
          ],
          'свеча': [
              self.burn,
              "Поджигает рандомного персонажа на 3 раунда. Каждый раунд он(а) теряет по 3 единицы здоровья.",
              characters, "", 0, 3, 3
          ],
          'вилка': [
              self.increase_damage, "Увеличивает урон на 2 единицы до конца игры.",
              characters, "+", 2, -1, 0
          ]
      }
    else:
      self.__reaction__ = {
          'TV': [
              self.increase_anger,
              "Increases anger by 10 for 2 turns. Decreases anger by 10 after the time runs out.",
              characters, "+", 10, 10, 2
          ],
          'toaster': [
              self.increase_damage, "Increases damage by 2x for 5 turns.",
              characters, "*", 2, 2, 5
          ],
          'telephone': [
              self.increase_anger,
              "Increases anger by 5 for 2 turns. Decreases anger by 5 after the time runs out.",
              characters, "+", 5, 5, 2
          ],
          'fridge': [
              self.freeze,
              "Freezes a random character for 3 turns and they lose 10 hp. During freeze, the character cannot attack.",
              characters, "", 0, 10, 3
          ],
          'burger': [
              self.increase_health, "Restores 10% from full health.",
              characters, "+", 0.1*self.hp_saver, -1, 0
          ],
          'grill': [
              self.increase_health, "Restores 50% from full health.",
              characters, "+", 0.5*self.hp_saver, -1, 0
          ],
          'painting': [
              self.swap,
              "Swaps hp of the player with and the character who has the most hp.",
              max(characters, key=lambda x: x.hp), "", -1, 0, 0
          ],
          'book': [
              self.increase_damage, "Increases damage by 1.5x for 2 turns.",
              characters, "*", 1.5, 1.5, 3
          ],
          'sofa': [
              self.increase_health,
              "Restores 60% from current health, but the player skips " +
              str(sofa_timer + 1) +
              " turns. Can be used infinite times, but each use adds 1 to the skips.",
              characters, "sofa", 1.6, -1, sofa_timer
          ],
          'pillow': [
              self.add_defense,
              "Decreases damage by 2, the effect holds for 5 hits.",
              characters, "", 2, 0, 5
          ],
          'table': [
              self.increase_damage, "Increases damage by 4x for 2 turns.",
              characters, "*", 4, 4, 2
          ],
          'candle': [
              self.burn,
              "Lights up a random character for 3 rounds. Each round they lose 3 hp.",
              characters, "", 0, 3, 3
          ],
          'fork': [
              self.increase_damage, "Increase damage by 2 for the rest of the game.", characters, "+",
              2, -1, 0
          ]
      }

    ch = 0
    if self.__lang__ == 0:
      print('\n\nВыберите предмет для использования (0 для выхода)')
    else:
      print('\n\nChoose an item to use (0 to exit):')
    if len(self.inventory) == 0:
      if self.__lang__ == 0:
        print('\n\nВ инвентаре нет предметов')
      else:
        print('\n\nNo items in inventory')
      time.sleep(1)
      return "", -1, 0, self
    else:
      print('\n\n')
      n = 1
      for item in self.inventory:
        print(n, '.', item, ': ', self.__reaction__[item][1])
        n += 1
      ch = int(input().strip())
      if ch == 0:
        return "", -1, 0, self
      if ch > len(self.inventory) or ch < 0:
        if self.__lang__ == 0:
          print('Неверный ответ')
        else:
          print('Answer is incorrect')
        return self.open_inventory(characters)
      else:
        if self.__lang__ == 0:
          print('\n\nВы использовали ', self.inventory[ch - 1])
        else:
          print('\n\nYou used ', self.inventory[ch - 1])

        if self.inventory[ch - 1] == 'sofa' or self.inventory[ch -
                                                              1] == 'диван':
          item = self.__reaction__[self.inventory[ch - 1]]
        else:
          item = self.__reaction__[self.inventory.pop(ch - 1)]

        if item == "fork" or item == "вилка":
          fork = True
          self.__s_dmg__ += 2
        time.sleep(1)
        clean()
        return item[0](characters=item[2],
                       type_of_action=item[3],
                       amount_to_increase=item[4],
                       amount_to_loose=item[5],
                       timer=item[6])

#-----------------------------------------------------------------------

#Checking if someone died
def dead(customers, speed, name, lang, winner, round_count):
  for customer in customers:
    if customer.hp <= 0:
      if customer == customers[0]:
        time.sleep(speed)
        clean()
        if lang == 0:
          print('Вы умерли!')
          print('Ваши вещи:', end=" ")
        else:
          print('You died!')
          print('Your stuff:', end=" ")

        new_game(name, lang, round_count)
      else:
        if lang == 0:
          print('О боже, ', customer.get_name(), ' умер(ла).')
          print(winner.get_name(), ' получил(а) ', end="")
        else:
          print('Oh god, ', customer.get_name(), ' died.')
          print(winner.get_name(), ' got ', end="")

        printed_smth = False
        if len(customer.inventory) > 0:
            for i in customer.inventory:
              if winner.inventory.count(i) == 0:
                if (i == "fork" or i == "вилка") and fork:
                      continue
                  
                if printed_smth:
                    print(",", end=' ')
                print(i, end='')
                
                printed_smth = True
                winner.inventory.append(i)
        
        
        if not printed_smth:
          print("nothing")
        else:
            print("\n")

        customers.remove(customer)
        break

#-----------------------------------------------------------------------

#Fighting screen/Action choosing screen, player fighting
def fight(customers, speed, name, lang, round_count):
  global action
  global amount
  global timer
  global target
  global fork
  global writesave
  global inventory_save
  global sofa_timer

  time.sleep(speed)
  clean()
  if action == "SOFA":
    timer -= 1
    if lang == 0:
      print("Вы использовали диван и пропускаете ход ради здорового сна.")
    else:
      print("You used sofa and skipped a turn for a healthy rest.")
  else:
    f = 0
    for i in customers:
      if lang == 0:
        print(f, '. ', i.get_name(), ', ', i.get_age(), ' лет, ', i.hp,
              ' здоровья и ', i.get_anger(), ' злости')
      else:
        print(f, '. ', i.get_name(), ', ', i.get_age(), ' years old, ', i.hp,
              ' hp and ', i.get_anger(), ' anger')
      f += 1
    print('\n\n')
    if lang == 0:
      print('Ваше здоровье:', customers[0].hp)
      print('Ваша злость:', customers[0].get_anger())
      print('Что будете делать?(атака(а)/лечение(л)/инвентарь(и)/выйти(в))')
    else:
      print('Your health:', customers[0].hp, ' hp')
      print('Your anger:', customers[0].get_anger())
      print('What would you do?(fight(f)/heal(h)/inventory(i)/exit(e))')
    ans = input().strip()
    if ans == 'инвентарь' or ans == 'и' or ans == 'inventory' or ans == 'i':
      if timer <= 0:
        action, amount, timer, target = customers[0].open_inventory(customers)
        if action == "FREEZE":
          target.hp -= amount
          int(target.hp)
        if action == "":
          return fight(customers, speed, name, lang, round_count)
      else:
        if lang == 0:
          print('Вы не можете использовать инвентарь, пока не закончится таймер')
        else:
          print('You cannot use inventory, while the timer is not over')
        return fight(customers, speed, name, lang, round_count)
    elif ans == 'heal' or ans == 'h' or ans == 'лечение' or ans == 'л':
      ch = customers[0].heal()
      time.sleep(speed)
      if ch == 0:
        time.sleep(speed)
        return fight(customers, speed, name, lang, round_count)
    elif ans == 'exit' or ans == 'e' or ans == 'выйти' or ans == 'в':
      writesave = open(filename, "w")
      writesave.write(str(lang)+'\n')
      writesave.write(str(name)+'\n')
      writesave.write(str(round_count)+'\n')
      for x in inventory_save:
          writesave.write(x + ",")
      writesave.write('\n')
      writesave.write(str(fork)+'\n')
      writesave.write(str(sofa_timer)+'\n')
      writesave.close()
      sys.exit()
    elif ans == 'fight' or ans == 'f' or ans == 'атака' or ans == 'а':
      if lang == 0:
        print(
            'Выберите номер человека, которого вы хотите атаковать (0 для выхода)'
        )
      else:
        print('Choose number of a person you want to fight (0 to exit)')
      num = int(input().strip())
      if num == 0:
        return fight(customers, speed, name, lang, round_count)
      if num + 1 > len(customers) or num < 0:
        if lang == 0:
          print('Неверный ответ')
        else:
          print('Answer is incorrect')
        return fight(customers, speed, name, lang, round_count)
      print('\n\n')
      tq = customers[0].technique(customers[num])        
      customers[num].hp -= tq
      if lang == 0:
        print('У персонажа ', customers[num].get_name(), ' осталось ',
              customers[num].hp, ' здоровья')
      else:
        print(customers[num].get_name(), ' has ', customers[num].hp, ' health')
      if customers[num].hp <= 50 and customers[num].hp > 0 and (action != "FREEZE" or target != customers[num]):
        dm = customers[num].counterattack(tq)
        if dm == 0:
          pass
        else:
          for s in range(5):
            time.sleep(0.5)
            print('.')
          if lang == 0:
            print(customers[num].get_name(), ' контратакует! Он(а) наносит ', dm,
                  ' урона')
          else:
            print(customers[num].get_name(), ' counterattacks! It was ', dm,
                  ' damage')
          if action == "DEF":
            timer -= 1
            customers[0].hp -= (dm - amount)
          else:
            customers[0].hp -= dm
          if lang == 0:
            print('У персонажа ', customers[0].get_name(), ' осталось ',
                  customers[0].hp, ' здоровья')
          else:
            print(customers[0].get_name(), ' has ', customers[0].hp, ' health')
          dead(customers, speed, name, lang, customers[num], round_count)
      else:
        dead(customers, speed, name, lang, customers[0], round_count)
    else:
      if lang == 0:
        print('Неверный ответ')
      else:
        print('Answer is incorrect')
      return fight(customers, speed, name, lang, round_count)

  for i  in customers[1:]:
    if customers.count(i) == 0:
      continue

    for g in range(2):
      print('|')
    fight2(customers, speed, customers.index(i), name, lang, round_count)

  if timer > 0:
    if action != "DEF" and action != "SOFA":
      timer -= 1
      if action == "BURN":
        for g in range(2):
          print('|')
        if lang == 0:
          print(target.get_name(), ' горит. Ауч!')
        else:
          print(target.get_name(), ' is on fire. Ouch!')
        target.hp -= amount
        int(target.hp)
        dead(customers, speed, name, lang, customers[0], round_count)
  else:
    if action != "":
      if amount != -1:
        time.sleep(speed)
        for g in range(2):
          print('|')
        if action == "BURN":
          if lang == 0:
            print(target.get_name(), ' больше не горит!')
          else:
            print(target.get_name(), ' is no longer on fire!')
        if action == "FREEZE":
          if lang == 0:
            print(target.get_name(), ' больше не в заморозке!')
          else:
            print(target.get_name(), ' is no longer frozen!')
        if action == "HP+":
          if lang == 0:
            print('Здоровье понизилось! :(')
          else:
            print('Health decreased! :(')
          target.hp -= amount
          int(target.hp)
        if action == "HP*":
          if lang == 0:
            print('Здоровье понизилось! :(')
          else:
            print('Health decreased! :(')
          target.hp /= amount
          int(target.hp)
        if action == "DMG*" or action == "DMG+":
          if lang == 0:
            print('Урон понизился! :(')
          else:
            print('Damage decreased! :(')
        if action == "ANGER+":
          if lang == 0:
            print('Злость понизилась! :(')
          else:
            print('Anger decreased! :(')
          target.set_anger(target, int(target.get_anger() - amount))
        if action == "ANGER*":
          if lang == 0:
            print('Злость понизилась! :(')
          else:
            print('Anger decreased! :(')
          target.set_anger(target, int(target.get_anger() / amount))
      action = ""

#-----------------------------------------------------------------------

#Fighting for characters
def fight2(customers, speed, i, name, lang, round_count):
  global action
  global amount
  global timer
  global target
  global defense
  global sofa_timer

  num = random.choice(customers)
  if num == customers[i] or num == customers[0] and random.uniform(0,
                                                                   1) < 0.05:
    return fight2(customers, speed, i, name, lang, round_count)
  time.sleep(speed)
  if action == "FREEZE" and customers[i] == target:
    if lang == 0:
      print(customers[i].get_name(), ' в заморозке и не может сделать ход!')
    else:
      print(customers[i].get_name(), ' is frozen and can\'t do their turn!')
  else:
    tq = customers[i].technique(num)
    if num == customers[0] and action == "DEF":
      timer -= 1
      num.hp -= (tq - amount)
    else:
      num.hp -= tq
    if lang == 0:
      print('У персонажа ', num.get_name(), ' осталось ', num.hp, ' здоровья')
    else:
      print(num.get_name(), ' has ', num.hp, ' health')
    if num.hp <= 45:
      c = random.uniform(0, 1)
      if c <= 0.4:
        lose = random.choice([1, 2, 3, 4])
        if customers[i].get_anger() - lose < 0:
          pass
        else:
          customers[i].calm_down(lose)
          if lang == 0:
            print(customers[i].get_name(), ' потерял(а) ', lose, ' злости!')
          else:
            print(customers[i].get_name(), ' lost ', lose, ' anger!')
    if num.hp <= 50 and num.hp > 0 and (action != "FREEZE" or target != num):
      dm = num.counterattack(tq)
      if dm == 0:
        pass
      else:
        for s in range(5):
          time.sleep(0.5)
          print('.')
        if lang == 0:
          print(num.get_name(), ' контратакует! Он(а) наносит ', dm, ' урона')
        else:
          print(num.get_name(), ' counterattacks! It was ', dm, ' damage')
        customers[i].hp = customers[i].hp - dm
        if lang == 0:
          print('У персонажа ', customers[i].get_name(), ' осталось ',
                customers[i].hp, ' здоровья')
        else:
          print(customers[i].get_name(), ' has ', customers[i].hp, ' health')
        dead(customers, speed, name, lang, num, round_count)
    else:
      dead(customers, speed, name, lang, customers[i], round_count)

#-----------------------------------------------------------------------

#Choosing language for the game
def language():
  print('English(write eng/e)/Russian(write rus/r or рус/р)')
  lang = input().strip()
  if lang == 'rus' or lang == 'r' or lang == 'рус' or lang == 'р':
    lang = 0
  elif lang == 'eng' or lang == 'e':
    lang = 1
  else:
    print('Answer is incorrect/Неверный ответ')
    time.sleep(1)
    clean()
    return language()
  return lang

#-----------------------------------------------------------------------

#Cleaning the console
def clean():
  os.system('cls' if os.name == 'nt' else 'clear')

#-----------------------------------------------------------------------

#Main game function
def game(name, lang, round_count):
  global writesave
  global action
  global amount
  global timer
  global target
  global sofa_timer
  global fork
  global inventory_save

  action = ""
  amount = -1
  timer = 0
  target = None
  sofa_timer = 0

  clean()

  customers = []
  speed = 2

  inventory0 = [
      'телевизор', 'тостер', 'телефон', 'холодильник', 'бургер', 'гриль',
      'картина', 'книга', 'диван', 'подушка', 'стол', 'свеча', 'вилка'
  ]

  inventory1 = [
      'TV', 'toaster', 'telephone', 'fridge', 'burger', 'grill', 'painting',
      'book', 'sofa', 'pillow', 'table', 'candle', 'fork'
  ]

  names0 = [
      'Марина', 'Владислав', 'Александра', 'Владимир', 'Алина', 'Михаил',
      'Диана', 'Даниил', 'Екатерина', 'Петр', 'Дмитрий', 'Арина', 'Сюзанна',
      'Данила', 'Алексей', 'Анна', 'Сабрина', 'Евгений', 'Алена', 'Григорий',
      'Сергей', 'Виталий', 'Геннадий', 'Елена', 'Татьяна', 'Яна', 'Борис',
      'Константин', 'Василиса', 'Павел', 'Иванна', 'Лев', 'Лидия', 'Ольга',
      'Иван'
  ]

  names1 = [
      'Marie', 'Rodd', 'Sara', 'Bob', 'Ashley', 'Mike', 'Diana', 'Daniel',
      'Kate', 'Peter', 'Drake', 'Flora', 'Susie', 'Dan', 'Alex', 'Abigale',
      'Cloe', 'Jake', 'Afina', 'Gregory', 'Sam', 'Vincent', 'Gin', 'Helen',
      'Trevis', 'Fiona', 'Kel', 'Kevin', 'Aisha', 'Perry', 'Violet', 'Leo',
      'Lana', 'Bella', 'Duke'
  ]

  ages = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]

  if inventory_save.count("fork") > 0 or inventory_save.count("вилка") > 0:
      fork = False

  if lang == 0:
    player = Player(name, random.choice(ages), inventory_save, 0, 0)
  else:
    player = Player(name, random.choice(ages), inventory_save, 1, 0)

  if fork:
    player.set_dmg(player.get_dmg() + 2)

  customers.append(player)

  for i in range(3 + round_count):
    if lang == 0:
      customer = Customer(random.choice(names0), random.choice(ages),
                          [random.choice(inventory0)], 0, random.choice(range(round_count + 1)))
      names0.remove(customer.get_name())
    else:
      customer = Customer(random.choice(names1), random.choice(ages),
                          [random.choice(inventory1)], 1, random.choice(range(round_count + 1)))
      names1.remove(customer.get_name())
    customers.append(customer)

  for i in customers:
    i.health()
    i.hp_saver = i.hp
    i.calm_down(i.get_anger())

  if lang == 0:
    print('Уровень ', round_count + 1)
    print('\n\nВаше имя:', player.get_name(), '; Ваш возраст:',
          player.get_age(), ' лет; Ваше здоровье:', player.hp)
  else:
    print('Round ', round_count + 1)
    print('\n\nYour name:', player.get_name(), '; Your age:', player.get_age(),
          ' years old; Your health:', player.hp, ' hp')

  time.sleep(speed)

  while len(customers) > 1:
    fight(customers, speed, name, lang, round_count)

  time.sleep(speed)
  clean()
  if lang == 0:
    print('Вы выиграли')
    print('Ваши вещи:', end=" ")
  else:
    print('You won')
    print('Your stuff:', end=" ")
  if len(customers[0].inventory) > 0:
    for j in range(0, len(customers[0].inventory) - 1):
      print(customers[0].inventory[j], end=", ")
    print(customers[0].inventory[len(customers[0].inventory) - 1])

  inventory_save = customers[0].inventory

  round_count += 1
  if round_count > 7:
    round_count = 0
    inventory_save = []
    fork = False

  writesave = open(filename, "w")

  writesave.write(str(lang)+'\n')
  writesave.write(str(name)+'\n')
  writesave.write(str(round_count)+'\n')
  for x in inventory_save:
      writesave.write(x + ",")
  writesave.write('\n')
  writesave.write(str(fork)+'\n')
  writesave.write(str(sofa_timer)+'\n')
  writesave.close()

  new_game(name, lang, round_count)

#-----------------------------------------------------------------------

#Starting new game
def new_game(name, lang, round_count):
  global filename
  global writesave
  global sofa_timer
  global fork
  global inventory_save

  if round_count == 0:
    if lang == 0:
      print('Игра окончена! Хотите начать игру заново?(да(д)/нет(н))')
    else:
      print('Game end! Do you want to play again?(yes(y)/no(n))')
  else:

    if lang == 0:
      print('Хотите продолжить?(да(д)/нет(н))')
    else:
      print('Do you want to continue?(yes(y)/no(n))')
  answ = input().strip()
  if answ == 'yes' or answ == 'y' or answ == 'да' or answ == 'д':
    if round_count > 0:
        
        readsave = open(filename, "r")
    
        lang = int(readsave.readline().strip())
        name = str(readsave.readline().strip())
        round_count = int(readsave.readline().strip())
        inventory_save = readsave.readline().strip().split(',')
        inventory_save.remove('')
        fork = eval(readsave.readline().strip())
        sofa_timer = int(readsave.readline().strip())
    
        readsave.close()
        
    else:
        
        inventory_save = []
        fork = False
        sofa_timer = 0
        
    game(name, lang, round_count)
  elif answ == 'no' or answ == 'n' or answ == 'нет' or answ == 'н':
     writesave = open(filename, "w")
     writesave.write(str(lang)+'\n')
     writesave.write(str(name)+'\n')
     writesave.write(str(round_count)+'\n')
     for x in inventory_save:
         writesave.write(x + ",")
     writesave.write('\n')
     writesave.write(str(fork)+'\n')
     writesave.write(str(sofa_timer)+'\n')
     writesave.close()
     sys.exit()
  else:
    if lang == 0:
      print('Неверный ответ')
    else:
      print('Answer is incorrect')
    return new_game(name, lang, round_count)

#-----------------------------------------------------------------------

#When game has just started:

clean()

action = ""
amount = -1
timer = 0
target = None

speed = 2

filename = "savefile.txt"
try:
    readsave = open(filename, "r")

    try:
      lang = int(readsave.readline().strip())
      name = str(readsave.readline().strip())
      round_count = int(readsave.readline().strip())
      inventory_save = readsave.readline().strip().split(',')
      inventory_save.remove('')
      fork = eval(readsave.readline().strip())
      sofa_timer = int(readsave.readline().strip())
    except:
      raise FileNotFoundError

    readsave.close()

    while True:
        clean()
        if lang == 0:
            print("Здравствуйте, ", name, "!")
            print("Хотите продолжить, где остановились? (да(д)/нет(н))")
        else:
            print("Hello, ", name, "!")
            print("Do you want to continue where you left off? (yes(y)/no(n))")

        answ = input().strip()
        if answ == "да" or answ == "д" or answ == "y" or answ == "yes":
            clean()
            break;
        elif answ == "нет" or answ == "н" or answ == "no" or answ == "n":
            clean()
            raise FileNotFoundError
        else:
            if lang == 0:
                print("Неверный ответ")
            else:
                print("Answer is incorrect")
            time.sleep(1)
            clean()


#-----------------------------------------------------------------------

except InterruptedError:
    sys.exit()
    
#-----------------------------------------------------------------------

except FileNotFoundError:

    lang = language()
    clean()

    #**************************

    if lang == 0:
      print('Введите имя:')
    else:
      print('Fill in your name:')
    name = input().strip()

    #**************************

    round_count = 0
    inventory_save = []
    fork = False
    sofa_timer = 0

    #**************************
  
    #Tutorial
    if lang == 0:
      print('\n\nПоказать туториал?(да(д)/нет(н))')
    else:
      print('\n\nShow tutorial?(yes(y)/no(n))')
    t = input().strip()

    if t == 'yes' or t == 'y' or t == 'да' or t == 'д':
      if lang == 0:
        print(
            '\n\nСтандартное здоровье: 100. Если вы младше 30, то у вас оно равно 115, но если старше 50, то 85. \nВозраст выбирается случайно в начале каждого раунда.\n\nВаша цель - победить всех персонажей во всех 8 раундах.'
        )
        time.sleep(speed * 4)
        print(
            '\n\nПощёчина - 5 урона; \nПинок - 10 урона; \nУдар - 15 урона. \n\nЕсли злость больше 5 или 10, к урону персонажа добавляется 5 доп. урона.\n\nТоже самое работает и у других.\n\nПерсонажи могут промахнуться, игрок в том числе. Чем ниже здоровье, тем больше шанс промаха.'
        )
        time.sleep(speed * 5)

        print(
            '\n\nКогда здоровье равно 50 или ниже, персонажи могут контратаковать!\n\nКогда другие персонажи атакуют кого-то со здоровьем ниже 45, они могут потерять немного злости.'
        )

        time.sleep(speed * 4)

        print(
         '\n\nВ игре есть предметы для восстановления здоровья (присутствуют постоянно и тратят злость для использования) и предметы, которые можно получить в бою.\nКаждый полученный предмет имеет особое свойство и сохраняется в инвентаре между раундами.'     
       )

        time.sleep(speed * 6)
      else:
        print(
            '\n\nStandard health: 100 hp. If you are younger than 30, you have 115 hp, but if older than 50, you have 85 hp.\nYour age is randomly chosen at the beginning of each round.\n\nYour goal is to defeat all characters in all 8 rounds.'
        )
        time.sleep(speed * 4)
        print(
            '\n\nSlap - 5 dmg; \nKick - 10 dmg; \nPunch - 15 dmg. \n\nIf your anger is over 5 or 10, your dmg is increased by 5.\n\nSame works for others.\n\nCharacters can miss, player included. The lower your health, the more the chance of missing.'
        )
        time.sleep(speed * 5)

        print(
            '\n\nWhen health is 50 hp or less, characters can counterattack!\n\nWhen other characters attack someone with hp under 45, they have chance to loose some anger.'
        )

        time.sleep(speed * 4)

        print(
         '\n\nIn game there\'re objects to restore health (constant and spend anger when used) and objects that you can get during the fight.\nEvery aquired item has its own effect and stays in inventory between rounds.'   
       )

        time.sleep(speed * 6)

#-----------------------------------------------------------------------

#Starting the main part of the game
writesave = open(filename, "w")
writesave.write(str(lang)+'\n')
writesave.write(str(name)+'\n')
writesave.write(str(round_count)+'\n')
for x in inventory_save:
    writesave.write(x + ",")
writesave.write('\n')
writesave.write(str(fork)+'\n')
writesave.write(str(sofa_timer)+'\n')
writesave.close()
game(name, lang, round_count)