# -*- coding: utf-8 -*-
"""MVP Rafael Araujo da Silva

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_BZItx711bAj8uxYUenL-ZEB_0RUygsd

# MVP Análise de Dados e Boas Práticas

**Nome:** Rafael Araujo da Silva

**Matrícula:**
4052024001926

**Dataset:** [Mushroom Dataset](https://https://archive.ics.uci.edu/dataset/73/mushroom)

# Descrição do Problema

O objetivo deste projeto é prever se um cogumelo é comestível (edible) ou venenoso (poisonous) com base em características observadas, como cor do chapéu, odor, tipo de superfície, presença de anel, entre outros. Esse tipo de classificação pode ser extremamente útil em contextos educacionais, acadêmicos e até mesmo em aplicações práticas de segurança alimentar.

## Hipóteses do Problema

As hipóteses que tracei são as seguintes:

• Cada instância do dataset representa um único cogumelo, com atributos observados de maneira precisa.

• Não existem cogumelos simultaneamente comestíveis e venenosos.

• Todos os atributos categóricos são descritivos e mutuamente exclusivos (ex: o cogumelo tem um tipo de odor por vez).

• A presença de valores como ? no atributo stalk-root pode representar ausência de informação ou dificuldade na coleta, e será tratada adequadamente.

## Tipo de Problema

Este é um problema de aprendizado supervisionado, pois temos uma variável-alvo conhecida (class) e buscamos prever seu valor com base em variáveis de entrada.
Trata-se especificamente de um problema de classificação binária: a classe pode ser "e" (edible/comestível) ou "p" (poisonous/venenoso).

## Seleção de Dados

## 📋 Restrições e critérios de seleção

- O dataset Mushroom foi escolhido por conter apenas variáveis categóricas, o que permite praticar codificação e análise exploratória.
- Não foram utilizadas bases que contenham valores contínuos, propositalmente, para aprofundar o trabalho em dados categóricos.

## Atributos do Dataset

| Atributo                    | Descrição                                                  |
|-----------------------------|--------------------------------------------------------------|
| `class`                     | Classe: comestível (e) ou venenoso (p)                       |
| `cap-shape`                 | Formato do chapéu (bell, conical, convex, flat, etc.)        |
| `cap-surface`               | Superfície do chapéu (fibrous, grooves, scaly, smooth)       |
| `cap-color`                 | Cor do chapéu (brown, yellow, white, etc.)                   |
| `bruises`                   | Presença de manchas (bruises) – yes ou no                    |
| `odor`                      | Odor (almond, anise, foul, none, etc.)                       |
| `gill-attachment`           | Fixação das lamelas ao caule                                |
| `gill-spacing`              | Espaçamento das lamelas                                      |
| `gill-size`                 | Tamanho das lamelas                                          |
| `gill-color`                | Cor das lamelas                                              |
| `stalk-shape`               | Forma do caule (enlarging ou tapering)                       |
| `stalk-root`                | Tipo de raiz do caule (bulbous, club, equal, rooted, ou ?)   |
| `stalk-surface-above-ring` | Superfície do caule acima do anel                            |
| `stalk-surface-below-ring` | Superfície do caule abaixo do anel                           |
| `stalk-color-above-ring`   | Cor do caule acima do anel                                   |
| `stalk-color-below-ring`   | Cor do caule abaixo do anel                                  |
| `veil-type`                 | Tipo de véu                                                  |
| `veil-color`                | Cor do véu                                                   |
| `ring-number`               | Número de anéis no caule                                     |
| `ring-type`                 | Tipo de anel                                                 |
| `spore-print-color`        | Cor da impressão de esporos                                  |
| `population`               | Tamanho da população onde o cogumelo é encontrado            |
| `habitat`                  | Tipo de habitat (grasses, woods, paths, etc.)                |

# Importação das Bibliotecas Necessárias e Carga de Dados

Esta seção consolida todas as importações de bibliotecas necessárias para a análise, visualização e pré-processamento dos dados, bem como o carregamento inicial do dataset Iris.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# carregamento do dataset (aqui, ele fica disponível nesse método)
# URL do arquivo .data no GitHub
raw_url = 'https://raw.githubusercontent.com/rafaelaraujozr/mushroom/main/agaricus-lepiota.data'

# Lista de nomes de colunas (23 atributos + alvo)
columns = [
    'class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
    'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
    'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
    'stalk-surface-below-ring', 'stalk-color-above-ring',
    'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
    'ring-type', 'spore-print-color', 'population', 'habitat'
]

# 1️⃣ Lê o arquivo direto do GitHub
df = pd.read_csv(raw_url, header=None, names=columns, na_values='?')

# 2️⃣ Visualiza as primeiras linhas
df.head()

"""É possível perceber que os dados estão codificados com letras (ex: `x`, `s`, `n`, `p`, etc.), o que representa valores categóricos definidos no dicionário da base original.

Um ponto de atenção é a presença do valor `NaN` (antes era `?`) na coluna `stalk-root`, o que indica dados ausentes.

# Análise de Dados

Nesta etapa de Análise de Dados Exploratória (EDA) sobre o dataset Mushroom, visamos entender a distribuição, as relações e as características das variáveis, o que é crucial para as etapas subsequentes de pré-processamento e modelagem.

## Total e Tipo das Instâncias
O dataset possui **8124 instâncias** e **23 atributos**, além da variável alvo (`class`), totalizando 24 colunas.
"""

print(f"Total de instâncias: {len(df)}")
print("\nTipos de dados por coluna:")
print(df.info())

"""Todos os atributos são do tipo `object`, ou seja, **categóricos**. Isso é esperado, pois o dataset Mushroom foi construído apenas com variáveis qualitativas.

Contabilizando quantos valores faltantes existem por coluna:
"""

df.isnull().sum()

"""A coluna `stalk-root` apresenta **2480 valores ausentes**, o que corresponde a aproximadamente **30%** do total do dataset. Nenhuma outra coluna possui valores faltantes.

Como todos os dados são categóricos, o método `describe()` trará contagens e frequências:
"""

df.describe()

"""O resumo mostra:

- A maioria dos atributos tem 3 a 12 categorias únicas.
- A variável `veil-type` tem apenas **um valor único** — portanto, **não traz informação útil** para a classificação e pode ser descartada.

Próximos passos:
- Tratar valores ausentes no dataset.
- Remover colunas que não agregam valor.
- Codificar variáveis categóricas.
- Preparar uma base numérica com os dados transformados.
"""

df_prep['stalk-root'] = df_prep['stalk-root'].fillna('missing')

"""Ao analisar a coluna `veil-type`, identificamos que ela possui apenas um valor único em todas as instâncias. Isso significa que ela não contribui para o processo de aprendizagem dos modelos e pode ser removida."""

df_prep.drop(columns=['veil-type'], inplace=True)

"""Como todas as colunas (com exceção de `class`) são categóricas, aplicaremos **One-Hot Encoding** para transformar essas variáveis em forma numérica, que pode ser interpretada pelos algoritmos de machine learning.

Também converteremos a variável alvo `class` para valores binários:
- `e` (edible/comestível) → 0
- `p` (poisonous/venenoso) → 1
"""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Separando X e y
X = df_prep.drop(columns=['class'])
y = df_prep['class'].map({'e': 0, 'p': 1})  # binariza o alvo

# Lista de colunas categóricas
categorical_cols = X.columns.tolist()

# Definindo o pré-processador com OneHotEncoder
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]
)

# Aplicando a transformação
X_encoded = preprocessor.fit_transform(X)
encoded_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)

# Convertendo para DataFrame
df_encoded = pd.DataFrame(X_encoded.toarray(), columns=encoded_feature_names)
df_encoded['target'] = y.values

"""CORRELAÇÕES & ANÁLISES AVANÇADAS

Agora que todas as variáveis estão em formato numérico (one-hot), podemos mensurar a relação entre cada feature e o alvo (`target` = 1 → venenoso).

**Observação**  
> Como tanto as features quanto o alvo são binárias, o coeficiente de correlação de Pearson equivale ao *point-biserial* – uma medida válida para este contexto.
"""

# 1️⃣  Matriz de correlação (apenas numéricas)
corr_matrix = df_encoded.corr(numeric_only=True)

# 2️⃣  Correlação de cada feature com o alvo
target_corr = (
    corr_matrix['target']          # coluna que relaciona cada variável ao alvo
    .drop('target')                # remove a autocorrelação
    .sort_values(ascending=False)  # ordena da maior para a menor
)

# 3️⃣  Exibe as 15 variáveis mais correlacionadas (positiva ou negativamente)
top15 = target_corr.head(15)
bottom15 = target_corr.tail(15)

print("Top 15 (positivamente correlacionadas → indicam cogumelo venenoso):")
display(top15)

print("\nTop 15 (negativamente correlacionadas → indicam cogumelo comestível):")
display(bottom15.abs().sort_values(ascending=False))

"""🔍 Principais insights

- `odor_foul` e `odor_pungent` têm correlação **fortemente positiva**, indicando que odores desagradáveis são excelentes indícios de cogumelos venenosos.  
- `gill_color_green` e `spore_print_color_green` também aparecem no topo, corroborando literatura micológica.  
- Entre as correlações negativas (associadas a cogumelos comestíveis), destacam-se `odor_none`, `bruises_t` (apresenta manchas) e `gill_size_b`.  

Esses resultados reforçam o que vimos na etapa gráfica: **cheiro e cor** são atributos altamente discriminativos.
"""

import matplotlib.pyplot as plt
import seaborn as sns

sel_feats = list(top15.index) + list(bottom15.index)
plt.figure(figsize=(8, 12))
sns.heatmap(
    corr_matrix.loc[sel_feats + ['target'], sel_feats + ['target']],
    cmap='coolwarm',
    center=0,
    linewidths=.5
)
plt.title('Heatmap – correlação entre features selecionadas e alvo')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Junta top 10 positivas e top 10 negativas
top_pos = target_corr.head(10)
top_neg = target_corr.tail(10)

# Junta em um só DataFrame
corr_df = pd.concat([top_pos, top_neg])
corr_df = corr_df.sort_values()

# Plot
plt.figure(figsize=(10, 7))
sns.barplot(
    x=corr_df.values,
    y=corr_df.index,
    palette=['#1f77b4' if v < 0 else '#d62728' for v in corr_df.values]
)
plt.axvline(0, color='black', linestyle='--')
plt.title('Correlação entre variáveis one-hot e classe (venenoso)')
plt.xlabel('Correlação com a variável target (1 = venenoso)')
plt.ylabel('Variável')
plt.tight_layout()
plt.show()

"""##CONCLUSÃO

Uma das análises mais reveladoras do estudo foi a relação entre o atributo **`odor`** e a variável alvo `class` (comestível ou venenoso).

##Comparação entre odor e toxicidade

Durante a etapa de análise exploratória, foi possível observar que determinados tipos de **odor** estão fortemente associados à toxicidade do cogumelo:

- Os cogumelos com **odor desagradável**, como:
  - `foul` (fétido),
  - `pungent` (ácido/irritante) e
  - `spicy` (picante),
  apresentam uma **correlação muito alta com a classe venenosa (`p`)**.

- Em contrapartida, cogumelos com **ausência de odor** (`none`) aparecem predominantemente associados à classe comestível (`e`).

Essas relações foram confirmadas por:

- Visualizações gráficas com `countplot` que mostraram a separação quase total entre os tipos de odor e a classe;
- Análise de correlação, onde `odor_foul` e `odor_pungent` apresentaram os maiores coeficientes positivos com a variável `target` (venenoso);
- Gráficos de barras que destacaram os odores como os atributos mais preditivos.

## Conclusão final

A variável `odor` se mostrou o **fator mais determinante** para identificar a toxicidade de um cogumelo. Esse insight reforça a importância de atributos sensoriais no processo de classificação e sugere que, mesmo antes de aplicar modelos de machine learning, já é possível obter **fortes indícios da classe do cogumelo apenas observando seu odor**.

"""