import random

class Poem:
	def __init__(self, n=2):
		self.n = n  # Order of the Markov chain
		self.model = {}
		self.shelley_corpus = """
		O wild West Wind, thou breath of Autumn's being,
		Thou, from whose unseen presence the leaves dead
		Are driven, like ghosts from an enchanter fleeing,
		Yellow, and black, and pale, and hectic red,
		Pestilence-stricken multitudes: O thou,
		Who chariotest to their dark wintry bed
		The winged seeds, where they lie cold and low,
		Each like a corpse within its grave, until
		Thine azure sister of the Spring shall blow
		Her clarion o'er the dreaming earth, and fill
		(Driving sweet buds like flocks to feed in air)
		With living hues and odours plain and hill:
		Wild Spirit, which art moving everywhere;
		Destroyer and preserver; hear, O hear!
		"""
		self.train(self.shelley_corpus)

	def train(self, text):
		words = text.split()
		for i in range(len(words) - self.n):
			key = tuple(words[i:i + self.n])
			next_word = words[i + self.n]
			self.model.setdefault(key, []).append(next_word)

	def generate(self, length=30, seed=None, line_length=random.randint(3,10)):
		if not self.model:
			return self.shelley_corpus.splitlines()[random.randint(0,len(self.shelley_corpus.splitlines())-1)].strip()+" Issue"
		start = seed or random.choice(list(self.model.keys()))
		output = list(start)
		poem = []
		line = list(start)

		for _ in range(length - len(start)):
			key = tuple(output[-self.n:])
			if key in self.model:
				next_word = random.choice(self.model[key])
				output.append(next_word)
				line.append(next_word)
				if len(line) >= line_length or next_word.endswith(('.', ',', '!', '?')):
					poem.append(' '.join(line))
					line = []
			else:
				break
		if line:  # Add the last line if not empty
			poem.append(' '.join(line))
		return '\n'.join(poem).splitlines()[0]

# Training with Percy Bysshe Shelley's corpus
if __name__ == "__main__":

	mc = Poem(n=2)
	print(mc.generate())
