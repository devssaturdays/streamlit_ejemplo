import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

df = pd.DataFrame(pd.read_csv("student-mat.csv", sep = ";"))

# Por simplicidad usaremos solo la ultima evaluación:
df = df.drop(["G1","G2"], axis = 1)

# Lista de columnas:
cols = df.columns.tolist()

# Lista de columnas numericas:
nc = []
for col in df:
	if df[col].astype(str).str.isnumeric().any():
		nc.append(col)


with st.sidebar:
	op = st.radio("Opcion", ["Información general", "Análisis estadístico"])

if op == "Información general":
	with open("info.txt", "r") as f:
		for line in f:
			st.write(line)

else:
	'''
	### Podemos empezar viendo como se distribuyen las notas dependiendo de los datos socioeconomicos de los que disponemos.
	'''
	cols.pop()						# No queremos que se pueda seleccionar G3

	col = st.selectbox("Columna a comparar", cols)

	val = []

	if col in nc:
		# columnas numericas
		left, right = st.beta_columns((1,4))
		left.write("")
		left.write("")
		t = left.checkbox("Rango")

		minimum = int(df[col].min())
		maximum = int(df[col].max())
		value = minimum	
		step = 1
		
		if t:
			value = (minimum, maximum)

		slider = right.slider("Valor", minimum, maximum, value, step)

		val.append(df.G3.values)

		if t == False:
			val.append(df.loc[df[col] <= slider, "G3"].values)
			val.append(df.loc[df[col] > slider, "G3"].values)
			labels = ["General", "Menor o igual", "Mayor"]
		else:
			elements = df.loc[df[col] >= slider[0], "G3"]
			elements = np.intersect1d(elements, df.loc[df[col] <= slider[1], "G3"])
			elements = pd.Series(elements)
			val.append(elements.values)
			labels = ["General", "En rango"]
	else:
		# columnas categoricas
		labels = []
		for i in df[col].unique():
			val.append(df.loc[df[col]==i, "G3"].values)
			labels.append(i)

	fig, ax = plt.subplots(figsize = (20,10))
	plt.rcParams.update({'font.size': 44})

	plt.boxplot(val, labels = labels)
	st.write(fig)

