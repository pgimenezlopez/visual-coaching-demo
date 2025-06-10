from supabase import create_client
import streamlit as st
from supabase._sync.client import SyncClient

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase: SyncClient = create_client(url, key)

def guardar_sesion(usuario, cliente, fecha, claridad, objetivo, accion, estado):
    data = {
        "usuario": usuario,
        "cliente": cliente,
        "fecha": fecha.isoformat(),
        "claridad": claridad,
        "objetivo": objetivo,
        "accion": accion,
        "estado": estado
    }
    supabase.table("sesiones").insert(data).execute()

def leer_sesiones(usuario, cliente):
    result = supabase.table("sesiones").select("*").eq("usuario", usuario).eq("cliente", cliente).order("fecha").execute()
    if result.data:
        sesiones = []
        for item in result.data:
            try:
                item["Fecha"] = datetime.fromisoformat(item["fecha"]).date() if item["fecha"] else None
            except Exception as e:
                item["Fecha"] = None
                print(f"Error procesando fecha: {item['fecha']} - {e}")
            item["Nivel de claridad (1-10)"] = item["claridad"]
            item["Objetivo de sesión"] = item["objetivo"]
            item["Acción comprometida"] = item["accion"]
            item["Estado de avance"] = item["estado"]
            sesiones.append(item)
        return sesiones
    return []