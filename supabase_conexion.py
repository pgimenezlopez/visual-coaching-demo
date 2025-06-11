from datetime import datetime
from typing import List, Dict, Any
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
    try:
        supabase.table("sesiones").insert(data).execute()
    except Exception as e:
        st.error(f"Error guardando sesión: {e}")

def leer_sesiones(usuario: str, cliente: str) -> List[Dict[str, Any]]:
    result = supabase.table("sesiones").select("*").eq("usuario", usuario).eq("cliente", cliente).order("fecha").execute()
    if result.data and isinstance(result.data, list):
        sesiones = []
        for item in result.data:
            item_copy = item.copy()
            try:
                item_copy["Fecha"] = datetime.fromisoformat(item_copy["fecha"]).date() if item_copy["fecha"] else None
            except Exception as e:
                item_copy["Fecha"] = None
                print(f"Error procesando fecha: {item_copy['fecha']} - {e}")
            item_copy["Nivel de claridad (1-10)"] = item_copy["claridad"]
            item_copy["Objetivo de sesión"] = item_copy["objetivo"]
            item_copy["Acción comprometida"] = item_copy["accion"]
            item_copy["Estado de avance"] = item_copy["estado"]
            sesiones.append(item_copy)
        return sesiones
    return []