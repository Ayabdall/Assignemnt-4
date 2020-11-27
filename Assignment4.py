import random
import math

class Mancala:
	regular_board = [4,4,4,4,4,4,0,
					 4,4,4,4,4,4,0]

	test_board = [0,0,0,0,2,0,0,
			 	  0,0,0,0,0,1,50]

	def print_board(self, board):
			for i in range (6):
				print(i+1, end=" ")
			print("\n")
			for i in range(len(board)):
				if i > 7: print(board[i], end="")
				elif (i == 7) : print("\n" + str(board[i]), end="")
				else : print(board[i], end="")
				print(" ",end="")
			print("\n")
			for i in range (6):
				print(i+1, end=" ")

	def has_moves(self, board, player):
			if player == 1:
				for i in range(6):
					if board[i]:
						return(True)
					else: pass
			if player == 2:
				for i in range(6):
					if board[i+7]:
						return(True)
					else: pass
			return False		

	def move(self, board, player): #This obviously was not sustainable
			player = player
			while True:
				print("\nPlayer " + str(player), end=" ")
				choice = input("Please choose a move from 1 to 6 ")
				if(not choice.isdigit()) : print("Invalid move")
				elif(choice.isdigit()) :
					choice = int(choice)
					if(choice<1 or choice>6): print("Invalid move")
					elif(not (choice<1 or choice>6)):
						if player == 1:
							choice = choice-1
						elif player == 2:
							choice = choice+6
						if board[choice] == 0: print("Invalid move, Please pick a non empty cell")
						else:
							temp = board[choice]
							board[choice] = 0
							for i in range(temp):
								diff = temp-i
								counter = (choice+i+1)%14
								board[counter] += 1
								if diff == 1:
									if (counter != 6 and counter != 13):
										if( (board[counter]-1) == 0 ):
											if( board[(counter+7)%14] ):
												if player == 1 : board[6] = board[(counter+7)%14]
												elif player == 2 : board[13] = board[(counter+7)%14]
												board[(counter+7)%14] = 0
									if( counter == 6 or counter == 13):
										if player == 1: 
											if self.has_moves(board,1) : player = 1
											elif self.has_moves(board,2) : player = 2
											else : player = 0
										elif player == 2: 
											if self.has_moves(board,2) : player = 2
											elif self.has_moves(board,1) : player = 1
											else : player = 0
									else:
										if player == 1 : 
											if self.has_moves(board,2) : player = 2
											elif self.has_moves(board,1) : player = 1
											else : player = 0
										elif player == 2 : 
											if self.has_moves(board,1) : player = 1
											elif self.has_moves(board,2) : player = 2
											else : player = 0
							return player

	def take_input(self,board,player):
		while True:
				print("\nPlayer " + str(player), end=" ")
				choice = input("Please choose a move from 1 to 6 ")
				if(not choice.isdigit()) : print("Invalid move")
				elif(choice.isdigit()) :
					choice = int(choice)
					if(choice<1 or choice>6): print("Invalid move")
					elif(not (choice<1 or choice>6)):
						if player == 1:
							choice = choice-1
						elif player == 2:
							choice = choice+6
						if board[choice] == 0: print("Invalid move, Please pick a non empty cell")
						else:
							return(choice)

	def distribute(self,board,player,choice):
		end = board[choice]
		board[choice] = 0
		i = 1
		while i <= end:
			counter = (choice+i)%14
			if player == 1:
				if counter != 13:
					board[counter] += 1
					i += 1
				elif counter == 13:
					i+=1
					end +=1
					counter = (choice+i)%14
					board[counter] += 1
					i+=1
			if player == 2:
				if counter != 6:
					board[counter] += 1
					i += 1
				elif counter == 6:
					i+=1
					end +=1
					counter = (choice+i)%14
					board[counter] += 1
					i+=1

		return(board,counter)

	def eat(self, board, player, counter):
		eat = False
		if player == 1:
			if (counter < 6):
				if board[counter] == 1:
					if(board[(counter+7)%14]):
						board[6] += board[(counter+7)%14]
						board[(counter+7)%14] = 0
						eat = True

		elif player == 2:
			if (counter >= 7 and counter < 13):
				if board[counter] == 1:
					if (board[(counter+7)%14]):
						board[13] += board[(counter+7)%14]
						board[(counter+7)%14] = 0
						eat = True
		return eat

	def extra_turn(self, board, player, counter):
		extra = False
		if player == 1:
			if counter == 6:
				extra = True
				return 1,extra
			else: return 2, extra
		elif player == 2:
			if counter == 13:
				extra = True
				return 2,extra
			else: return 1, extra

	def find_avail_moves (self, board, player):
		moves = []
		if player == 1:
			for i in range(6):
				if board[i]:
					moves.append(i)
				else: pass
		if player == 2:
			for i in range(6):
				if board[i+7]:
					moves.append(i+7)
				else: pass
		return(moves)		

	def random_choice(self,board, player):
		choice = random.choice(self.find_avail_moves (board, player))
		return choice

	def pick_best_move(self, board, player):
		best = 0
		moves = self.find_avail_moves (board, player)
		for i in moves:
			temp_board = board.cop()
			self.distribute(temp_board, player, i)
			if player == 1:
				if temp_board[6] > best:
					best = temp_board[6]
					choice = i
			elif temp_board[13] > best:
					best = temp_board[13]
					choice = i
		return choice

	def alpha_beta(self, board, player):
		big_arr = [[board,0]]
		for i in range(3):
			for i in big_arr:
				moves = self.find_avail_moves(big_arr.pop()[0],player)
				for j in moves:
					temp_board = board.copy()
					new_board = self.new_move_bot(temp_board, player, j)
					big_arr.append(new_board)

	def which_bot(self, board, mode, player):
		if mode == 1:
			choice = self.random_choice(board,player)
		if mode == 2:
			choice = self.random_choice(board, player)
		return choice

	def Tournment(self, player,mode, bot,board):
		if not bot:
			if player == 1:
				choice = self.take_input(board,player)
			elif player == 2:
				if mode == 1:
					choice = self.which_bot(board, mode, player)
				if mode == 0:
					choice = self.take_input(board,player)
		else:
			if player == 1:
				if mode == 1:
					choice = self.which_bot(board,mode,player)
				elif mode == 2:
					choice = self.which_bot(board,mode,player)
			if player == 2:
				if bot == 1:
					choice = self.which_bot(board,bot,player)
				elif bot == 2:
					choice = self.which_bot(board,mode,player)
		return choice

	def new_move_bot(self, board, player, choice):
		board, counter = self.distribute(board, player, choice)
		eat = self.eat(board, player, counter)
		player, extra = self.extra_turn(board,player,counter)
		return(board)

	def new_move(self, board, player, mode, bot):
		choice = self.Tournment( player,mode, bot,board)
		board, counter = self.distribute(board, player, choice)
		eat = self.eat(board, player, counter)
		player, extra = self.extra_turn(board,player,counter)
		self.print_board(board)
		return(player)

	def play(self, board, mode,bot):
		player = 1
		self.print_board(board)
		while True:
			if(self.has_moves(board, player)):
				pass
			else:
				if player == 1:
					if(self.has_moves(board, 2)): player = 2
					else: player = 0
				elif player == 2:
					if(self.has_moves(board, 1)): player = 1
					else: player = 0
			
			if player == 0: break
			player = self.new_move(board, player, mode, bot)

def pick(player_cards, player):
	# print("player "+str(player)+"'s available cards are : ")
	print(*player_cards)
	while(True):
		# move = int(input("P1 please pick an available card \n"))
		move = int(input())
		if move in player_cards:
			return(move)
		else:
			print("invalid card, please try again")

def check(p1,p2,draw,i,p1_score,p2_score,discard):
	if(p1==p2):
		if discard :
			print("draw")
		else:
			print("draw")
			draw.append(i)
	else:
		if(p1 > p2):
			print("P1 won")
			if not draw:
				p1_score+=i
			else:
				p1_score += i
				for j in draw:
					p1_score+= j
				draw = []
		elif(p2 > p1):
			print("P2 won")
			if not draw:
				p2_score+=i
			else:
				p2_score += i
				for j in draw:
					p2_score+= j
				draw = []
		else:
			print("error")
	return(p1_score,p2_score)

def pick_random(player_cards):
	move = random.choice(player_cards)
	print("Computer's move "+str(move))
	return(move)

def pick_highest(player_cards, draw_card):
	move = max(player_cards)
	print("Computer's move "+str(move))
	return(move)

def pick_buckets(player_cards, draw_card):
	move = 0
	if (draw_card < 14 and draw_card > 10):
		move = max(player_cards)
	elif(draw_card < 11 and draw_card > 7):
		move = max([card for card in player_cards if (card < 11 and card > 7)])
	elif(draw_card < 8 and draw_card > 4):
		move = max([card for card in player_cards if (card < 8 and card > 4)])
	elif (draw_card < 5):
		move = max([card for card in player_cards if (card < 5)])
	print("Computer's move "+str(move))
	return(move)

def pick_same(player_cards, draw_card):
	move = draw_card
	print("Computer's move "+str(move))
	return(move)

def pick_same_plus_one(player_cards, draw_card): # what inspired pick cheat. They're practically the same function but passing p1 into draw card
	move = 0
	x = draw_card+1
	if x in player_cards:
		move = x
	else:
		move = max(player_cards)
	print("Computer's move "+str(move))
	return(move)

def pick_cheat_max(player_cards, p1):
	move = 0
	draw_card = p1
	x = draw_card+1
	if x in player_cards:
		move = x
	else:
		move = max(player_cards)
	print("Computer's move "+str(move))
	return(move)

def pick_cheat_min(player_cards, p1): #WHATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
	# WHEN THIS PLAYS AGAINST PICK SAME THEY ALWAYS GET THE SAME SCORE REGARDLESSSS ?????????????????????????????????????????????????????????????????????
	#okay I think I understand why now lol
	# THIS ONE KICKS ***********************
	# this consistently gets the highest scores with no draws while minimizing losses.
	# Player one only gets one card which is the king card and that's it. Whenever player 1 plays it, player 2 automaticlly plays a one.
	move = 0
	draw_card = p1
	x = draw_card+1
	if x in player_cards:
		move = x
	else:
		move = min(player_cards)
	print("Computer's move "+str(move))
	return(move)

def pick_cheat_same(player_cards, p1): #gets less scores than cheat min because of the draw and doesn't consistantly have all the best cards
	move = 0
	draw_card = p1
	x = draw_card+1
	if x in player_cards:
		move = x
	else:
		if p1 in player_cards:
			move = p1
		else:
			move = min(player_cards)
	print("Computer's move "+str(move))
	return(move)

def func(draw_card, this_player_cards, other_player_cards, this_player_score, other_player_score, turn, total):
	move = 0
	if turn == 1: # first turn
		if draw_card >= 7:
			half = math.ceil(draw_card/2)
			move = max([card for card in this_player_cards if (card <= half and card > 1)])
		elif draw_card == 1:
			move = 1
		elif draw_card == 2:
			move = 2
		else:
			move = random.choice([card for card in this_player_cards if (card <= 4 and card > 1)])
	else: #anything other than the first turn
		if draw_card <= 5:
			x = draw_card+1
			if x in this_player_cards:
				move = x
			elif draw_card in this_player_cards:
				move = draw_card
			else:
				move = min(this_player_cards)
		else:
			score_diff = abs(other_player_score-this_player_score)
			abs_diff = []
			x = 0
			abs_modified = []
			for i in other_player_cards:
				abs_diff.append(abs(draw_card - i)+1) # + math.ceil(turn/4)

			for i in abs_diff:
				abs_modified.append(i ** (-1))
			
			Mx = max(abs_modified)

			for i in range(len(abs_modified)):
				if abs_modified[i] == Mx:
					x = i

			for i in range(len(abs_modified)):
				abs_modified[i] **= 10
				abs_modified[i] *= max(0, (i-x))

			print(abs_modified)
			print(this_player_cards)
			move = random.choices(this_player_cards,weights=abs_modified)[0]

			if move > draw_card + 1 :
				pass
			elif move < draw_card + 1:
				if move == draw_card :
					pass
				else:
					move = min(this_player_cards)
					for i in range(len(this_player_cards)):
						if move == this_player_cards[i]:
							if i == len(this_player_cards):
								pass
							else:
								move = this_player_cards[i]
			elif move == draw_card:
				pass

	print(move)
	print("Computer's move "+str(move))
	return(move)

# predict what the other player will play, and If you hava a card higher that then play it, if you don't then play a card that minimizes the difference between you and the oponent or thier gain by getting a draw
# if
# gain = max(won card * min while keeping it at least one if possible ((mine-his)))
# else if you don't have a card higher than his, then maximize the difference between your card and his card
# however this openes up a problem of the enemy player thinking two steps ahead and realizing that you would play the lowest card you have and just playing one higher HMMMMMM

def play():
	cntr = 1
	total = 0
	p1=0
	p2=0
	draw =[]
	p1_cards = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	p1_score = 0
	p2_cards = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	p2_score = 0
	draw_cards = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	random.shuffle(draw_cards)

	for i in draw_cards:
		print("\n")
		print("Current card : " + str(i), end="")
		if not draw:
			print("")
		else:
			print(" and ", end="")
			print(*draw)
		print("Current turn : " + str(cntr))

		p1 = pick(p1_cards,1)
		p2 = func(i, p2_cards, p1_cards, p1_score,p2_score,cntr,total)

		p1_score, p2_score = check(p1,p2,draw,i,p1_score,p2_score,True)
		cntr+=1

		p1_cards.remove(p1)
		p2_cards.remove(p2)

	return(p1_score,p2_score)

print("welcome, what game would you like to play")
while True:
	x = input("enter 1 to play GOPS or 2 to play Mancala")
	if(not x.isdigit()) : print("Invalid move")
	elif(x.isdigit()) :
		x = int(x)
		if x == 1:
			p1_score = 0
			p2_score = 0
			avg = 0
			games = input("how many games would you like to play?")
			if(not games.isdigit()) : print("Invalid move")
			elif(games.isdigit()) :
				games = int(games)

			for i in range(games):
				curr_p1_score, curr_p2_score = play()
				p1_score += curr_p1_score
				p2_score += curr_p2_score

				print ("p1 score " + str(p1_score))
				print ("p2 score " + str(p2_score))
			print("thank you for playing")
			break
		elif x == 2:
			new_board = Mancala()
			new_board.play(new_board.regular_board,0,0)
			print("thank you for playing")
			break