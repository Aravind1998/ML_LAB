"""

Write a program to demonstrate the working of the decision tree based ID3 algorithm. Use an appropriate data set for building the decision tree and apply this knowledge toclassify a new sample. 

"""



from math import log
import operator

'''
Reads the dataset and creates a list of lists of the values and also a seperate
variable for all the attributes that are in the dataset.
'''
def createDataSet():
    file = open('gender.csv')
    data = [[]]

    for line in file:
        line = line.strip("\r\n")
        data.append(line.split(','))
    
    data.remove([])
    
    #We assume that the first row are all headers and we exclude those form the dataset
    headers = data[0]
    data.remove(headers) 
    return data, headers

'''
Calculates the entropy of a (subsetted) dataset.
'''
def entropy(dataSet):
    numberOfEntries = len(dataSet)
    labelCounts = {}
    
    #The number of unique elements and their occurence
    for attribute in dataSet:
        currentLabel = attribute[-1]
        if currentLabel not in labelCounts.keys(): 
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        
    currentEntropy = 0.0
    
    for key in labelCounts:
        probability = float(labelCounts[key]) / numberOfEntries
        #For the calculation, we use a log2 base
        currentEntropy -= probability * log(probability, 2)
        
    return currentEntropy

'''
Splits the dataset, based on their axis and value, and returns the remaining dataset
'''
def splitData (data, axis, value):
    splittedData = []
    for attribute in data:
        if attribute[axis] == value:
            reducedAttribute = attribute[:axis]  #Chop out axis used for splitting
            reducedAttribute.extend(attribute[axis + 1:])
            splittedData.append(reducedAttribute)
    return splittedData


def chooseBestAttributeToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  #The last column is used for the labels
    baseEntropy = entropy(dataSet)
    bestInfoGain = 0.0;
    bestAttribute = -1
    for i in range(numFeatures):  #Iterate over all the features
        attributeList = [example[i] for example in dataSet]  #Create a list of all the examples of this feature
        uniqueVals = set(attributeList)  #Get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitData(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * entropy(subDataSet)

        #Calculation of the information gain
        infoGain = baseEntropy - newEntropy

        if (infoGain > bestInfoGain):  #Compare this to the best gain so far
            bestInfoGain = infoGain  #If better than current best, set to best
            bestAttribute = i
    return bestAttribute


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    #Extracting data
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]  #Stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1:  #Stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    #Use Information Gain
    bestAttribute = chooseBestAttributeToSplit(dataSet)
    bestAttributeLabel = labels[bestAttribute]

    #Build a tree recursively
    myTree = {bestAttributeLabel: {}}
    del (labels[bestAttribute])
    featValues = [example[bestAttribute] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]  #Copy all of labels, so trees don't mess up existing labels
        myTree[bestAttributeLabel][value] = createTree(splitData(dataSet, bestAttribute, value), subLabels)
    return myTree


def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel

# Define the main function
def main():                      
    #Collect all the data:
    myData, labels = createDataSet()
        
    #Build the decision tree:
    mytree = createTree(myData, labels)
    print(mytree)

main()
