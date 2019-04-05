from Grid_3       import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_3   import PlayerAI
from Displayer_3  import Displayer
from GameManager_3 import *
import time
import random

f= open("results.txt","a")
i = 0
result = []
while i <= 30: 
    playerAI    = PlayerAI()
    computerAI  = ComputerAI()
    displayer   = Displayer()
    gameManager = GameManager(4, playerAI, computerAI, displayer)

    maxTile     = gameManager.start()
    result.append(maxTile)
    f.write(str(maxTile))
    f.write("\n")
    i+=1
print(result)