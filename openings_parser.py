import sys

def loadFromFile(filename):
	print("  [OpeningsParser] read openings from file=" + filename)
	file_in_lines = readFile(filename)
	
	if formatCheck(file_in_lines):
		print("  [OpeningsParser] format check ok!")
	else:
		sys.exit()
	
	return parseOpenings(file_in_lines)	


def readFile(filename):
	# read in the openings file
	file_in_lines = []
	f = open(filename, "r")
	for x in f:
		file_in_lines.append(x)
	f.close()
	print("  [OpeningsParser] successfully read file, got " + str(len(file_in_lines)) + " lines")
	return file_in_lines


def saveToFile(hashmap, filename):
	# empty the file
	f = open(filename, "w")
	f.write("")
	f.close()
	
	# save every entry of the hashmap to the file
	f = open(filename, "a")
	for k in hashmap.keys():
		f.write("" + k + "=" + str(hashmap[k]) + "\n")
	f.close()
	print("  [OpeningsParser] successfully saved hashmap to file=" + filename)
	

def loadPreformatted(filename):
	# if it was parsed and saved before, we can skip parsing and just load it from the save file
	map_entries = readFile(filename)
	hashmap = {}
	for i in range(len(map_entries)):
		entry = map_entries[i].strip()
		
		# separate name from moves by "="
		if not len(entry.split("=")) == 2:
			print("Malformatted save file, expected '=' in line " + i)
			sys.exit()
			
		key = (entry.split("=")[0]).strip()
		array = (entry.split("=")[1]).strip()
		
		# parse array from string
		if not array.startswith("[") or not array.endswith("]"):
			print("Malformatted save file, expected '[' and ']' in line " + i)
			sys.exit()
		moves = array.replace("'", "").replace("[","").replace("]","").replace(" ","").split(",")
		
		hashmap[key] = moves
	return hashmap


def formatCheck(file_line_array):
	file_as_string = ""
	for x in file_line_array:
		file_as_string = file_as_string + x
	
	# sanity checks: all openings are there (A-E, 00-99 each)
	for letter in range(65, 70): # ascii codes of A-E
		for number1 in range(10):
			for number2 in range(10):
				opening_name = "" + chr(letter) + str(number1) + str(number2)
				if not opening_name in file_as_string:
					print("  [OpeningsParser] WARNING: could not find expected opening " + opening_name)
	
	for line in file_line_array:
		is_line_ok = False
		
		if line.strip() == "|-":
			is_line_ok = True
		
		if line.strip().startswith("*"):
			is_line_ok = True
		
		if line.strip().startswith("|") and len(line.strip().split("||")) == 3:
			is_line_ok = True
		
		# TODO more checks
		
		if not is_line_ok:
			print("  [OpeningsParser] ERROR: malformed line: " + line)
			return False	
		
	return True


def translateAlgebraicGermanToEnglish(move):
	# for a single move, translate the german (Short) Algebraic Notation to the english one
	move = move.replace("B", "P") # Bauer = Pawn
	move = move.replace("S", "N") # Springer = Knight
	move = move.replace("L", "B") # Laeufer = Bishop
	move = move.replace("T", "R") # Turm = Rook
	move = move.replace("D", "Q") # Dame = Queen
	move = move.replace("K", "K") # Koenig = King
	return move

def parseMoveslist(moves, additionalMoves = ""):
	moveslist = []
	
	movesstring = ""
	if "..." in additionalMoves:
		movesstring = moves + additionalMoves.split("...")[1]
	else:
		movesstring = moves + " " + additionalMoves
	movesstring = movesstring.strip()
	#print(movesstring + "\n")
	
	#for i in range(len(movesstring.split(" "))):
	#	if movesstring.split(" ")[i].endswith(".") and i % 3 == 0: # number in a place we dont expect
	#		print("Weird move in opening ")
	#		return []
	
	for part in movesstring.split(" "):
		if not part.endswith("."):
			moveslist.append(translateAlgebraicGermanToEnglish(part))
	#print(moveslist)
	
	return moveslist

def extractOneliner(string, hashmap):
	# | MANE || MOVES || [OPTIONAL MOVES]
	# e.g.:
	# | A25 || 1. c4 e5 2. Sc3 Sc6 || 3. g3 g6 4. Lg2 Lg7 5. e3
	
	line_as_array = string.split("||")
	
	if len(line_as_array) == 2 or len(line_as_array[2].strip()) == 0: # no variations given
		name = line_as_array[0][1:].strip()
		hashmap[name] = parseMoveslist(line_as_array[1].strip())
	elif not len(line_as_array[2].replace(" ", "")) == 0: #single variation given
		# mainline
		name = line_as_array[0][1:].strip() 
		hashmap[name] = parseMoveslist(line_as_array[1].strip())
		
		#mainline + variation
		name = line_as_array[0][1:].strip() + "b" 
		hashmap[name] = parseMoveslist(line_as_array[1].strip(), line_as_array[2].strip())
	

def parseOpenings(line_array):
	# extract the openings and variants
	openings = {} # hashmap, name is the key and the value is a moves array
	
	# oneliner have "|-" in the line before and after, multiliner have * at the beginning of every additional line
	last_multiliner_header = ""
	multilineindex = 0
	for i in range(1, len(line_array)-1):
		if "|-" in line_array[i-1] and "|-" in line_array[i+1]:
			extractOneliner(line_array[i], openings)
		else:
			if not "|-" in line_array[i]:
				#print("multiliner part in line " + str(i))
				if not "*" in line_array[i]:
					last_multiliner_header = line_array[i]
					multilineindex = 0
				else:
					name = last_multiliner_header.split("||")[0][1:].strip() + chr(97 + multilineindex) 
					openings[name] = parseMoveslist(last_multiliner_header.split("||")[1].strip(), line_array[i].replace("*","").strip())
					multilineindex = multilineindex + 1
					#print("multimove line " + name + ": " + str(openings[name]))

	print("  [OpeningsParser] found " + str(len(openings.keys())) + " openings")
	#print(openings.keys())
	return openings