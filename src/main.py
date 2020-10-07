import numpy as np
import pandas as pd
from random import randint

import DecisionTree as dt
import deps.data_processing.splitter as splitter


N_TREE = 3


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
  data = pd.read_csv('../../dadosBenchmark_validacaoAlgoritmoAD.csv', sep=';')
  sets = splitter.bootstrap(data, N_TREE)
  roots = []
  columns = list(data.columns[:-1])
  list_columns = random_columns(columns, n_max=len(columns)-1)
  for i in range(N_TREE):
    roots.append(dt.DecisionNode(sets[i][0], 'Joga'))
    roots[-1].fit(list_columns[i].copy())
  # print(root.test(data.iloc[12]))