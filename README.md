# Modo de usar

```
python3 src/main.py < caminho para o dataset > < separador usado pelo csv > < coluna das classes > -na < lista de colunas com atributos numéricos >
```

# Exemplo

```
python3 main.py '../../diabetes.csv' ',' 'Outcome' -na Pregnancies Glucose BloodPressure SkinThickness Insulin BMI DiabetesPedigreeFunction Age Outcome
```

# Instalar dependências

```
pip install -r requirements.txt
```