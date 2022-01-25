from direction import LEFT, UP, RIGHT, DOWN

class AI:
  def __init__(self):
    self.fields = [['']]
    self.height = 1
    self.width = 1

  def is_free(self, row, col, direction=None):
    if direction == LEFT: col -= 1
    elif direction == UP: row -= 1
    elif direction == RIGHT: col += 1
    elif direction == DOWN: row += 1

    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False

    if self.fields[row][col] == '': return True
    if self.fields[row][col] == 'f': return True
    else: return False

  # Funkce dostane seznam seznamů stringů fields. Záznam fields[i][j] říká,
  # co je na políčku na řádku i ve sloupci j. Možné hodoty jsou 'f', což značí jídlo,
  # prázdný string '' což značí prázdné pole, 'h' značí hlavu hada, pro nějž se rozhodujete
  # a cokoli dalšího znamená tělo nějakého hada. To je záznam ve formátu '4-arnost'.
  # Číslo před pomlčkou značí, o kolikátý díl těla se jedná (hlava je 0) a zbytek za pomlčkou
  # je jméno daného hada.
  # Tuto funkci můžete libovolně upravit. Jenom zachovejte její název a vstupní parametry
  # a vracejte jedině jednu z hodnot LEFT, UP, RIGHT, DOWN
  # Můžete přidat jakékoli další funkce.

  def decide_direction(self, fields):
    self.fields = fields
    self.height = len(fields)
    self.width = len(fields[0])
    head_row, head_col = 0, 0
    food_row, food_col = 0, 0
    for i in range(self.height):
      for j in range(self.width):
        if fields[i][j] == 'f':
          food_row, food_col = i, j
        if fields[i][j] == 'h':
          head_row, head_col = i, j

    if food_row < head_row and self.is_free(head_row, head_col, UP):
      return UP
    elif food_col < head_col and self.is_free(head_row, head_col, LEFT):
      return LEFT
    elif food_row > head_row and self.is_free(head_row, head_col, DOWN):
      return DOWN
    elif food_col > head_col and self.is_free(head_row, head_col, RIGHT):
      return RIGHT

      
    print('PANIC!!!')
    return LEFT
