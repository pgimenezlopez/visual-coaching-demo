from datetime import date, datetime

import pandas as pd
import plotly.express as px
import streamlit as st
import openai

from supabase_conexion import guardar_sesion, leer_sesiones

st.set_page_config(page_title="Dashboard de Coaching", layout="wide")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Dashboard de Coaching Personalizado")
st.markdown("Seguimiento visual y registro de procesos de coaching con datos en la nube (Supabase).")

# Usuario simulado (en producción, usar login real)
usuario_email = "coachdemo@email.com"

# Ingreso manual o selección de cliente
clientes = ["Lucía", "Marcos"]
st.markdown("## 🧑‍💼 Cliente")
if st.checkbox("Agregar nuevo cliente"):
    cliente_input = st.text_input("Nombre del nuevo cliente")
else:
    cliente_input = st.selectbox("Seleccionar cliente", clientes)

# Formulario de registro
st.markdown("## ✍️ Registrar nueva sesión")
with st.form("registro_sesion"):
    fecha = st.date_input("Fecha de sesión", value=date.today())
    claridad = st.slider("Nivel de claridad (1-10)", 1, 10, 5)
    objetivo = st.text_input("Objetivo trabajado")
    accion = st.text_input("Acción comprometida")
    estado = st.selectbox("Estado de avance", ["Completado", "En progreso", "Pendiente"])
    submitted = st.form_submit_button(label="💾 Guardar sesión")

    if submitted and cliente_input:
        guardar_sesion(usuario_email, cliente_input, fecha, claridad, objetivo, accion, estado)
        st.success("✅ Sesión guardada exitosamente")

# Visualización
if cliente_input:
    sesiones = leer_sesiones(usuario_email, cliente_input)
    if sesiones:
        df = pd.DataFrame(sesiones)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Sesiones", len(df))
        col2.metric("Prom. claridad", round(df["Nivel de claridad (1-10)"].mean(), 2))
        col3.metric("Acciones completadas", f"{(df['Estado de avance'] == 'Completado').sum()} / {len(df)}")

        col_izq, col_der = st.columns([2, 1])
        with col_izq:
            st.subheader("📈 Evolución de claridad")
            fig = px.line(df, x="Fecha", y="Nivel de claridad (1-10)", markers=True)
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col_der:
            st.subheader("📋 Sesiones")
            st.dataframe(df[["Fecha", "Objetivo de sesión", "Estado de avance"]].rename(columns={
                "Fecha": "🗓 Fecha",
                "Objetivo de sesión": "🎯 Objetivo",
                "Estado de avance": "📌 Estado"
            }), use_container_width=True)

        st.markdown("---")
        ultima = df.iloc[-1]
        st.markdown("### 🧠 Última sesión registrada")
        st.markdown(f"🗓️ Fecha: **{ultima['Fecha']}**")
        st.markdown(f"🎯 Objetivo: _{ultima['Objetivo de sesión']}_")
        st.markdown(f"📌 Acción comprometida:")
        st.code(ultima["Acción comprometida"])
        st.markdown(f"✅ Estado: **{ultima['Estado de avance']}**")
    else:
        st.info("No hay sesiones registradas todavía.")

# -------------------------------
# Módulo de IA: Próximos pasos
# -------------------------------
from ia_proximos_pasos import generar_proximos_pasos

st.markdown("---")
st.markdown("## 🤖 IA: Próximos pasos sugeridos")

texto_sesion = st.text_area("📄 Ingresá una nota libre de la sesión o comentario del cliente", height=200)

if st.button("Generar próximos pasos"):
    if texto_sesion.strip():
        pasos = generar_proximos_pasos(texto_sesion)
        st.markdown("### ✅ Próximos pasos generados por IA")
        st.write(pasos)
    else:
        st.warning("Por favor, ingresá algún texto para poder generar sugerencias.")
