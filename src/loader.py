from pathlib import Path
import pandas as pd
from src.atom_parser import parse_atom_file


def load_all_atom_folders(base_folder: Path) -> pd.DataFrame:
    """
    Lee todos los archivos .atom de todas las subcarpetas
    (ej: 2020/, 2021/, 2022/, etc.) y devuelve un DataFrame unificado.
    """
    all_dfs = []
    
    # Iterar sobre cada subcarpeta (años)
    for year_folder in base_folder.iterdir():
        if not year_folder.is_dir():
            continue
        
        print(f"\nProcesando carpeta: {year_folder.name}")
        
        atom_files = list(year_folder.glob("*.atom"))
        print(f"{len(atom_files)} archivos encontrados")
        
        for file in atom_files:
            df = parse_atom_file(file)
            if not df.empty:
                all_dfs.append(df)
    
    if not all_dfs:
        print("No se encontraron datos en ninguna carpeta")
        return pd.DataFrame()
    
    df_combined = pd.concat(all_dfs, ignore_index=True)
    print(f"\nTotal combinado: {len(df_combined)} registros")
    
    return df_combined