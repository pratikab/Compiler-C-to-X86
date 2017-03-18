import cparser.py
import parsetab.py

# ------------------------------------------------------------
#	This code generates the following :-				
# 	1. Global Symbol Tables								
#	2. Local Symbol Tables for indivisual functions		
#	3. Abstract Syntax Tree (AST) 						
#-------------------------------------------------------------

class Node(object):
	# List of all the attributes
	attributes = []
	"""docstring for Node"""
	# Constructing nodes
	def __init__(self, arg):
		super(Node, self).__init__()
		self.arg = arg

	# Display the nodes hanging on the sub-tree of the "node"

class Visitor(object):
	# Will contain methods to traverse different type of nodes