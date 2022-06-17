import ete3

from tree_node import TreeNode

def makeTree(tree):
	t = ete3.Tree()
	make_ete_tree_recursive(t, tree)
	return t


def saveToFile(tree, GAME_TREE_OUT_FILE_NAME):# styling
	tree.render(GAME_TREE_OUT_FILE_NAME, tree_style=getStyle())


def show(tree):
	tree.show(tree_style=getStyle())


def getStyle():
	ts = ete3.TreeStyle()
	ts.mode="r"
	ts.scale = 150 # how many pixels per branch length unit
	ts.branch_vertical_margin = 10 # how many pixels between adjacent branches
	ts.show_leaf_name = False
	def my_layout(node):
		F = ete3.TextFace(node.name, tight_text=True)
		F.hz_align = 2 # 0 left, 1 center, 2 right
		ete3.add_face_to_node(F, node, column=0, position="branch-top")
	ts.layout_fn = my_layout
	
	ts.title.add_face(ete3.TextFace("Chess Openings: game-tree", fsize=150), column=0)
	#ts.legend.add_face(ete3.CircleFace(10, "red"), column=0)
	#ts.legend.add_face(ete3.TextFace("0.5 support"), column=1)
	
	return ts


def make_ete_tree_recursive(parent_ete_node, current_node):
	ns = ete3.NodeStyle()
	ns["vt_line_width"] = 3
	ns["hz_line_width"] = 3
	ns["vt_line_type"] = 0 # 0 = solid, 1= dashed, 2 = dotted
	ns["hz_line_type"] = 0
	
	ns["size"] = 12
	if current_node.depth % 2 == 0:
		ns["fgcolor"] = "#000000"
	else:
		ns["fgcolor"] = "#c7c7c7"
	
	# each branch of openings gets their own color
	if current_node.opening_name and current_node.opening_name.startswith("A"):
		ns["vt_line_color"] = "#06857a"
		ns["hz_line_color"] = "#06857a"
	elif current_node.opening_name and current_node.opening_name.startswith("B"):
		ns["vt_line_color"] = "#e1ca09"
		ns["hz_line_color"] = "#e1ca09"
	elif current_node.opening_name and current_node.opening_name.startswith("C"):
		ns["vt_line_color"] = "#0375b1"
		ns["hz_line_color"] = "#0375b1"
	elif current_node.opening_name and current_node.opening_name.startswith("D"):
		ns["vt_line_color"] = "#c42748"
		ns["hz_line_color"] = "#c42748"
	elif current_node.opening_name and current_node.opening_name.startswith("E"):
		ns["vt_line_color"] = "#f6913a"
		ns["hz_line_color"] = "#f6913a"
	elif current_node.opening_name and current_node.opening_name.startswith("Z"):
		ns["vt_line_color"] = "#6eff2b"
		ns["hz_line_color"] = "#6eff2b"
	
	if not current_node.move:
		node_name = "Game Start"
		ns["fgcolor"] = "White" #invisible
	else: 
		node_name = "" + str(current_node.move)
	
	face_text = ""
	if current_node.opening_name:
		face_text = face_text + " (" + str(current_node.opening_name) + ")"
	
	if current_node.score:
		face_text = face_text + " [" + str(current_node.score) + "]"
		
	
	#if current_node.is_leaf():
	#	ete_node = parent_ete_node.add_child(name = str(current_node.move) + " (" + str(current_node.opening_name) + ") (" + str(current_node.score) + ")")
	#else: 
	#	if current_node.opening_name: #check for "not None"
	#		ete_node = parent_ete_node.add_child(name = str(current_node.move) + " (" + str(current_node.opening_name) + ")")
	#	else:
	#		ete_node = parent_ete_node.add_child(name = str(current_node.move))
	
	ete_node = parent_ete_node.add_child(name = node_name, dist=1)
	ete_node.set_style(ns)
	
	if len(face_text)>0:
		F = ete3.TextFace(face_text, fgcolor="red", fstyle="italic", fsize=6)
		F.fgcolor = ns["vt_line_color"]
		ete_node.add_face(F, column=0, position="branch-bottom")
	
	for child in current_node.childs:
		make_ete_tree_recursive(ete_node, child)