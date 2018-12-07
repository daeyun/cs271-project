import othello

def minimax(state, depth):
	legalMoves = state.generateLegalMoves()
	bestScore = float("-inf") # Start as maxPlayer (you)
	bestMove = None
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = minPlayer(successor, depth-1) # Switch to opponent (minPlayer)
		if bestMove is None or score > bestScore:
			bestMove = move
			bestScore = score
	return bestMove
	
def minPlayer(state, depth):
	if depth == 0 or state.gameOver():
		return heuristic(state)
	legalMoves = state.generateLegalMoves()
	bestScore = float("inf")
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = maxPlayer(successor, depth-1) # Switch to maxPlayer
		if score < bestScore:
			bestScore = score
	return bestScore
	
def maxPlayer(state, depth):
	if depth == 0 or state.gameOver():
		return heuristic(state)
	legalMoves = state.generateLegalMoves()
	bestScore = float("-inf")
	for move in legalMoves:
		successor = state.makeMove(move) # This should return a new state, not change the one passed in
		score = minPlayer(successor, depth-1) # Switch to minPlayer
		if score > bestScore:
			bestScore = score
	return bestScore
