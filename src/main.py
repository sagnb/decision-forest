import numpy as np
import pandas as pd
from random import randint
import argparse

import DecisionTree as dt
import deps.data_processing.splitter as splitter
import deps.data_processing.normalizer as normalizer


N_TREE = 5


def parse():
  parser = argparse.ArgumentParser(description='Decision Tree')
  parser.add_argument('path')
  parser.add_argument('sep')
  parser.add_argument('target')
  parser.add_argument('-na', '--numeric_attributes', nargs='+')
  return parser.parse_args()


def random_columns(columns, k=N_TREE, n_min=2, n_max=2):
  if n_max >= n_min: 
    list_columns = []
    for _ in range(k):
      n_columns = randint(n_min, n_max)
      new_columns = []
      copy_columns = columns.copy()
      for _ in range(n_columns):
        index = randint(0, len(copy_columns) - 1)
        column = copy_columns.pop(index)
        new_columns.append(column)
      list_columns.append(new_columns)
    return list_columns
  else:
    return [columns for _ in range(k)]


if __name__ == '__main__':
  args = parse()
  data = pd.read_csv(args.path, sep=args.sep)
  if args.numeric_attributes:
    data = normalizer.min_max(data, args.numeric_attributes, True)
  list_train, list_test = splitter.cross_validation(data, args.target, 2)
  for train_data, test_data in zip(list_train, list_test):
    sets = splitter.bootstrap(train_data, N_TREE)
    roots = []
    columns = list(train_data.columns[:-1])
    list_columns = random_columns(columns, n_max=len(columns)-1)
    for i in range(N_TREE):
      roots.append(dt.DecisionNode(sets[i][0], args.target))
      roots[-1].fit(list_columns[i].copy())
    list_results = []
    test_index = randint(0, test_data.shape[0]-1)
    for i in range(N_TREE):
      list_results.append(roots[i].test(test_data.iloc[test_index]))
    print(test_data.iloc[test_index])
    print(pd.Series(list_results).value_counts().index[0])
