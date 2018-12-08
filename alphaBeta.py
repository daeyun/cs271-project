def alphaBeta(state, depth, player):
	legalMoves = state.get_legal_moves(player)
	bestScore = float("-inf") # Start as maxPlayer (you)
	bestMove = None
	alpha = float("-inf")
	beta = float("inf")
	opponent = None
	if player == 'W': # This is maxPlayer
		opponent = 'B' # This is minPlayer
	elif player == 'B': # This is maxPlayer
		opponent = 'W' # This is minPlayer
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = minPlayer(successor, depth-1, alpha, beta, opponent) # Switch to opponent (minPlayer)
		if score > alpha:
			alpha = score # Update lower bound for maxPlayer
		if bestMove is None or score > bestScore:
			bestMove = move
			bestScore = score
	return bestMove
	
def minPlayer(state, depth, a, b, player):
	if depth == 0 or state.gameOver():
		return heuristic(state)
	legalMoves = state.get_legal_moves(player)
	if len(legalMoves) == 0:
		return maxPlayer(state, depth, a, b) # If no legal moves, skip turn
	bestScore = float("inf")
	alpha = a
	beta = b
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = maxPlayer(successor, depth-1, alpha, beta, player) # Switch to maxPlayer
		if score < beta:
			beta = score  # Update upper bound for minPlayer
		if alpha >= score:
			return min(bestScore, score) # Prune rest of the moves
		if score < bestScore:
			bestScore = score
	return bestScore
	
def maxPlayer(state, depth, a, b, player):
	if depth == 0 or state.gameOver():
		return heuristic(state)
	legalMoves = state.get_legal_moves(player)
	if len(legalMoves) == 0:
		return maxPlayer(state, depth, a, b) # If no legal moves, skip turn
	bestScore = float("-inf")
	alpha = a
	beta = b
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = minPlayer(successor, depth-1, alpha, beta, opponent) # Switch to minPlayer
		if score > alpha:
			alpha = score # Update lower bound for maxPlayer
		if beta <= score:
			return max(bestScore, score) # Prune rest of the moves
		if score > bestScore:
			bestScore = score
	return bestScore
