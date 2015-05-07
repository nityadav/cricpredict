import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB

# parameters
playing_teams = ["England","Australia"]
playing_teams.sort()

def decision_tree():
	# train your datasets
	# form the train set
	train_file = open("data/" + "_".join(playing_teams) + "_train.csv")
	x_train = np.loadtxt(train_file, delimiter=",")
	m_train = x_train.shape[0]
	y_train = x_train[:,0:1].reshape(m_train)
	x_train = x_train[:,1:]
	# train and cross-validate
	clf = DecisionTreeClassifier(max_depth=None, min_samples_split=1,random_state=0)
	scores = cross_val_score(clf, x_train, y_train)
	clf = clf.fit(x_train, y_train)
	# do the testing
	test_file = open("data/" + "_".join(playing_teams) + "_test.csv")
	x_test = np.loadtxt(test_file, delimiter=",")
	m_test = x_test.shape[0]
	y_test = x_test[:,0:1].reshape(m_test)
	x_test = x_test[:,1:]
	prediction = clf.predict(x_test)
	# get the results
	bad_matches = []
	urls = [line.strip() for line in open("data/" + "_".join(playing_teams) + "_test_matches.csv")]
	accuracy = 0
	for i in range(m_test):
		if prediction[i] != y_test[i]:
			bad_matches.append(urls[i])
		else:
			accuracy += 1
	return [scores.mean(), float(accuracy)/float(m_test), bad_matches]

def random_forests():
	# train your datasets
	# form the train set
	train_file = open("data/" + "_".join(playing_teams) + "_train.csv")
	x_train = np.loadtxt(train_file, delimiter=",")
	m_train = x_train.shape[0]
	y_train = x_train[:,0:1].reshape(m_train)
	x_train = x_train[:,1:]
	# train and cross-validate
	clf = RandomForestClassifier(n_estimators=11, max_depth=None, min_samples_split=1, random_state=0)
	scores = cross_val_score(clf, x_train, y_train)
	clf = clf.fit(x_train, y_train)
	# do the testing
	test_file = open("data/" + "_".join(playing_teams) + "_test.csv")
	x_test = np.loadtxt(test_file, delimiter=",")
	m_test = x_test.shape[0]
	y_test = x_test[:,0:1].reshape(m_test)
	x_test = x_test[:,1:]
	prediction = clf.predict(x_test)
	# get the results
	bad_matches = []
	urls = [line.strip() for line in open("data/" + "_".join(playing_teams) + "_test_matches.csv")]
	accuracy = 0
	for i in range(m_test):
		if prediction[i] != y_test[i]:
			bad_matches.append(urls[i])
		else:
			accuracy += 1
	return [scores.mean(), float(accuracy)/float(m_test), bad_matches]

def adaboost():
	# train your datasets
	# form the train set
	train_file = open("data/" + "_".join(playing_teams) + "_train.csv")
	x_train = np.loadtxt(train_file, delimiter=",")
	m_train = x_train.shape[0]
	y_train = x_train[:,0:1].reshape(m_train)
	x_train = x_train[:,1:]
	# train and cross-validate
	clf = AdaBoostClassifier(n_estimators=10)
	scores = cross_val_score(clf, x_train, y_train)
	clf = clf.fit(x_train, y_train)
	# do the testing
	test_file = open("data/" + "_".join(playing_teams) + "_test.csv")
	x_test = np.loadtxt(test_file, delimiter=",")
	m_test = x_test.shape[0]
	y_test = x_test[:,0:1].reshape(m_test)
	x_test = x_test[:,1:]
	prediction = clf.predict(x_test)
	# get the results
	bad_matches = []
	urls = [line.strip() for line in open("data/" + "_".join(playing_teams) + "_test_matches.csv")]
	accuracy = 0
	for i in range(m_test):
		if prediction[i] != y_test[i]:
			bad_matches.append(urls[i])
		else:
			accuracy += 1
	return [scores.mean(), float(accuracy)/float(m_test), bad_matches]

def svm_classifier():
	# train your datasets
	# form the train set
	train_file = open("data/" + "_".join(playing_teams) + "_train.csv")
	x_train = np.loadtxt(train_file, delimiter=",")
	m_train = x_train.shape[0]
	y_train = x_train[:,0:1].reshape(m_train)
	x_train = x_train[:,1:]
	# train and cross-validate
	clf = svm.SVC(kernel='sigmoid')
	scores = cross_val_score(clf, x_train, y_train)
	clf = clf.fit(x_train, y_train)
	# do the testing
	test_file = open("data/" + "_".join(playing_teams) + "_test.csv")
	x_test = np.loadtxt(test_file, delimiter=",")
	m_test = x_test.shape[0]
	y_test = x_test[:,0:1].reshape(m_test)
	x_test = x_test[:,1:]
	prediction = clf.predict(x_test)
	# get the results
	bad_matches = []
	urls = [line.strip() for line in open("data/" + "_".join(playing_teams) + "_test_matches.csv")]
	accuracy = 0
	for i in range(m_test):
		if prediction[i] != y_test[i]:
			bad_matches.append(urls[i])
		else:
			accuracy += 1
	return [scores.mean(), float(accuracy)/float(m_test), bad_matches]

def naive_bayes():
	# train your datasets
	# form the train set
	train_file = open("data/" + "_".join(playing_teams) + "_train.csv")
	x_train = np.loadtxt(train_file, delimiter=",")
	m_train = x_train.shape[0]
	y_train = x_train[:,0:1].reshape(m_train)
	x_train = x_train[:,1:]
	# train and cross-validate
	clf = GaussianNB()
	scores = cross_val_score(clf, x_train, y_train)
	clf = clf.fit(x_train, y_train)
	# do the testing
	test_file = open("data/" + "_".join(playing_teams) + "_test.csv")
	x_test = np.loadtxt(test_file, delimiter=",")
	m_test = x_test.shape[0]
	y_test = x_test[:,0:1].reshape(m_test)
	x_test = x_test[:,1:]
	prediction = clf.predict(x_test)
	# get the results
	bad_matches = []
	urls = [line.strip() for line in open("data/" + "_".join(playing_teams) + "_test_matches.csv")]
	accuracy = 0
	for i in range(m_test):
		if prediction[i] != y_test[i]:
			bad_matches.append(urls[i])
		else:
			accuracy += 1
	return [scores.mean(), float(accuracy)/float(m_test), bad_matches]


# main starts here
print "Decision Tree results:"
print decision_tree()
print "Random Forests results:"
print random_forests()
print "AdaBoost results:"
print adaboost()
print "SVM results:"
print svm_classifier()
print "Naive Bayes results:"
print naive_bayes()
print ""