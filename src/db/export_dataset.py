"""
Exportación de dataset analítico para storytelling.

Responsabilidad:
- leer datos desde la base de datos (fuente de verdad)
- realizar joins entre tablas normalizadas
- generar un dataset denormalizado (1 fila = 1 contrato)
- exportar a formato Parquet y CSV
"""

from pathlib import Path
import pandas as pd

from src.db.engine import engine


# Directorio de salida de datasets analíticos
EXPORT_DIR = Path("data/export")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def exportar_dataset() -> None:
    """
    Genera el dataset analítico a partir de la base de datos
    y lo exporta a Parquet y CSV.
    """

    query = """
    SELECT
        c.id_entry_num,
        c.id_entry,
        c.titulo,
        c.id_licitacion,
        c.fecha_actualizacion,
        c.fecha_adjudicacion,
        c.estado,

        tc.nombre_contrato AS tipo_contrato,
        c.codigo_subtipo_contrato,

        c.importe_estimado,
        c.importe_total,
        c.importe_sin_impuestos,

        c.codigo_cpv_principal,
        c.codigo_region_nuts,
        c.ofertas_recibidas,
        c.id_plataforma,

        e.empresa_nombre,
        e.nif_empresa,
        e.empresa_es_pyme,
        e.empresa_pais,

        o.organo_nombre,
        o.organo_dir3,
        o.organo_postalcode,
        o.organo_localidad,
        o.organo_email,
        o.organo_telefono,
        o.organo_nif,

        to2.nombre_tipo_organo AS tipo_organo,
        tao.nombre_actividad_organo AS actividad_organo

    FROM contrato c
    LEFT JOIN empresa e ON c.contr_empresa_id = e.empresa_id
    LEFT JOIN organo o ON c.contr_organo_id = o.organo_id
    LEFT JOIN tipo_contrato tc ON c.codigo_tipo_contrato = tc.codigo_tipo_contrato
    LEFT JOIN tipo_organo to2 ON o.tipo_organo_codigo = to2.codigo_tipo_organo
    LEFT JOIN tipo_actividad_organo tao ON o.actividad_organo_codigo = tao.codigo_actividad_organo
    """

    df = pd.read_sql(query, engine)

    parquet_path = EXPORT_DIR / "contratos_menores_test.parquet"
    csv_path = EXPORT_DIR / "contratos_menores_test.csv"

    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False)

    print("Dataset analítico generado correctamente")
    print(f"Parquet: {parquet_path}")
    print(f"CSV:     {csv_path}")


if __name__ == "__main__":
    exportar_dataset()