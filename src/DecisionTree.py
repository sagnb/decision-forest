"""Decision Tree"""


__author__ = "Sá, G. N. B."
__credits__ = ["Sá, G. N. B."]
__license__ = "MIT"
__version__ = "1.0.1"	
__maintainer__ = "Sá, G. N. B."
__email__ = "guinbsa@gmail.com"
__status__ = "Development"

__all__ = ['DecisionNode']


import math
import deps.data_structures.Tree as tr


class DecisionNode(tr.Node):
	"""Node of Decision Tree"""
	def __init__(self, data, main_question, *children):
		"""Constructor

		Parameters:
		data (?): Any information
		main_question (function): Main question of the problem
		children (DecisionNode): Any son of this node

		"""
		super().__init__(data, *children)
		self.children = dict(self.children)
		self.main_question = main_question
		self.main_answers = {}
		self.count = 0
		self.question = None
		for answer in list(map(self.main_question, self.data)):
			if not (answer in self.main_answers):
				self.main_answers[answer] = 0
			self.main_answers[answer] += 1
			self.count += 1

	def __str__(self):
		"""Returns a string with the node information
		
		Return:
		str: String containing the answers to the main question 
			of this node
		
		"""
		return ''.join([
			f'{answer} -> {self.main_answers[answer]}; ' 
			for answer in self.main_answers
			])

	@property
	def lst_of_children(self):
		"""Returns the list of children for this node
		
		Return:
		list: List of children of this node
		
		"""
		return self.children.values()

	def new_son(self, *data):
		"""Adds a new node in the subtree
		
		Parameters:
		data (?): Any information
		
		"""
		for d in data:
			self.children[d[0]] = DecisionNode(d[1], self.main_question)

	def fit(self, questions, max_height=math.inf):
		"""Trains the tree to solve the problem

		Parameters:
		questions (list): List of functions that represent the 
			other information

		"""
		if questions and max_height > 0 and len(self.main_answers) > 1:
			answers = {}
			questions, self.question = self.choise(questions)
			for index, answer in enumerate(list(map(self.question, self.data))):
				if not (answer in answers):
					answers[answer] = []
				answers[answer].append(self.data[index])
			for answer in answers:
				self.new_son((answer, answers[answer]))
			for son in self.lst_of_children:
				son.fit(questions.copy(), max_height-1)

	def choise(self, questions):
		"""Returns a function from the list to evolve the problem

		Parameters:
		questions (list): List of functions that represent the 
			other information

		Return:
		function: Function to evolve the problem

		"""
		best_question = None
		best_gain = 0
		index = 0
		for i, question in enumerate(questions):
			gain = self.information_gain(question)
			if best_gain <= gain:
				best_gain = gain
				best_question = question
				index = i
		return questions, questions.pop(index)

	def information_gain(self, A):
		answers = {}
		children = {}
		for index, answer in enumerate(list(map(A, self.data))):
			if not (answer in answers):
				answers[answer] = []
			answers[answer].append(self.data[index])
		for answer in answers:
			children[answer] = DecisionNode(answers[answer], self.main_question)
		info_D = 0
		for answer in self.main_answers:
			info_D += (self.main_answers[answer]/float(self.count)) * math.log(
				(self.main_answers[answer]/float(self.count)), 2
				)
		info_AD = 0
		for son in children.values():
			info_Dj = 0
			for answer in son.main_answers:
				info_Dj += (son.main_answers[answer]/float(son.count)) * math.log(
					(son.main_answers[answer]/float(son.count)), 2
					)
			info_AD += son.count/float(self.count) * info_Dj
		return info_D - info_AD

	def test(self, sample):
		if self.is_leaf:
			result = list(self.main_answers.keys())[0]
			for answer in self.main_answers:
				if self.main_answers[answer] > self.main_answers[result]:
					result = answer
			return result
		return self.children[self.question(sample)].test(sample)


if __name__ == '__main__':
	root = DecisionNode(list(range(1, 200)), lambda x : x%6 == 0)
	root.fit([lambda x: x%2 == 0, lambda x: x%3 == 0, lambda x: x%4 == 0, lambda x: x%5 == 0])
	print(root.test(int(input('digite um numero: '))))
