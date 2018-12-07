def alphaBeta(state, depth):
	legalMoves = state.generateLegalMoves()
	bestScore = float("-inf") # Start as maxPlayer (you)
	bestMove = None
	alpha = float("-inf")
	beta = float("inf")
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = minPlayer(successor, depth-1, alpha, beta) # Switch to opponent (minPlayer)
		if score > alpha:
			alpha = score # Update lower bound for maxPlayer
		if bestMove is None or score > bestScore:
			bestMove = move
			bestScore = score
	return bestMove
	
def minPlayer(state, depth, a, b):
	if depth == 0 or state.gameOver():
		return heuristic(state)
	legalMoves = state.generateLegalMoves()
	bestScore = float("inf")
	alpha = a
	beta = b
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = maxPlayer(successor, depth-1, alpha, beta) # Switch to maxPlayer
		if score < beta:
			beta = score  # Update upper bound for minPlayer
		if alpha >= score:
			return min(bestScore, score) # Prune rest of the moves
		if score < bestScore:
			bestScore = score
	return bestScore
	
def maxPlayer(state, depth, a, b):
	if depth == 0 or state.gameOver():
		return heuristic(state)
	legalMoves = state.generateLegalMoves()
	bestScore = float("-inf")
	alpha = a
	beta = b
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = minPlayer(successor, depth-1, alpha, beta) # Switch to minPlayer
		if score > alpha:
			alpha = score # Update lower bound for maxPlayer
		if beta <= score:
			return max(bestScore, score) # Prune rest of the moves
		if score > bestScore:
			bestScore = score
	return bestScore