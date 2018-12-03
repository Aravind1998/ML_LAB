"""

Assuming a set of documents that need to be classified, use the naïve Bayesian Classifier model to perform this task. Built-in Java classes/API can be used to write the program. Calculate the accuracy, precision, and recall for your data set. 

"""



import pandas as pd

msg = pd.read_csv('data6.csv',names = ['message','label'])
print("Total instances in the dataset = ",msg.shape[0])

msg['labelnum'] = msg.label.map({'pos':1,'neg':0})
X = msg.message
Y = msg.labelnum

print("The messagw and its label of first 5 instances")
X5, Y5 = X[0:5],msg.label[0:5]
for x,y in zip(X5,Y5):
    print(x,',',y)

from sklearn.model_selection import train_test_split

xtrain, xtest, ytrain, ytest = train_test_split(X,Y)
print("Dataset is split into Training and testing samples")
print("Total training instances = ", xtrain.shape[0])
print("Total testing instances = ", xtest.shape[0])

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
xtrain_dtm = count_vect.fit_transform(xtrain)
xtest_dtm = count_vect.transform(xtest)
print("Total features extracted using CountVectorizer =",xtrain_dtm.shape[1])

print("Features for first 5 training instances are listed below")
df = pd.DataFrame(xtrain_dtm.toarray(),columns = count_vect.get_feature_names())
print(df[0:5])

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(xtrain_dtm,ytrain)
predicted = clf.predict(xtest_dtm)

print("Classification results of tesing samples")
for doc, p in zip(xtest,predicted):
    pred = 'pos' if p == 1 else 'neg'
    print("%s -> %s" % (doc, pred))

from sklearn import metrics
print("Accuracy Metrics")
print("Accuracy of the classifier = ",metrics.accuracy_score(ytest,predicted))
print("Recall = ",metrics.recall_score(ytest,predicted))
print("Precision = ",metrics.precision_score(ytest,predicted))
print("Confusion Matrix = ",metrics.confusion_matrix(ytest,predicted))
