import copy

def alphaBeta(state, depth, player):
	legalMoves = state.get_legal_moves(player)
	# state.print()
	# print('Current Player: ', player)
	# print('All legal moves from this position: ', legalMoves)
	bestScore = float("-inf") # Start as maxPlayer (you)
	bestMove = None
	alpha = float("-inf")
	beta = float("inf")
	for move in legalMoves:
		successor = copy.deepcopy(state)
		successor.make_move(move, player, play_test=False)
		score = minPlayer(successor, depth-1, alpha, beta, player) # Switch to opponent (minPlayer)
		if score > alpha:
			alpha = score # Update lower bound for maxPlayer
		if bestMove is None or score > bestScore:
			bestMove = move
			bestScore = score
	return bestMove
	
def minPlayer(state, depth, a, b, player):
	if depth == 0:
		return heuristic(state, player)
	legalMoves = state.get_legal_moves(player)
	opponent = state.get_opponent(player)
	if len(legalMoves) == 0:
		return maxPlayer(state, depth-1, a, b, player) # If no legal moves, skip turn
	bestScore = float("inf")
	alpha = a
	beta = b
	for move in legalMoves:
		successor = copy.deepcopy(state)
		successor.make_move(move, opponent, play_test=False)
		score = maxPlayer(successor, depth-1, alpha, beta, player) # Switch to maxPlayer
		if score < beta:
			beta = score  # Update upper bound for minPlayer
		if alpha >= score:
			return min(bestScore, score) # Prune rest of the moves
		if score < bestScore:
			bestScore = score
	return bestScore
	
def maxPlayer(state, depth, a, b, player):
	if depth == 0:
		return heuristic(state, player)
	legalMoves = state.get_legal_moves(player)
	if len(legalMoves) == 0:
		return maxPlayer(state, depth-1, a, b, player) # If no legal moves, skip turn
	bestScore = float("-inf")
	alpha = a
	beta = b
	for move in legalMoves:
		successor = copy.deepcopy(state)
		successor.make_move(move, player, play_test=False)
		score = minPlayer(successor, depth-1, alpha, beta, player) # Switch to minPlayer
		if score > alpha:
			alpha = score # Update lower bound for maxPlayer
		if beta <= score:
			return max(bestScore, score) # Prune rest of the moves
		if score > bestScore:
			bestScore = score
	return bestScore


def weighted_heuristic(state, player):
	weights = [
		120, -20, 20, 5, 5, 20, -20, 120,
		-20, -40, -5, -5, -5, -5, -40, -20,
		20, -5, 15, 3, 3, 15, -5, 20,
		5, -5, 3, 3, 3, 3, -5, 5,
		5, -5, 3, 3, 3, 3, -5, 5,
		20, -5, 15, 3, 3, 15, -5, 20,
		-20, -40, -5, -5, -5, -5, -40, -20,
		120, -20, 20, 5, 5, 20, -20, 120,
	]
	return state.get_weighted_sum(weights, player)


def heuristic(state, player):
	assert player in ('W', 'B')
	return weighted_heuristic(state, player)
