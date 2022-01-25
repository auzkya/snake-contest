from game import SnakeGame

from participants import martin, ester, frantisek, jana, sarka, tobias, laura, dominika, kylian, adam

game = SnakeGame(20, 20, 30, 150)
#game.add_human_player('Human 1', '#bbff00', ['d','w','a','s'])
game.add_ai_player('Martin', '#ff0000', martin.AI())
game.add_ai_player('Ester', '#ff00dd', ester.AI())
game.add_ai_player('Frantisek', '#eeaa33', frantisek.AI())
game.add_ai_player('Jana', '#3399cc', jana.AI())
game.add_ai_player('Sarka', '#cccccc', sarka.AI())
game.add_ai_player('Tobias', '#aaaa33', tobias.AI())
game.add_ai_player('Laura', '#ffffff', laura.AI())
game.add_ai_player('Dominika', '#333333', dominika.AI())
game.add_ai_player('Kylian', '#880088', kylian.AI())
game.add_ai_player('Adam', '#66ff00', adam.AI())
#game.add_ai_player('Filip', '#88ff88', filip.AI())

game.start()

