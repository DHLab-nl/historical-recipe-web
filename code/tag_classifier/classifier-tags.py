#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import pandas as pd
import ast
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import fbeta_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split

"""
Script to train multilabel classifier based on Allerhande df_tags_matrix
"""

# Author: melvinwevers@gmail.com

df = pd.read_csv('./data/allerhande_clean.csv', low_memory=False)
df["tags"] = df["tags"].map(lambda d: ast.literal_eval(d))
df = df.dropna(subset=['tag_0'])
df = df.dropna(subset=['description'])

# Transfer tags into dummy matrix
mlb = MultiLabelBinarizer()
df_tags_matrix = pd.DataFrame(mlb.fit_transform(df['tags']),
                              columns=mlb.classes_, index=df.index)


df_tags_matrix['gezond'] = df_tags_matrix['slank'] + df_tags_matrix['gezond']
df_tags_matrix['vegetarisch'] = df_tags_matrix['vegetarisch'] + df_tags_matrix['zonder vlees/vis'] + df_tags_matrix['veganistisch']
df_tags_matrix['gezond'] = df_tags_matrix['gezond'].apply(lambda x: 1 if x >= 1 else 0)
df_tags_matrix['vegetarisch'] = df_tags_matrix['vegetarisch'].apply(lambda x: 1 if x >= 1 else 0)

drop_cols = ['advertorial', 'koningsdag', 'in te vriezen', 'slank', 'lente', 'halloween', 'zuid-afrikaans',
             'oost-europees', 'picknick', 'kidsfavoriet', 'jamie oliver', 'caribisch',
             'camping', 'surinaams', 'vaderdag', 'valentijnsdag', 'argentijns', 'sinterklaas', 'pocheren',
            'verjaardag', 'traktatie', 'stomen', 'keukenmachine', 'zonder vlees/vis', 'zuid-amerikaans', 'veganistisch' ,'wat eten we vandaag',
            'moederdag']

df_tags_matrix.drop(drop_cols, axis=1, inplace=True)

for col in df_tags_matrix.columns:
    if df_tags_matrix[col].sum() < 50:
        df_tags_matrix.drop(col, axis=1, inplace=True)

stop_words = ['indiaas', 'indiase', 'vegetarisch', 'italiaans', 'thais', 'thaise', 'hollands',
    'hollandse', 'franse', 'frans', 'oven', 'borrel', 'aziatische', 'aziatisch', 'borrel',
    'mediterraanse', 'chinees', 'chinese', 'spaanse', 'spaanse', 'bakken', 'grillen', 
    'mexicaans', 'mexicaanse', 'glutenvrij', 'glutenvrije', 'lactosevrij', 'lactosevrije',
    'snel', 'amerikaans', 'amerikaanse', 'barbecue', 'indonesisch', 'indonesische', 
    'roerbakken/wokken', 'vooraf te maken', 'frituren', 'kerst', 'stoven', 'midden-oosters',
    'zonder vlees/vis', 'japans', 'japanse', 'budget', 'engels', 'engelse', 'gezond',
    'oud  nieuw', 'pasen', 'zonder vlees', 'gourmet']



df.recipe_instruction = df.recipe_instruction.fillna('')
df_tags_matrix['text'] = df.title + ' ' + df.description + ' ' + df.recipe_instruction

df_tags_matrix['text_without_stopwords'] = df_tags_matrix['text'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in (stop_words)]))


df_tags_matrix = df_tags_matrix.dropna()
mlb.classes_ = df_tags_matrix.columns[:-1]

X = df_tags_matrix['text_without_stopwords']
y = df_tags_matrix.drop(['text', 'text_without_stopwords'], axis=1).as_matrix()
print(X.shape, y.shape)
# shuffle and make training and test set
X_shuf, y_shuf = shuffle(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_shuf, y_shuf, test_size=0.3, random_state=1)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(min_df=5, max_features=10000)),
    ('clf', OneVsRestClassifier(LinearSVC(verbose=True, C=1.0, class_weight='balanced', max_iter=5000)))])

parameters = {
    'tfidf__min_df': (0, 5, 10),
    'tfidf__max_features': (None, 10000),
    'tfidf__max_df': (0.25, 0.50, 0.75, 0.90),
    'tfidf__ngram_range': [(1,1), (1,2), (1,3), (1,4), (1,5), (2, 2), (2, 3), (2, 4), (2,5), (2,6), (3,3), (3,4), (3,5)]
}

clf_rand = RandomizedSearchCV(pipeline, parameters, n_iter=50, cv=5, n_jobs=30, verbose=0)
clf_rand.fit(X_train, y_train)
joblib.dump(clf_rand, 'clf_tags.pkl')
print("Best Estimator Steps: {}".format(clf_rand.best_estimator_.steps))
print("Best Score: {}".format(clf_rand.best_score_))
print("Best Params: {}".format(clf_rand.best_params_))

predictions = clf_rand.predict(X_test)
print("Accuracy Score: {}".format(accuracy_score(y_test, predictions)))

score = fbeta_score(y_test, predictions, beta=2, average=None)
avg_sample_score = fbeta_score(y_test, clf_rand.predict(X_test), beta=2, average='samples')
print('Average F2 test score {}'.format(avg_sample_score))
print('F2 test scores per tag:')
scores_ = [(mlb.classes_[l], score[l]) for l in score.argsort()[::-1]]


with open('output_tag_classifier.txt', 'w') as f:
    print('Best Score:', clf_rand.best_score_, file=f)
    print('Best Params:', clf_rand.best_params_, file=f)
    print('Scores:', scores_, file=f)
