"""
Pipeline ETL - Contratos menores (España)

Ejecución completa:
- parsing
- limpieza
- creación de esquema
- inserción en base de datos

Este archivo solo orquesta el flujo.
"""

from pathlib import Path
from src.config import RAW_DATA_DIR, DDL_PATH  
from src.loader import load_all_atom_folders
from src.transform.cleaning import limpiar_contratos 
from src.db.schema import ejecutar_schema
from src.db.insert import (
    insertar_tablas_maestras,
    insertar_empresas,
    insertar_organos,
    insertar_contratos,
)


def main() -> None:
    print("Iniciando pipeline ETL")

    # --------------------------------------------------
    # 1. Ejecutar esquema SQL
    # --------------------------------------------------
    print("Ejecutando esquema SQL...")
    ejecutar_schema(DDL_PATH)

    # --------------------------------------------------
    # 2. Parsing de archivos ATOM
    # --------------------------------------------------
    print("Parseando archivos .atom...")
    df_raw = load_all_atom_folders(RAW_DATA_DIR)

    # --------------------------------------------------
    # 3. Limpieza y normalización
    # --------------------------------------------------
    print("Limpiando datos...")
    df_clean = limpiar_contratos(df_raw)

    # --------------------------------------------------
    # 4. Inserción en base de datos
    # --------------------------------------------------
    print("Insertando tablas maestras...")
    insertar_tablas_maestras()

    print("Insertando empresas...")
    df_clean = insertar_empresas(df_clean)

    print("Insertando órganos...")
    df_clean = insertar_organos(df_clean)

    print("Insertando contratos...")
    insertar_contratos(df_clean)

    print("Pipeline ETL finalizado correctamente")


if __name__ == "__main__":
    main()