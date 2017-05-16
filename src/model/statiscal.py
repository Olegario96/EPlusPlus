import random

##
## @brief      Class for statiscal. This class is responsible for implements
##             the sampling methods. The eplusplus software at the first version
##             will support only the random sampling (i.e. Monte Carlo) and the
##             Latin Hypercube Sampling method. The import random is used to
##             sorte random falues from the lists.
##
class Statiscal(object):

	def __init__(self):
		super(Statiscal, self).__init__()

	##
	## @brief      This method choose a random value inside a list and return
	##             it.
	##
	## @param      self    Non static method
	## @param      sample  List with the values that we wanna randomly choose.
	##
	## @return     Return a random value from the list "sample".
	##
	def randomValue(self, sample):
		return random.choice(sample)

	##
	## @brief      This method receive as argument a list with values and the
	##             number of values that we want to choose randomly. The method
	##             create a variable to control the the "while" loop and a list
	##             to apend the values that were randomly choose. After choose
	##             the values, just return the list.
	##
	## @param      self        Non static method
	## @param      sample      List with the values that we wanna randomly
	##                         choose.
	##
	## @param      numSamples  Number of how many values we wanna randomly
	##                         choose. For example: if we have a list with 5
	##                         values and we want 3 random values we pass the
	##                         list as "sample" and the "numSamples" as 3.
	##
	## @return     Return a list with all the values that were randomly choose.
	##             The list has a length equals to the "numSamples".
	##
	def randomValues(self, sample, numSamples):
		i = 0
		sampleFinal = []
		while i < numSamples:
			sampleFinal.append(self.randomValue(sample))
			i += 1

		return sampleFinal

	##
	## @brief      This method is a implementation of a simplificated version of
	##             the Latin Hypercube Sampling method. The method, basically,
	##             consists on split the the "sample" into "n" groups and
	##             randomly choose a value from each group. So if we have a
	##             "sample" with 5 values and we want a "numSamples" of 2 this
	##             method will split our "sample" into 3 lists being 2 with 2
	##             values and one with just one value. After that, for each
	##             list that we generate, we choose a random number and insert
	##             into a new list. At the end, we just return this list.
	##
	## @param      self       Non static method
	## @param      sample     List with the values from where we will take
	##                        the values aplying the LHS method.
	## @param      numSamples Number of values that we wanna choose from the
	##                        "sample" using the LHS method.
	##
	## @return     Return the values taken from the "sample" after aply the
	##             LHS method.
	##
	def lhsValues(self, sample, numSamples):
		lhsValuesFinal = []
		factor = float(len(sample))/numSamples
		lhsValues = [sample[int(factor*i):int(factor*(i+1))] for i in range(numSamples)]

		for element in lhsValues:
			lhsValuesFinal.append(self.randomValue(element))

		return lhsValuesFinal