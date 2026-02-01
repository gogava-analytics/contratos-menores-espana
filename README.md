# 📊 Proyecto ETL - Contratos Menores de España

## 🎯 ¿Qué hace este proyecto?

Este proyecto **descarga, procesa y analiza** datos de contratos públicos menores en España desde la [Plataforma de Contratación del Sector Público](https://contrataciondelestado.es).

Los datos se obtienen en formato XML (archivos `.atom`), se limpian, estructuran y almacenan en una base de datos MySQL para su análisis posterior.

---

## 📁 Estructura del Proyecto

```
proyecto_contratos_menores/
│
├── data/                           # Datos del proyecto
│   ├── raw/                        # Archivos .atom descargados (por año)
│   │   ├── 2020/
│   │   ├── 2021/
│   │   └── ...
│   ├── export/                     # Datasets para análisis
│   └── interim/                    # Datos intermedios (opcional)
│
├── sql/                            # Esquemas y consultas SQL
│   └── ddl.sql                     # Definición de tablas
│
├── src/                            # Código fuente
│   ├── atom_parser.py              # Parseo de archivos .atom
│   ├── loader.py                   # Carga de múltiples archivos
│   ├── config.py                   # Configuración y rutas
│   ├── main.py                     # Pipeline ETL principal
│   │
│   ├── db/                         # Módulos de base de datos
│   │   ├── engine.py               # Conexión MySQL
│   │   ├── schema.py               # Ejecución de DDL
│   │   ├── insert.py               # Inserción de datos
│   │   └── export_dataset.py       # Exportación para análisis
│   │
│   └── transform/                  # Transformaciones de datos
│       └── cleaning.py             # Limpieza del DataFrame
│
├── notebooks/                      # Análisis exploratorio (Jupyter)
├── .env                            # Credenciales de BD (no subir a Git)
├── .gitignore                      # Archivos ignorados por Git
└── README.md                       # Este archivo
```

---

## 🚀 Instalación y Configuración

### 1️⃣ Requisitos
- Python 3.8+
- MySQL 8.0+
- Conexión a internet (para descargar datos)

### 2️⃣ Instalar dependencias
```bash
pip install pandas sqlalchemy pymysql python-dotenv
```

### 3️⃣ Configurar base de datos
Crea un archivo `.env` en la raíz del proyecto:

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=contratos_menores_test
```

⚠️ **Importante**: Nunca subas el archivo `.env` a Git (ya está en `.gitignore`)

### 4️⃣ Descargar datos
Los archivos `.atom` deben descargarse manualmente desde:
- https://contrataciondelestado.es/sindicacion/sindicacion_643/contratosMenoresPerfilesContratantes.atom

Organízalos por año en `data/raw/`:
```
data/raw/
├── 2020/*.atom
├── 2021/*.atom
└── 2022/*.atom
```

---

## ▶️ Ejecución del Pipeline ETL

### Modo 1: Ejecución completa
```bash
python -m src.main
```

Esto ejecuta:
1. ✅ Crea el esquema de base de datos
2. 📄 Parsea todos los archivos `.atom`
3. 🧹 Limpia y normaliza los datos
4. 💾 Inserta en MySQL
5. ✅ Genera dataset analítico en `data/export/`

### Modo 2: Solo exportar dataset (después del ETL)
```python
from src.db.export_dataset import exportar_dataset
exportar_dataset()
```

---

## 🗄️ Modelo de Datos

### Tablas principales:

**`contrato`** (tabla central)
- Información de cada contrato: título, fechas, importes, estado

**`empresa`**
- Empresas ganadoras de contratos
- NIF, nombre, país, si es PYME

**`organo`**
- Órganos de contratación (ministerios, ayuntamientos, etc.)
- Código DIR3, nombre, actividad

**`tipo_contrato`** / **`tipo_organo`** / **`tipo_actividad_organo`**
- Tablas de catálogo (valores predefinidos)

### Relaciones:
```
contrato.contr_empresa_id  → empresa.empresa_id
contrato.contr_organo_id   → organo.organo_id
contrato.codigo_tipo_contrato → tipo_contrato.codigo_tipo_contrato
```

---

## 📊 Análisis de Datos

### Dataset exportado
Después de ejecutar el pipeline, encontrarás:
- `data/export/contratos_menores.parquet` (formato optimizado)
- `data/export/contratos_menores.csv` (compatible con Excel)

### Campos del dataset analítico:
| Campo | Descripción |
|-------|-------------|
| `titulo` | Título del contrato |
| `tipo_contrato` | Suministros / Servicios / Obras |
| `fecha_adjudicacion` | Fecha de adjudicación |
| `importe_total` | Importe total (€) |
| `empresa_nombre` | Empresa ganadora |
| `organo_nombre` | Órgano contratante |
| `actividad_organo` | Actividad del órgano (Sanidad, Educación...) |

### Ejemplo de uso en notebook:
```python
import pandas as pd

# Cargar dataset
df = pd.read_parquet('data/export/contratos_menores.parquet')

# Análisis básico
print(f"Total contratos: {len(df):,}")
print(f"Importe total: {df['importe_total'].sum():,.2f} €")

# Contratos por tipo
df['tipo_contrato'].value_counts()

# Top 10 empresas ganadoras
df['empresa_nombre'].value_counts().head(10)
```

---

## 🧹 Limpieza de Datos

El módulo `cleaning.py` realiza:
1. **Elimina columnas redundantes** (resúmenes, campos duplicados)
2. **Extrae ID numérico** del `id_entry`
3. **Elimina duplicados** (se queda con el registro más reciente)

Columnas eliminadas:
- `objeto_contrato` (redundante con `titulo`)
- `organo_contratacion_resumen` (incompleto)
- `importe_adjudicado_con_IVA` / `sin_IVA` (se usa `importe_total`)

---

## 🔧 Solución de Problemas

### Error: `FileNotFoundError: ddl.sql`
**Causa**: Falta el archivo SQL  
**Solución**: Verifica que `sql/ddl.sql` exista

### Error: `Access denied for user`
**Causa**: Credenciales incorrectas en `.env`  
**Solución**: Verifica usuario/contraseña de MySQL

### Error: `No module named 'src'`
**Causa**: Ejecutando desde carpeta incorrecta  
**Solución**: Ejecuta desde la raíz del proyecto:
```bash
python -m src.main  # ✅ Correcto
python src/main.py  # ❌ Incorrecto
```

### Advertencia: "contratos sin empresa_id"
**Causa**: Datos inconsistentes entre archivos .atom  
**Solución**: Normal en datos públicos, se filtran automáticamente

---

## 📈 Próximos Pasos (para tu análisis)

### EDA (Exploratory Data Analysis)
1. ✅ Cargar dataset exportado
2. 📊 Estadísticas descriptivas
3. 📉 Tendencias temporales (contratos por año/mes)
4. 🏢 Análisis de empresas (concentración, PYMES vs grandes)
5. 🗺️ Análisis geográfico (por región NUTS)
6. 💰 Análisis económico (distribución de importes)

### Visualizaciones sugeridas
- Evolución temporal de contratos
- Top 20 empresas ganadoras
- Distribución de importes (histograma)
- Contratos por tipo de actividad
- Mapa de calor por provincia

---

## 📝 Notas Técnicas

### Formato de los archivos .atom
Los archivos son feeds Atom (XML) con estructura:
```xml
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>...</id>
    <title>...</title>
    <ContractFolderStatus>
      <ProcurementProject>...</ProcurementProject>
      <TenderResult>...</TenderResult>
    </ContractFolderStatus>
  </entry>
</feed>
```

### Namespaces utilizados:
- `atom`: Feed estándar Atom
- `cbc` / `cac`: Esquema CODICE (contratación pública)

---

## 🤝 Contribuciones

Este es un proyecto personal de análisis de datos públicos.  
Si encuentras errores o mejoras, abre un issue o pull request.

---

## 📄 Licencia

Datos: Propiedad del Gobierno de España (datos públicos)  
Código: Uso libre

---

## 🔗 Enlaces Útiles

- [Plataforma de Contratación](https://contrataciondelestado.es)
- [Documentación CODICE](https://contrataciondelestado.es/wps/portal/!ut/p/b0/04_Sj9CPykssy0xPLMnMz0vMAfGjzOKNgo1NDLwMDDz9QgKc_VzdDBxdg0L8QxwCDPQLsh0VARhWOao!/)
- [Guía de datos abiertos](https://datos.gob.es)

---

**Última actualización**: Enero 2025  
**Autor**: [Tu nombre]