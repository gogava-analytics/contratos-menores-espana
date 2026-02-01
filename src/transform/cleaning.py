"""
Limpieza y normalización del DataFrame de contratos.
"""

import pandas as pd


COLUMNAS_A_ELIMINAR = [
    "objeto_contrato",
    "id_expediente",
    "organo_contratacion_resumen",
    "estado_resumen",
    "importe_resumen",
    "importe_adjudicado_con_IVA",
    "importe_adjudicado_sin_IVA",
]


def limpiar_contratos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.drop(
        columns=COLUMNAS_A_ELIMINAR,
        errors="ignore"
    )

    df["id_entry_num"] = (
        df["id_entry"]
        .astype(str)
        .str.extract(r"(\d+)$")
    )

    df = df.drop_duplicates(
        subset=["id_entry_num"],
        keep="last"
    )

    return df
