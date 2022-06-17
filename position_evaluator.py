import sys
import chess
from stockfish import Stockfish
import os.path

from progress_bar import ProgressBar

def ratePositions(openings, loaded_ratings, save_path, exe_path, params, depth, elo):
	# stockfish for all complicated stuff
	stockfish = Stockfish(exe_path, parameters=params)
	stockfish.set_depth(depth)
	stockfish.set_elo_rating(elo)

	# other chess library for converting notations (short algebraic to coordinate notation, because that is what stockfish wants)
	cleared_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
	board = chess.Board(cleared_fen)

	position_ratings = {} # key is name and value is rating
	
	f = open(save_path, "a")

	pb = ProgressBar(i=0, i_max=len(openings.keys()), prefix = "  ", suffix = "", length = 50)
	pb.draw(0)
	pb.time()
	
	for i in range(len(openings.keys())):	
		keys_list = list(openings)
		opening_name = keys_list[i]
		
		# if we already rated this before, we can skip it
		if opening_name in loaded_ratings:
			position_ratings[opening_name] = loaded_ratings[opening_name]
			pb.draw(i+1)
			continue
		
		# reset boards
		stockfish.set_fen_position(cleared_fen)
		board = chess.Board(cleared_fen)
		
		# translate using other chess board
		moves = openings[opening_name]
		translated_moves = []
		moves_legal = True
		for move in moves:
			try:
				translated_move = str(board.parse_san(move))
				translated_moves.append(translated_move)
				board.push_san(translated_move)
			except:
				print("  [Evaluator] ERROR: INVALID MOVE in opening " + opening_name + ", move " + move + ", " + str(sys.exc_info()[0]) + ": " + str(moves))
				moves_legal = False
				break
		if not moves_legal:
			pb.time()
			pb.draw(i+1)
			continue
		
		stockfish.set_position(translated_moves)
		score = stockfish.get_evaluation()
		position_ratings[opening_name] = score.get('value')
		f.write("" + opening_name + "=" + str(score.get('value')) + "\n")
		
		pb.time()
		pb.draw(i+1)
	
	f.close()
	return position_ratings


def readFile(filename):
	if not os.path.isfile(filename):
		f = open(filename, "w")
		f.write("")
		f.close()
	
	# read in the ratings file
	file_in_lines = []
	f = open(filename, "r")
	for x in f:
		file_in_lines.append(x)
	f.close()
	print("  [Evaluator] successfully read save file, got " + str(len(file_in_lines)) + " lines")
	return file_in_lines


def loadRatings(filename):
	# if it was evaluated and saved before, we can skip evaluation and just load it from the save file
	map_entries = readFile(filename)
	hashmap = {}
	for i in range(len(map_entries)):
		entry = map_entries[i].strip()
		
		# separate name from moves by "="
		if not len(entry.split("=")) == 2:
			print("Malformatted save file, expected '=' in line " + i)
			sys.exit()
			
		key = (entry.split("=")[0]).strip()
		value = (entry.split("=")[1]).strip()
		hashmap[key] = float(value)
	return hashmap
