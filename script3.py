import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Simulamos datos de tu comercio (luego esto vendrá de tu Excel real)
# visitas, tiempo_en_pagina, agrego_al_carrito, compro? (1=si, 0=no)
datos = pd.DataFrame({
    'visitas': [1, 5, 2, 10, 3, 8, 1, 12],
    'tiempo_min': [1, 10, 2, 15, 3, 9, 0.5, 20],
    'carrito': [0, 1, 0, 1, 0, 1, 0, 1],
    'compro': [0, 1, 0, 1, 0, 1, 0, 1]
})

X = datos[['visitas', 'tiempo_min', 'carrito']]
y = datos['compro']

# 2. Entrenar
modelo = RandomForestClassifier()
modelo.fit(X, y)

# 3. GUARDAR el cerebro entrenado en un archivo
joblib.dump(modelo, 'modelo_tienda.pkl')
print("Modelo guardado como modelo_tienda.pkl")