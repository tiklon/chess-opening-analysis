class TreeNode(object):
	def __init__(self):
		self.move = None
		self.score = None
		self.parent = None
		self.childs = []
		self.opening_name = None
		self.depth = 0
	
	def has_child_with_move(self, searched_move):
		for child in self.childs:
			if searched_move in child.move:
				return True
		return False
	
	def add_child(self, move):
		child = TreeNode()
		child.parent = self
		child.move = move
		child.score = None
		child.depth = self.depth + 1
		self.childs.append(child)
	
	def get_child(self, searched_move):
		for child in self.childs:
			if searched_move in child.move:
				return child
				
	def count_nodes_recursive(self):
		i = 1
		for child in self.childs:
			i = i + child.count_nodes_recursive()
		return i
	
	def is_leaf(self):
		return len(self.childs) == 0
		
	def count_leaves(self):
		if self.is_leaf():
			return 1
		
		i = 0
		for child in self.childs:
			i = i + child.count_leaves()
		return i
	
	def get_all_nodes(self):
		tmp = [self]
		for child in self.childs:
			tmp = tmp + child.get_all_nodes()
		return tmp
		
	def get_all_leaves_recursive(self):
		tmp = []
		if self.is_leaf():
			tmp.append(self)
		else:
			for child in self.childs:
				tmp = tmp + child.get_all_leaves_recursive()
		return tmp
	
	def is_white_to_move(self):
		return self.depth % 2 == 0 # node depth even means white is to move (selecting a child), odd is black
		
	def get_best_opening_white_good_black_good(self):
		if self.is_leaf():
			return [self.opening_name, self.score]
		else:
			result = ["Name", 0]
			for child in self.childs:
				child_eval = child.get_best_opening_white_good_black_good()
				
				# scores in centipawn, positive is good for white and negative is good for black
				if result == ["Name", 0]:
					result = child_eval
				else:
					if self.is_white_to_move() and child_eval[1] > result[1]:
						result = child_eval
					elif self.is_white_to_move() and child_eval[1] < result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] > result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] < result[1]:
						result = child_eval
					else:
						result = child_eval
			
			if self.opening_name: # if not leave but still enging of a line: possibility to end here, i.e. take the value of this node instead of childs
				if self.is_white_to_move() and self.score and self.score > result[1]:
					result = [self.opening_name, self.score]
				elif not self.is_white_to_move() and self.score and self.score < result[1]:
					result = [self.opening_name, self.score]
			
			# print("move made to " + result[0] + " " + str(result[1]))
			return result
	
	def get_best_opening_white_bad_black_good(self):
		if self.is_leaf():
			return [self.opening_name, self.score]
		else:
			result = ["Name", 0]
			for child in self.childs:
				child_eval = child.get_best_opening_white_bad_black_good()
				
				# scores in centipawn, positive is good for white and negative is good for black
				if result == ["Name", 0]:
					result = child_eval
				else:
					if self.is_white_to_move() and child_eval[1] < result[1]:
						result = child_eval
					elif self.is_white_to_move() and child_eval[1] > result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] > result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] < result[1]:
						result = child_eval
					else:
						result = child_eval
			
			if self.opening_name: # if not leave but still enging of a line: possibility to end here, i.e. take the value of this node instead of childs
				if self.is_white_to_move() and self.score and self.score < result[1]:
					result = [self.opening_name, self.score]
				elif not self.is_white_to_move() and self.score and self.score < result[1]:
					result = [self.opening_name, self.score]
			
			# print("move made to " + result[0] + " " + str(result[1]))
			return result
	
	def get_best_opening_white_good_black_bad(self):
		if self.is_leaf():
			return [self.opening_name, self.score]
		else:
			result = ["Name", 0]
			for child in self.childs:
				child_eval = child.get_best_opening_white_good_black_bad()
				
				# scores in centipawn, positive is good for white and negative is good for black
				if result == ["Name", 0]:
					result = child_eval
				else:
					if self.is_white_to_move() and child_eval[1] > result[1]:
						result = child_eval
					elif self.is_white_to_move() and child_eval[1] < result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] < result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] > result[1]:
						result = child_eval
					else:
						result = child_eval
			
			if self.opening_name: # if not leave but still enging of a line: possibility to end here, i.e. take the value of this node instead of childs
				if self.is_white_to_move() and self.score and self.score > result[1]:
					result = [self.opening_name, self.score]
				elif not self.is_white_to_move() and self.score and self.score > result[1]:
					result = [self.opening_name, self.score]
			
			# print("move made to " + result[0] + " " + str(result[1]))
			return result
			
	def get_best_opening_white_bad_black_bad(self):
		if self.is_leaf():
			return [self.opening_name, self.score]
		else:
			result = ["Name", 0]
			for child in self.childs:
				child_eval = child.get_best_opening_white_bad_black_bad()
				
				# scores in centipawn, positive is good for white and negative is good for black
				if result == ["Name", 0]:
					result = child_eval
				else:
					if self.is_white_to_move() and child_eval[1] < result[1]:
						result = child_eval
					elif self.is_white_to_move() and child_eval[1] > result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] < result[1]:
						result = result
					elif not self.is_white_to_move() and child_eval[1] > result[1]:
						result = child_eval
					else:
						result = child_eval
			
			if self.opening_name: # if not leave but still enging of a line: possibility to end here, i.e. take the value of this node instead of childs
				if self.is_white_to_move() and self.score and self.score < result[1]:
					result = [self.opening_name, self.score]
				elif not self.is_white_to_move() and self.score and self.score > result[1]:
					result = [self.opening_name, self.score]
			
			# print("move made to " + result[0] + " " + str(result[1]))
			return result