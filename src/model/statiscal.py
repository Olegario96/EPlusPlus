import random

class Statiscal(object):

	def __init__(self):
		super(Statiscal, self).__init__()

	def randomValue(self, sample):
		return random.choice(sample)

	def randomValues(self, sample, numSaples):
		i = 0
		sampleFinal = []
		while i < numSaples:
			sampleFinal.append(self.randomValue(sample))
			i += 1

		return sampleFinal

	def lhsValues(self, sample, numSaples):
		lhsValuesFinal = []
		lhsValues = [sample[x:x+numSamples] for x in range(0, len(sample), numSamples)]

		for element in lhsValues:
			lhsValuesFinal.append(self.randomValue(element))

		return lhsValuesFinal

st = Statiscal()
sample = [4, 7, 9, 6, 15, 11, 13]
numSamples = 3
print(st.lhsValues(sample, numSamples))