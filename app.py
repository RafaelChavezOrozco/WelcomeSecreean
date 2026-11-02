import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="WelcomeScreen - ShopIA", layout="centered")

# Cargar modelo
modelo = joblib.load('modelo_tienda.pkl')

# =========================================
# PARTE 0: PANTALLA DE BIENVENIDA
# =========================================
if 'entrado' not in st.session_state:
    st.session_state.entrado = False

# Si NO ha entrado, muestra solo la bienvenida
if not st.session_state.entrado:
    st.title("WelcomeScreen 🛒✨")
    st.header("Bienvenido a ShopIA")
    st.write("Sistema inteligente de predicción para comercio digital")
    st.write("---")
    st.write("**¿Qué hace este proyecto?**")
    st.write("1. Analiza el comportamiento del cliente")
    st.write("2. Calcula la probabilidad de que compre")
    st.write("3. Guarda el historial y genera gráficas")

    st.write("")
    st.write("")

    # El botón mágico para entrar
    if st.button("Entrar a la Tienda ->"):
        st.session_state.entrado = True
        st.rerun()  # Recarga la página para mostrar la tienda

    st.stop()  # IMPORTANTE: Aquí se detiene y no muestra lo demás hasta que le des al botón

# =========================================
# PARTE 1: TIENDA (Solo se ve después de dar al botón)
# =========================================
st.title("Mi Predictor de Ventas")
st.write("Página de prueba para comercio digital")

if st.button("← Volver a Bienvenida"):
    st.session_state.entrado = False
    st.rerun()

st.header("1. ¿Este cliente va a comprar?")
visitas = st.slider("Cuántas veces ha visitado la tienda", 1, 20, 3)
tiempo = st.slider("Minutos en la página", 0, 30, 5)
carrito = st.selectbox("¿Agregó al carrito?", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")

if st.button("Calcular probabilidad y GUARDAR"):
    datos_nuevo = [[visitas, tiempo, carrito]]
    prob = modelo.predict_proba(datos_nuevo)
    prob_compra = prob[0][1] * 100

    st.metric("Probabilidad de que COMPRE", f"{prob_compra:.1f}%")
    st.progress(prob[0][1])

    nuevo_registro = {
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'visitas': visitas,
        'tiempo_min': tiempo,
        'carrito': carrito,
        'probabilidad': prob_compra,
    }

    archivo = 'historial_ventas.csv'
    if not os.path.exists(archivo):
        pd.DataFrame([nuevo_registro]).to_csv(archivo, index=False)
    else:
        pd.DataFrame([nuevo_registro]).to_csv(archivo, mode='a', header=False, index=False)

    st.success(f"Guardado en {archivo}")

st.header("2. Dashboard")
archivo = 'historial_ventas.csv'
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
    st.write(f"Llevas {len(df)} clientes guardados.")
    st.dataframe(df.tail(5))
    fig1 = px.histogram(df, x='probabilidad', nbins=10, title="Probabilidad de compra")
    st.plotly_chart(fig1)
else:
    st.info("Aún no hay historial. Dale a Calcular.")