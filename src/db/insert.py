import pandas as pd

from src.db.engine import engine
from src.config import (
    MAPA_TIPO_CONTRATO,
    MAPA_TIPO_ORGANO,
    MAPA_ACTIVIDAD_ORGANO,
)


# ======================================================
# TABLAS MAESTRAS
# ======================================================

def insertar_tablas_maestras() -> None:
    """
    Inserta las tablas de referencia (catálogos).
    Se ejecuta una sola vez.
    """
    pd.DataFrame(
        MAPA_TIPO_CONTRATO.items(),
        columns=["codigo_tipo_contrato", "nombre_contrato"]
    ).to_sql(
        "tipo_contrato",
        engine,
        if_exists="append",
        index=False
    )

    pd.DataFrame(
        MAPA_TIPO_ORGANO.items(),
        columns=["codigo_tipo_organo", "nombre_tipo_organo"]
    ).to_sql(
        "tipo_organo",
        engine,
        if_exists="append",
        index=False
    )

    pd.DataFrame(
        MAPA_ACTIVIDAD_ORGANO.items(),
        columns=["codigo_actividad_organo", "nombre_actividad_organo"]
    ).to_sql(
        "tipo_actividad_organo",
        engine,
        if_exists="append",
        index=False
    )


# ======================================================
# EMPRESA
# ======================================================

def insertar_empresas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Inserta empresas y devuelve el DataFrame original
    con empresa_id obtenido desde SQL.
    """
    df_empresa = (
        df[
            [
                "nif_empresa",
                "empresa_ganadora",
                "pais_empresa",
                "es_pyme_empresa",
            ]
        ]
        .groupby(
            ["nif_empresa", "empresa_ganadora"],
            dropna=False
        )
        .last()
        .reset_index()
        .rename(
            columns={
                "empresa_ganadora": "empresa_nombre",
                "pais_empresa": "empresa_pais",
                "es_pyme_empresa": "empresa_es_pyme",
            }
        )
    )

    df_empresa.to_sql(
        "empresa",
        engine,
        if_exists="append",
        index=False
    )

    # Leer IDs desde SQL
    df_empresa_sql = pd.read_sql(
        "SELECT * FROM empresa",
        engine
    )

    # Merge para obtener empresa_id
    df = df.merge(
        df_empresa_sql[
            ["empresa_id", "empresa_nombre", "nif_empresa"]
        ],
        how="left",
        left_on=["empresa_ganadora", "nif_empresa"],
        right_on=["empresa_nombre", "nif_empresa"]
    ).drop(columns=["empresa_nombre"])

    return df


# ======================================================
# ORGANO
# ======================================================

def insertar_organos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Inserta órganos de contratación y devuelve el DataFrame
    con organo_id obtenido desde SQL.
    """
    df_organo = (
        df[
            [
                "id_dir3",
                "nombre_organo",
                "tipo_organo_codigo",
                "actividad_organo_codigo",
                "codigo_postal_organo",
                "localidad_organo",
                "email_organo",
                "telefono_organo",
                "nif_organo",
            ]
        ]
        .groupby(
            ["nombre_organo", "nif_organo", "id_dir3"],
            dropna=False
        )
        .last()
        .reset_index()
        .rename(
            columns={
                "id_dir3": "organo_dir3",
                "nombre_organo": "organo_nombre",
                "codigo_postal_organo": "organo_postalcode",
                "localidad_organo": "organo_localidad",
                "email_organo": "organo_email",
                "telefono_organo": "organo_telefono",
                "nif_organo": "organo_nif",
            }
        )
    )

    df_organo.to_sql(
        "organo",
        engine,
        if_exists="append",
        index=False
    )

    # Leer IDs desde SQL
    df_organo_sql = pd.read_sql(
        "SELECT * FROM organo",
        engine
    )

    # Merge para obtener organo_id
    df = df.merge(
        df_organo_sql[
            ["organo_id", "organo_nombre", "organo_nif", "organo_dir3"]
        ],
        how="left",
        left_on=["nombre_organo", "nif_organo", "id_dir3"],
        right_on=["organo_nombre", "organo_nif", "organo_dir3"]
    ).drop(
        columns=["organo_nombre", "organo_nif", "organo_dir3"]
    )

    return df


# ======================================================
# CONTRATO
# ======================================================

def insertar_contratos(df: pd.DataFrame) -> None:
    """
    Inserta contratos en la base de datos.
    """
    df_contrato = df[
        [
            "id_entry_num",
            "id_entry",
            "titulo",
            "id_licitacion",
            "fecha_actualizacion",
            "fecha_adjudicacion",
            "estado",
            "codigo_tipo_contrato",
            "codigo_subtipo_contrato",
            "importe_estimado",
            "importe_total",
            "importe_sin_impuestos",
            "codigo_cpv_principal",
            "codigo_region_nuts",
            "ofertas_recibidas",
            "id_plataforma",
            "organo_id",
            "empresa_id",
        ]
    ].rename(
        columns={
            "organo_id": "contr_organo_id",
            "empresa_id": "contr_empresa_id",
        }
    )

    df_contrato.to_sql(
        "contrato",
        engine,
        if_exists="append",
        index=False
    )
