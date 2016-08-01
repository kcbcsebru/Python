import urllib
from numpy import genfromtxt, zeros
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB

#download the data to ircs.csv
url = 'http://aima.cs.berkeley.edu/data/iris.csv'
webpage = urllib.urlopen(url)
fp = open("iris.txt", 'w')
fp.write(webpage.read())
fp.close()


# read the file and get the data and name
data = genfromtxt('iris.txt', delimiter=',', usecols=(0,1,2,3), dtype=float)
name = genfromtxt('iris.txt', delimiter=',', usecols=(4), dtype=str)

# get the train data and test data
names = ['setosa', 'versicolor', 'virginica']
t = zeros(len(name))
t[name == 'setosa'] = 1
t[name == 'versicolor'] = 2
t[name == 'virginica'] = 3
train, test, train_t, test_t = cross_validation.train_test_split(data, t, test_size=0.4, random_state=0)

# train
classifier = GaussianNB()
classifier.fit(train, train_t)

# test
t_predict = classifier.predict(test)
ac = sum(test_t == t_predict)
ac_rate = float(ac)/float(len(test_t))
print ac_rate

