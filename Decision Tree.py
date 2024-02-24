
"""DecisionTree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DR1RFwxaXyDps0OmshQjCwXFw1kYzMjW
"""

import pandas as pd
import numpy as np
import pprint
import math
from google.colab import drive
drive.mount('/content/drive')


class Tree:
    def __init__(self, vl, l, f):
        self.vl = vl
        self.dict = {}
        for x, y in zip(l, f):
            self.dict[x] = y


class ID3DecisionTree:
    """
    Decision tree using ID3
    """

    def __init__(self):
        pass

    def get_entropy(self, cdf):
        # TODO: Calculate the entropy(s)
        targetColumn = cdf.columns[-1]
        uniqueValue = list(cdf[targetColumn].unique())
        _entropy = 0
        # find entropy for a data set
        for value in uniqueValue:
            _entropy = _entropy - (len(cdf.loc[cdf[targetColumn] == value])/len(cdf)) *\
                math.log2(len(cdf.loc[cdf[targetColumn] == value])/len(cdf))
        return _entropy

    def gain(self, cdf):
        targetColumn = cdf.columns[-1]
        cdfEntropy = self.get_entropy(cdf)
        '''columns -> list of column in pandas series
        axis -> for understaniding the column
        get all columns except targetcolumn
        It should be modified because of high complexity'''
        columns = list(cdf.columns)
        columns.pop()
        chosenColumn = 'NaN'
        mx = -1000000.00
        for col in columns:
            _entropy = 0
            uniqueValue = cdf[col].unique()
            '''expected entropy for each attribute '''
            for value in uniqueValue:
                _entropy = _entropy + (len(cdf.loc[cdf[col] == value])/len(cdf)) *\
                    self.get_entropy((cdf.loc[cdf[col] == value]))
            _entropy = cdfEntropy - _entropy

            if mx < _entropy:
                mx = _entropy
                chosenColumn = str(col)
        return chosenColumn

    def split_table(self, df, attr, value):
        return df[df[attr] == value].reset_index(drop=True).drop(attr, axis=1)

    def fit(self, df):
        targetColumn = df.columns[-1]
        uniqueValue = list(df[targetColumn].unique())
        if len(uniqueValue) == 1 or len(df.columns) <= 2:
            res = ''
            mx = 0.00
            dict = {}
            for rec in df[targetColumn]:
                if rec not in dict:
                    dict[rec] = 0
                dict[rec] = dict[rec]+1
                if mx < dict[rec]:
                    mx = dict[rec]
                    res = rec
            return Tree(res, [], [])
        # compute entropy(s)
        chosen = self.gain(df)
        # Split the df based on the values of max_gain_attr
        li = []
        lii = []
        uniqueValue = df[chosen].unique()
        for vl in uniqueValue:
            li.append(vl)
            lii.append(self.fit(self.split_table(df, chosen, vl)))
        return Tree(chosen, li, lii)

    def predict(self, example, tree, default='unknown'):
        if len(tree.dict) == 0:
            return tree.vl
        attribute = tree.vl
        if example[attribute] in tree.dict.keys():
            subtree = tree.dict[example[attribute]]
            return self.predict(example, subtree)
        else:
            return default

    def evaluate(self, tree, df):
        # TODO: Complete the evaluate method
        correct = 0
        for i in range(len(df)):
            if self.predict(df.iloc[i][0:-1], tree) == df.iloc[i][-1]:
                correct = correct+1
        return correct / len(df)*100

# TODO: Complete the class for decision tree using CART


class CARTDecisionTree:
    def __init__(self):
        pass

    def giniImpurity(self, df):
        target = list(df.columns)[-1]
        uv = df[target].unique()
        sumofs = 0
        for v in uv:
            sumofs = sumofs + math.pow(len(df[df[target] == v]), 2)
        sumofs = sumofs / math.pow(len(df), 2)
        return 1-sumofs

    def get(self, df):
        mn = 1000000
        res = ''
        li = list(df.columns)
        li.pop()
        for col in li:
            uv = df[col].unique()
            avg = 0
            for v in uv:
                avg = avg + (len(df[df[col] == v])/len(df)
                             * self.giniImpurity(df[df[col] == v]))
            if avg < mn:
                mn = avg
                res = col
        return res

    def split_table(self, df, attr, value):
        return df[df[attr] == value].reset_index(drop=True).drop(attr, axis=1)

    def fit(self, df):
        targetColumn = df.columns[-1]
        uniqueValue = list(df[targetColumn].unique())
        if len(uniqueValue) == 1 or len(df.columns) <= 2:
            res = ''
            mx = 0.00
            dict = {}
            for rec in df[targetColumn]:
                if rec not in dict:
                    dict[rec] = 0
                dict[rec] = dict[rec]+1
                if mx < dict[rec]:
                    mx = dict[rec]
                    res = rec
            return Tree(res, [], [])
        # compute entropy(s)
        chosen = self.get(df)
        # Split the df based on the values of max_gain_attr
        li = []
        lii = []
        uniqueValue = df[chosen].unique()
        for vl in uniqueValue:
            li.append(vl)
            lii.append(self.fit(self.split_table(df, chosen, vl)))
        return Tree(chosen, li, lii)

    def predict(self, example, tree, default=None):
        if len(tree.dict) == 0:
            return tree.vl
        attribute = tree.vl
        if example[attribute] in tree.dict.keys():
            subtree = tree.dict[example[attribute]]
            return self.predict(example, subtree)
        else:
            return default

    def evaluate(self, tree, df):
        correct = 0
        for i in range(len(df)):
            if self.predict(df.iloc[i][0:-1], tree) == df.iloc[i][-1]:
                correct = correct+1
        return correct / len(df)*100


# Read the dataset
data_path = '/content/drive/MyDrive/__ML__Practice__Folder__/play_tennis.csv'
df = pd.read_csv(data_path)

# TODO: Shuffle the df randomly
df = df.sample(frac=1)

# TODO: Split the df into train_df and test_df using 80:20 ratio
train_df = df.sample(int(len(df)*0.8), random_state=42).reset_index(drop=True)
test_df = df.drop(train_df.index).reset_index(drop=True)

# debugging code


def show(tree, t=2):
    if len(tree.dict) == 0:
        print(' '*t, "{'", tree.vl, "'}")
        return
    print(' '*t, "{")
    print('*'*(t-1), tree.vl)
    for x, y in tree.dict.items():
        print(' '*t, x)
        show(y, t+1)
    print(' '*t, "}")
    return


# Train the model
model = ID3DecisionTree()
tree = model.fit(train_df)

# Visualize the decision tree
# pprint.pprint(tree.dict)
show(tree)
# Predict an example
x = {'Outlook': 'Sunny', 'Temperature': 'Hot',
     'Humidity': 'High', 'Wind': 'Weak'}
y_pred = model.predict(x, tree)
print("#ID3: Output class:", y_pred)
# Evaluate the model
acc = model.evaluate(tree, test_df)
print("#ID3: Accuracy: {:.3f}".format(acc))

# Train the model
model = CARTDecisionTree()
tree = model.fit(train_df)

# Visualize the decision tree
# pprint.pprint(tree)
show(tree)
# Predict an example
x = {'Outlook': 'Sunny', 'Temperature': 'Hot',
     'Humidity': 'High', 'Wind': 'Weak'}
y_pred = model.predict(x, tree)
print("#CART: Output class:", y_pred)
# Evaluate the model
acc = model.evaluate(tree, test_df)
print("#CART: Accuracy: {:.3f}".format(acc))
