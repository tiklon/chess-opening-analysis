import openings_parser as op
from tree_node import TreeNode
import position_evaluator as pe
import visualizer

OPENINGS_RAW_FILE = "data/openings_raw.txt"
OPENINGS_PARSED_FILE = "data/openings_parsed.txt"
STOCKFISH_EXE_PATH = "E:/Programme/Stockfish/stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe"
STOCKFISH_THREADS = 16
STOCKFISH_DEPTH = 15
STOCKFISH_RATING = 3600
RATINGS_SAVE_FILE_PREFIX = "data/ratings"
GAME_TREE_OUT_FILE_NAME = "game_tree.pdf"


def main(op_in, op_out, skip_parse, rate_out, sf_path, sf_threads, sf_depth, sf_rating, tree_path, dontSave, dontShow):
	print("_" * 60 + "\nStep 1: Loading the openings from file ...")
	if skip_parse:
		openings = op.loadPreformatted(op_out)
	else:
		openings = op.loadFromFile(op_in)
	op.saveToFile(openings, op_out)

	print("_" * 60 + "\nStep 2: Evaluating all end-positions ...")
	loaded_ratings = pe.loadRatings(rate_out)
	position_ratings = pe.ratePositions(openings, loaded_ratings, rate_out, sf_path, {"Threads": sf_threads, "Minimum Thinking Time": 1}, sf_depth, sf_rating)

	# apply game theory: extensive form game i.e. building a game-tree
	print("_" * 60 + "\nStep 3: Building the game-tree from the openings and their ratings...")
	root = TreeNode()
	for opening_name in openings.keys():
		moves = openings[opening_name]
		current_node = root
		
		if not opening_name in position_ratings:
			continue
		
		for move in moves:
			if current_node.has_child_with_move(move):
				current_node = current_node.get_child(move)
			else:
				current_node.add_child(move)
				current_node = current_node.get_child(move)
				
		current_node.opening_name = opening_name
		current_node.score = position_ratings[opening_name]
				
	print("  [TreeBuilding] build a Game-Tree with a total of " + str(root.count_nodes_recursive()) + " nodes and " + str(root.count_leaves()) + " leafs")

	# now to the analysis results
	print("_" * 60 + "\nStep 4: analysis on the game-tree ...")
	good_good = root.get_best_opening_white_good_black_good()
	good_bad = root.get_best_opening_white_good_black_bad()
	bad_good = root.get_best_opening_white_bad_black_good()
	bad_bad = root.get_best_opening_white_bad_black_bad()
	print("  The best opening if both play perfect is " + good_good[0] + " with a centipawn rating of " + str(good_good[1]) + "\n  - " + str(openings[good_good[0]]) + "\n")
	print("  The best opening for white if black is bad is " + good_bad[0] + " with a centipawn rating of " + str(good_bad[1]) + "\n  - " + str(openings[good_bad[0]]) + "\n")
	print("  The best opening for black if white is bad is " + bad_good[0] + " with a centipawn rating of " + str(bad_good[1]) + "\n  - " + str(openings[bad_good[0]]) + "\n")
	print("  The best opening if both try really hard to lose is " + bad_bad[0] + " with a centipawn rating of " + str(bad_bad[1]) + "\n  - " + str(openings[bad_bad[0]]) + "\n")


	# visualising the resulting game tree with ete3
	tree = visualizer.makeTree(root)
	if not dontSave:
		visualizer.saveToFile(tree, tree_path)
	if not dontShow:
		visualizer.show(tree)
	

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
	parser.add_argument('--OPin', metavar='path', required=False, default=OPENINGS_RAW_FILE,
						help='the path to the un-parsed, raw openings file')
	parser.add_argument('--OPout', metavar='path', required=False, default=OPENINGS_PARSED_FILE,
						help='the path to the parsed openings file or output destination')
	parser.add_argument('--skipParse', required=False, action='store_true',
						help='to skip parsing and take "--op-out" of a previous run as input')
	parser.add_argument('--ratingOut', metavar='path', required=False, default=RATINGS_SAVE_FILE_PREFIX,
						help='the path prefix of the ratings output file, will be extended by e.g. "_depth_15.txt" depending on the Stockfish depth')
	parser.add_argument('--sfPath', metavar='path', required=False, default=STOCKFISH_EXE_PATH,
						help='the path to the exe file of stockfish')
	parser.add_argument('--sfThreads', metavar='int', required=False, default=STOCKFISH_THREADS,
						help='number of threads that stockfish will run on')
	parser.add_argument('--sfDepth', metavar='int', required=False, default=STOCKFISH_DEPTH,
						help='depth that stockfish will calculate to')
	parser.add_argument('--sfRating', metavar='int', required=False, default=STOCKFISH_RATING,
						help='ELO-rating that stockfish will use')
	parser.add_argument('--treePath', metavar='path', required=False, default=GAME_TREE_OUT_FILE_NAME,
						help='the path to the game-tree that this program will produce')
	parser.add_argument('--dontSave', required=False, default=False, action='store_true',
						help='to not save the game-tree to file')
	parser.add_argument('--dontShow', required=False, default=False, action='store_true',
						help='to not show the resulting game-tree in a pop-up window')
						
						
	args = parser.parse_args()
	main(op_in=args.OPin,
		 op_out=args.OPout,
		 skip_parse=args.skipParse,
		 rate_out=args.ratingOut+"_depth_"+str(args.sfDepth)+".txt",
		 sf_path=args.sfPath,
		 sf_threads=args.sfThreads,
		 sf_depth=args.sfDepth,
		 sf_rating=args.sfRating,
		 tree_path=args.treePath,
		 dontSave= args.dontSave,
		 dontShow= args.dontShow)