from pathlib import Path
from sqlalchemy import text

from src.db.engine import engine


def ejecutar_schema(ddl_path: Path) -> None:
    """
    Ejecuta un archivo DDL (.sql) en la base de datos.

    Parameters
    ----------
    ddl_path : Path
        Ruta al archivo SQL con el esquema
    """
    if not ddl_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo DDL: {ddl_path}"
        )

    ddl_sql = ddl_path.read_text(encoding="utf-8")

    # Separar sentencias por ;
    statements = [
        stmt.strip()
        for stmt in ddl_sql.split(";")
        if stmt.strip()
    ]

    with engine.connect() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
        conn.commit()

    print("✅ Esquema SQL ejecutado correctamente")
