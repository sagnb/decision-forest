import numpy as np
import pandas as pd

import DecisionTree as dt


if __name__ == '__main__':
  data = pd.read_csv('../../dadosBenchmark_validacaoAlgoritmoAD.csv', sep=';')
  root = dt.DecisionNode(data, 'Joga')
  root.fit(list(data.columns))
  print(root.test(data.iloc[12]))