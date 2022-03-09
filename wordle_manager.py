from wordle import Wordle

class WordleManager():
	def __init__(self):
		self.instances = {}

	def create(self, i, *args):
		self.instances[i] = Wordle()

	


	def get(self, i):
		print(self.instances)
		return self.instances[i]

