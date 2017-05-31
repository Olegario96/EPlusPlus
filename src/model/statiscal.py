import random
from pyDOE import lhs

##
## @brief      Class for statiscal. This class is responsible for implements
##             the sampling methods. The eplusplus software at the first version
##             will support only the random sampling and the Latin Hypercube
##             Sampling method using "pyDOE" lib. The import random is used to
##             sort random falues from the lists.
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
	## @brief      This method receives a dictionary and the number of samples
	##             that user wants. So it creates a matrix of samplesSize x
	##             len(possibleValues). At this matrix every column represents
	##             one variable of the variables and tis value is randomly
	##             choosed from the the list of all possible values.
	##
	## @param      self            Non static mehotd
	## @param      possibleValues  A dictionary (Hash Table) with the number
	##                             of entries equals to the number of variables
	##                             which maps to a list with all possible
	##                             values of that variable.
	## @param      sampleSize      Number of data (sample) that the user wants.
	##
	## @return     Returns a matrix sampleSize x len(possibleValues). Each line
	##             contains one value from the list inside the hash table that
	##             was randomly choosed.
	##
	def randomValues(self, possibleValues, sampleSize):
		i = 0
		j = 0
		matrixSample = []
		sample = []

		while i < sampleSize:
			while j < len(possibleValues):
				randomValue = self.randomValue(possibleValues[j])
				sample.append(randomValue)
				j += 1

			j = 0
			matrixSample.append(sample)
			i += 1

		return matrixSample

	##
	## @brief      This method refers to the Hypercube Latin Sampling.
	##             It uses the pyDOE library to do the sampling. This method
	##             is to complex to explain here. Please, search on the internet
	##             for more information to learn about it.
	##
	## @param      self            Non static method
	## @param      possibleValues  A dictionary (Hash Table) with the number
	##                             of entries equals to the number of variables
	##                             which maps to a list with all possible
	##                             values of that variable.
	## @param      sampleSize      Number of data (sample) that the user wants.
	##
	## @return     Returns a matrix sampleSize x len(possibleValues). This
	##             matrix contains values from 0 to 1 that will be mapped to
	##             our set of variables
	##
	def lhsValues(self, possibleValues, sampleSize):
		lhd = lhs(len(possibleValues), samples=sampleSize)

		return lhd

	##
	## @brief      This method map a continuous value to a discrete one.
	##             We apply this method to every value in our dictionary that
	##             contains all possible values supplied by the user. This allow
	##             to have a consistent sample.
	##
	## @param      value         The continous value that will use as baseline.
	## @param      discrete      The discrete value that we want to map.
	##
	## @return    Returns the next discrete value.
	##
	def discrete(self, value, discrete):
	    diff = 1/discrete
	    total=diff
	    i=1
	    while (total<value):
	        i+=1
	        total+=diff
	    return i

	##
	## @brief      This method creates a list of lists which number of lists
	##             is equal to "sampleSize". Each list has a value for each
	##             variable, creating a possibility, among all. For do this
	##             we take the values created from the "lhs" method and map
	##             the values to our values taken from CSV using the "discrete"
	##             function (see its documentation for more info). Each list
	##             has a size equal to the number of variable in each item
	##             of this list has a value from the csv that represents that
	##             column.
	##
	## @param      self            Non static method.
	## @param      lhd             Matrix samplesSize x len(possibleValues)
	##                             with values from the "lhs" method. See its
	##                             documentation for more info.
	##
	## @param      possibleValues  A dictionary (Hash Table) with the number
	##                             of entries equals to the number of variables
	##                             which maps to a list with all possible
	##                             values of that variable.
	##
	## @param      sampleSize      Number of possibilities that the user wants.
	##
	## @return     A list of lists containing the continous values mapped
	##             to values of variable which came from the csv informed
	##             by the user.
	##
	def mapValues(self, lhd, possibleValues, sampleSize):
		mappedValues = []
		for i in range(0, sampleSize):
			chosenValues = []
			for j in range(0, len(possibleValues)):
				column = int(self.discrete(lhd[i][j],len(possibleValues[j])))-1
				values = str(possibleValues[j][column])
				chosenValues.append(values)
			mappedValues.append(chosenValues)

		return mappedValues