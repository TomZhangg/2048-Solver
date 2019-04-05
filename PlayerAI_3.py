#AIM: PLAYER_AI GETS THE NEXT MOVE FOR THE PLAYER 
#Heuristic source: http://ranjaykrishna.com/blog/can-an-artificial-intelligence-win-2048

import math 
import numpy as np
import random
from BaseAI_3 import BaseAI
from Grid_3 import *
import numpy as np
import time



def Free(grid):
	if TerminalTest(grid):
		return -np.inf
	grid = grid.map
	free = grid[0].count(0) + grid[1].count(0) + grid[2].count(0) + grid[3].count(0)
	return free

def Grad(grid):
	if TerminalTest(grid):
		return -np.inf

	TLHead = [
				[  4.5,    2,    1,    0],
				[    2,  1.5,    0,   -1],
				[    1,    0, -1.5,   -2],
				[    0,   -1,   -2, -3.5]
			 ]
	TRHead = [
				[    0,    1,    2,  4.5],
				[   -1,    0,  1.5,    2],
				[   -2, -1.5,    0,    1],
				[ -3.5,   -2,   -1,    0]
			 ]
	BLHead = [
				[    0,   -1,   -2, -3.5],
				[    1,    0, -1.5,   -2],
				[    2,  1.5,    0,   -1],
				[  4.5,    2,    1,    0]
			 ]
	BRHead = [
				[ -3.5,   -2,   -1,    0],
				[   -2, -1.5,    0,    1],
				[   -1,    0,  1.5,    2],
				[    0,    1,    2,  4.5]
			 ]


	TLHeadScore = 0
	TRHeadScore = 0
	BLHeadScore = 0
	BRHeadScore = 0

	for i in range(4):
		for j in range(4):
			TLHeadScore += TLHead[i][j]*grid.map[i][j]
			TRHeadScore += TRHead[i][j]*grid.map[i][j]
			BLHeadScore += BLHead[i][j]*grid.map[i][j]
			BRHeadScore += BRHead[i][j]*grid.map[i][j]

	score = max(TLHeadScore, TRHeadScore, BLHeadScore, BRHeadScore)
	return score

def Mono(grid):
	if TerminalTest(grid):
		return -np.inf

	Left = [
				[    2,    1,    0,   -1],
				[    2,    1,    0,   -1],
				[    2,    1,    0,   -1],
				[    2,    1,    0,   -1]
		   ]
	Top  = [
				[    2,    2,    2,    2],
				[    1,    1,    1,    1],
				[    0,    0,    0,    0],
				[   -1,   -1,   -1,   -1]
			 ]
	Right = [
				[   -1,    0,    1,    2],
				[   -1,    0,    1,    2],
				[   -1,    0,    1,    2],
				[   -1,    0,    1,    2]
			 ]
	Bottom = [
				[   -1,   -1,   -1,   -1],
				[    0,    0,    0,    0],
				[    1,    1,    1,    1],
				[    2,    2,    2,    2]
			 ]


	LeftScore = 0
	TopScore = 0
	RightScore = 0
	BottomScore = 0

	for i in range(4):
		for j in range(4):
			LeftScore += Left[i][j]*grid.map[i][j]
			TopScore += Top[i][j]*grid.map[i][j]
			RightScore += Right[i][j]*grid.map[i][j]
			BottomScore += Bottom[i][j]*grid.map[i][j]

	score = max(LeftScore, RightScore, TopScore, BottomScore)
	return score

def Eval(grid):
	score = 0
	score += Grad(grid) * 0.9 + Mono(grid) * 0.1 
	
	return score

def TerminalTest(grid):
	return not grid.canMove()

def Maximize(grid, alpha, beta, depth, start):
	if TerminalTest(grid) or depth == 0 or(time.clock()-start) >= 0.05:
		return Eval(grid)

	maxUtility =  -np.inf
	
	moves = grid.getAvailableMoves()
	for movetup in moves:
		child = movetup[1]
		maxUtility = max(maxUtility, Minimize(child, alpha, beta, depth-1, start))

		if maxUtility >= beta:
			break

		alpha = max(maxUtility, alpha)

	return maxUtility

def Expect(grid):
	total = 0

	availableCells = grid.getAvailableCells();
	
	if len(availableCells) == 0:
		return -np.inf

	for cellxy in availableCells:
		grid2 = grid.clone()
		grid2.insertTile(cellxy, 2)

		grid4 = grid.clone()
		grid4.insertTile(cellxy, 4)

		total += (0.1 * Eval(grid4)) + (0.9 * Eval(grid2))


	return total/len(availableCells)

def getAvalailbleMovesAdversary(grid):
	moves = []

	availableCells = grid.getAvailableCells();


	for cellxy in availableCells:
		grid2 = grid.clone()
		grid2.insertTile(cellxy, 2)
		grid4 = grid.clone()
		grid4.insertTile(cellxy, 4)
		
		moves.append(grid2)
		moves.append(grid4)

		
	return moves

def Minimize(grid, alpha, beta, depth, start):
	if TerminalTest(grid) or depth == 0 or (time.clock()-start) >= 0.05:
		return Expect(grid)

	minUtility = np.inf 

	moves = getAvalailbleMovesAdversary(grid)
	for child in moves:
		minUtility = min(minUtility, Maximize(child, alpha, beta, depth-1, start))
		
		if minUtility <= alpha:
			break

		beta = min(minUtility, beta)

	return minUtility

def Decision(grid):
	limit = 4
	start = time.clock()
	alpha = -np.inf
	beta = np.inf

	return Minimize(grid, alpha, beta, limit, start)

class PlayerAI(BaseAI):
	def getMove(self, grid):
		moves = grid.getAvailableMoves()
		maxUtility = -np.inf
		nextDir = 0
		for movetup in moves:
			move = movetup[0]
			child = movetup[1]

			utility = Decision(child) 

			if utility >= maxUtility:
				maxUtility = utility
				nextDir = move

		return nextDir


