#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import pandas as pd
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score

"""
Script to train recipe classifier.
The classifier can detect if a newspaper article contains a recipe
"""


dataset = pd.read_pickle('./data/recipe_dataset.pkl')
dataset['type_id'] = dataset['type'].factorize()[0]
category_id_df = dataset[['type', 'type_id']].drop_duplicates().sort_values('type_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['type_id', 'type']].values)
labels = ['articles', 'recipes']

# prepare features
X = dataset['ocr_without_stopwords']
y = dataset['type'].values

# shuffle dataset
X_shuf, y_shuf = shuffle(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_shuf, y_shuf, test_size=0.3, random_state=1)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# Naive Bayes
# initialize classifier
NB_clf = Pipeline([
	('tfidf', TfidfVectorizer(min_df=5, max_df=0.9, sublinear_tf=True, ngram_range=(1,2), analyzer='word')),
	('clf', MultinomialNB())])

params = {
	'tfidf__min_df': (0, 5, 10),
	'tfidf__max_df': (0.25, 0.50, 0.75, 0.90),
	'tfidf__analyzer': ['word'],
	'tfidf__ngram_range': [(1,1), (1,2), (1,3), (1,4), (1,5), (2, 2), (2, 3), (2, 4), (2,5), (2,6), (3,3), (3,4), (3,5)],
	'tfidf__use_idf': (True, False),
	'clf__alpha': (1e-2, 1e-3)
}

# Random Search for hyper-parameters
NB_randsearch = RandomizedSearchCV(NB_clf, param_distributions=params, n_iter=50, cv=5, n_jobs=30, verbose=3)
NB_randsearch.fit(X_train, y_train)

joblib.dump(NB_randsearch, 'NB_clf.pkl')

print("Naive Bayes Best Score:{}".format(NB_randsearch.best_score_))
print("Naive Bayes Best Params:{}".format(NB_randsearch.best_params_))

NB_pred = NB_randsearch.predict(X_test)

print("Accuracy Naive Bayes: {}".format(accuracy_score(y_test, NB_pred)))
scores = {}
scores['precision'] = precision_score(y_test, NB_pred, average=None)
scores['recall'] = recall_score(y_test, NB_pred, average=None)
scores['f1'] = f1_score(y_test, NB_pred, average=None)
print("Naive Bayes Precision/Recall/F1 Score:")
print("-" * 80)
print(pd.DataFrame(data=scores, index=labels))


# SVM classifier
# Initialize classifier
SVM_clf = Pipeline([('tfidf', TfidfVectorizer(min_df=5, max_df=0.75, sublinear_tf=True, ngram_range=(1, 2), analyzer='word')),
						 ('clf-svm', SGDClassifier(alpha=1e-3, random_state=42))])


params = {
	'tfidf__min_df': (0, 5),
	'tfidf__max_df': (0.50, 0.75, 0.90),
	'tfidf__analyzer': ['word'],
	'tfidf__ngram_range': [(1, 1), (1,2), (1, 3), (1,4), (1,5), (2, 2), (2, 3), (2, 4), (2,5), (3,3), (3,4), (3,5)],
	'clf-svm__alpha': (1e-2, 1e-3)
}

# Random Search for hyper-parameters SVM
svm_randsearch = RandomizedSearchCV(SVM_clf, param_distributions=params, n_iter=50, cv=5, n_jobs=30,
								random_state=333, verbose=3)

svm_randsearch.fit(X_train, y_train)
joblib.dump(svm_randsearch, 'SVM_clf.pkl')

print("SVM Best Score:{}".format(svm_randsearch.best_score_))
print("SVM Best Params:{}".format(svm_randsearch.best_params_))

SVM_pred = svm_randsearch.predict(X_test)

print("Accuracy SVM: {}".format(accuracy_score(y_test, SVM_pred)))
scores = {}
scores['precision'] = precision_score(y_test, SVM_pred, average=None)
scores['recall'] = recall_score(y_test, SVM_pred, average=None)
scores['f1'] = f1_score(y_test, SVM_pred, average=None)
print("SVM Precision/Recall/F1 Score:")
print("-" * 80)
print(pd.DataFrame(data=scores, index=labels))


# SVC classifier
# Initialize Linear SVC Classifier
SVC_clf = Pipeline([
	('tfidf', TfidfVectorizer(min_df=5, max_df=0.75, sublinear_tf=True, ngram_range=(1,2), analyzer='word')),
	('svc-clf', OneVsRestClassifier(LinearSVC(verbose=True, class_weight='balanced', C=1.0)))])


params = {
	'tfidf__min_df': (0, 5),
	'tfidf__max_df': (0.50, 0.75, 0.90),
	'tfidf__analyzer': ['word'],
	'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3), (1, 4), (1,5), (2, 2), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)],
}

# Random Search for hyper-parameters
svc_randsearch = RandomizedSearchCV(SVC_clf, param_distributions=params,
									n_iter=50, cv=5, n_jobs=30,
									random_state=333, verbose=3)

svc_randsearch.fit(X_train, y_train)
joblib.dump(svc_randsearch, 'SVC_clf.pkl')

print("SVM Best Score:{}".format(svc_randsearch.best_score_))
print("SVM Best Params:{}".format(svc_randsearch.best_params_))

SVC_pred = svc_randsearch.predict(X_test)

print("Accuracy SVC: {}".format(accuracy_score(y_test, SVC_pred)))
scores = {}
scores['precision'] = precision_score(y_test, SVC_pred, average=None)
scores['recall'] = recall_score(y_test, SVC_pred, average=None)
scores['f1'] = f1_score(y_test, SVC_pred, average=None)
print("SVC Precision/Recall/F1 Score:")
print("-" * 80)
print(pd.DataFrame(data=scores, index=labels))
