import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

RUT_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "17DucEMBJ6wfZhBT4Y2ngMz9o1pUw5oTOBs38us5KTTQ/edit?gid=48935242#gid=48935242"
)


def _get_client():
    try:
        secrets = st.secrets["gcp_service_account"]
        creds_dict = {
            "type": secrets["type"],
            "project_id": secrets["project_id"],
            "private_key_id": secrets["private_key_id"],
            "private_key": secrets["private_key"],
            "client_email": secrets["client_email"],
            "client_id": secrets["client_id"],
            "auth_uri": secrets["auth_uri"],
            "token_uri": secrets["token_uri"],
            "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": secrets["client_x509_cert_url"],
            "universe_domain": secrets["universe_domain"],
        }
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error conectando a Google Sheets (RUT): {e}")
        return None


@st.cache_data(ttl=600)
def _cargar_rut_sheet() -> pd.DataFrame:
    client = _get_client()
    if not client:
        return pd.DataFrame()
    try:
        sh = client.open_by_url(RUT_SHEET_URL)
        ws = sh.get_worksheet_by_id(48935242)
        data = ws.get_all_values()
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    except Exception as e:
        st.error(f"Error cargando hoja RUT: {e}")
        return pd.DataFrame()


def buscar_por_rut(rut: str) -> dict:
    """Busca un RUT en la hoja maestra y devuelve sus datos asociados.

    Args:
        rut: RUT a buscar (con o sin puntos, mayúsculas/minúsculas).

    Returns:
        dict con las columnas de la hoja, o dict vacío si no se encuentra.
    """
    rut_limpio = str(rut).replace(".", "").strip().upper()
    df = _cargar_rut_sheet()
    if df.empty or "RUT" not in df.columns:
        return {}

    df["RUT"] = df["RUT"].astype(str).str.replace(".", "", regex=False).str.strip().str.upper()
    match = df[df["RUT"] == rut_limpio]

    if match.empty:
        return {}

    row = match.iloc[0].to_dict()
    return {k: str(v) if pd.notna(v) else "" for k, v in row.items()}
