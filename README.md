# Análisis de Contratos Menores en España (2020-2025)

**Identificación de oportunidades de mercado para PYMEs mediante análisis de competencia geográfica**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características Principales](#características-principales)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Resultados y Análisis](#resultados-y-análisis)
- [Modelo de Datos](#modelo-de-datos)
- [Próximos Pasos](#próximos-pasos)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Licencia](#licencia)

---

## Descripción del Proyecto

Este proyecto analiza contratos menores del sector público español durante el periodo 2020-2025 con el objetivo de identificar oportunidades geográficas de baja competencia para empresas proveedoras, especialmente PYMEs.

### Contexto

Los contratos menores representan una vía estratégica de acceso al sector público debido a su menor complejidad administrativa y umbrales económicos reducidos (< 15.000€ para servicios y suministros, < 40.000€ para obras). Sin embargo, muchos mercados locales presentan alta concentración de proveedores, limitando la entrada de nuevos competidores.

### Objetivo Principal

Detectar provincias y localidades con baja competencia donde nuevas empresas pueden competir efectivamente mediante análisis cuantitativo del ratio contratos/empresa, identificación de mercados saturados versus oportunidades, y scoring multifactorial de viabilidad de negocio.

---

## Características Principales

### 1. Pipeline ETL Completo

- Parsing automatizado de feeds ATOM (XML) de la Plataforma de Contratación del Sector Público
- Limpieza y normalización de datos con manejo de inconsistencias
- Base de datos relacional MySQL con esquema normalizado (3FN)
- Exportación a formatos analíticos: Parquet (optimizado para análisis) y CSV

### 2. Análisis Exploratorio de Datos (EDA)

- Distribución temporal de contratos e importes adjudicados
- Análisis de principales organismos contratantes y empresas adjudicatarias
- Segmentación por tipo de contrato: obras, servicios, suministros
- Estadísticas descriptivas completas con identificación de outliers

### 3. Análisis de Competencia Geográfica

- **Métrica principal**: Ratio contratos/empresa por provincia como indicador de saturación del mercado
- Clasificación de competencia en cinco niveles: Muy Alta, Alta, Media, Baja, Muy Baja
- Mapa interactivo de España con visualización por nivel de competencia
- Análisis granular por código postal en provincias prioritarias

### 4. Sistema de Scoring de Oportunidad

Modelo de puntuación compuesto que considera:

- 50% - Nivel de competencia (ratio contratos/empresa invertido)
- 30% - Volumen de mercado (número absoluto de contratos)
- 20% - Valor medio por contrato

### 5. Insights Accionables

- Ranking de provincias con mayor potencial de oportunidad
- Análisis detallado por tipo de órgano contratante (administración local, autonómica, estatal)
- Identificación de códigos postales específicos con baja competencia
- Recomendaciones estratégicas basadas en datos para entrada en mercado

---

## Arquitectura del Proyecto

```
contratos-menores-espana/
│
├── data/
│   ├── raw/                      # Datos originales (feeds ATOM)
│   │   └── atom/
│   │       ├── 2020/
│   │       ├── 2021/
│   │       ├── 2022/
│   │       ├── 2023/
│   │       ├── 2024/
│   │       └── 2025/
│   │
│   ├── export/                   # Datasets procesados para análisis
│   │   ├── contratos_menores.parquet
│   │   ├── contratos_menores.csv
│   │   └── localidades.csv
│   │
│   └── interim/                  # Datos intermedios (opcional)
│
├── src/
│   ├── atom_parser.py           # Parser de archivos ATOM/XML
│   ├── loader.py                # Carga masiva de archivos
│   ├── config.py                # Configuración y constantes del proyecto
│   │
│   ├── transform/
│   │   └── cleaning.py          # Limpieza y normalización de datos
│   │
│   └── db/
│       ├── engine.py            # Gestión de conexión a MySQL
│       ├── schema.py            # Ejecución de DDL (Data Definition Language)
│       ├── insert.py            # Inserción de datos con integridad referencial
│       └── export_dataset.py    # Exportación a formatos analíticos
│
├── sql/
│   └── ddl.sql     # Definición del esquema de base de datos
|   |__ modelo.mwb             
│
├── notebooks/
│   └── storytelling_competencia.ipynb   # Análisis completo y visualizaciones
│
├── main.py                      # Orquestador del pipeline ETL
├── requirements.txt             # Dependencias del proyecto
├── .env.example                 # Template de variables de entorno
├── .gitignore
└── README.md
```

---

## Instalación

### Prerrequisitos

- Python 3.11 o superior
- MySQL 8.0 o superior
- Git

### Instrucciones

**1. Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/contratos-menores-espana.git
cd contratos-menores-espana
```

**2. Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar variables de entorno**

```bash
cp .env.example .env
```

Editar el archivo `.env` con las credenciales de MySQL:

```env
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=contratos_menores
```

**5. Obtener datos fuente** (opcional)

Los archivos ATOM pueden descargarse desde la [Plataforma de Contratación del Sector Público](https://contrataciondelestado.es).

---

## Uso

### Ejecución del Pipeline ETL

```bash
python main.py
```

Este comando ejecuta el flujo completo:

1. Creación automática de base de datos y tablas (si no existen)
2. Parsing de todos los archivos ATOM en `data/raw/atom/`
3. Limpieza y normalización de datos
4. Inserción en MySQL con validación de integridad referencial

### Exportación de Dataset Analítico

```bash
python -m src.db.export_dataset
```

Genera los archivos:
- `data/export/contratos_menores.parquet` (formato optimizado)
- `data/export/contratos_menores.csv` (formato compatible)

### Análisis con Jupyter Notebook

```bash
jupyter notebook notebooks/storytelling_competencia.ipynb
```

El notebook incluye:

- Análisis exploratorio de datos completo
- Visualizaciones estáticas (matplotlib, seaborn)
- Mapa interactivo de competencia por provincia (folium)
- Cálculo de scoring de oportunidad
- Generación de insights accionables

---

## Resultados y Análisis

### Métricas Generales (Periodo 2020-2025)

Las métricas específicas se actualizan tras la ejecución del análisis en el notebook.

- Total de contratos analizados
- Importe total adjudicado (€)
- Número de provincias con datos
- Empresas únicas identificadas
- Organismos contratantes únicos

### Principales Hallazgos

**Distribución de Competencia por Provincia**

La clasificación de provincias según nivel de competencia revela patrones geográficos significativos:

- Provincias con alta densidad empresarial: ratio < 5 contratos/empresa
- Provincias con oportunidad media: ratio 5-10 contratos/empresa
- Provincias con baja competencia: ratio > 10 contratos/empresa (objetivo prioritario)

**Patrones Identificados**

- Provincias pequeñas y medianas presentan menor competencia relativa
- Servicios especializados muestran mayor concentración de proveedores
- Administraciones locales (ayuntamientos) ofrecen mayor diversidad de contratos
- Estacionalidad observada con picos de actividad en Q4 (cierre presupuestario)

---

## Modelo de Datos

### Esquema Relacional

El modelo implementa tercera forma normal (3FN) para garantizar integridad y minimizar redundancia.

```
┌─────────────────────┐
│  tipo_contrato      │
├─────────────────────┤
│ codigo_tipo_contrato│ PK
│ nombre_contrato     │
└─────────────────────┘
         │
         │ 1:N
         │
┌────────▼─────────────────────┐
│       contrato               │
├──────────────────────────────┤
│ id_entry_num                 │ PK
│ id_entry                     │
│ titulo                       │
│ id_licitacion                │
│ fecha_actualizacion          │
│ fecha_adjudicacion           │
│ estado                       │
│ codigo_tipo_contrato         │ FK
│ codigo_subtipo_contrato      │
│ importe_estimado             │
│ importe_total                │
│ importe_sin_impuestos        │
│ codigo_cpv_principal         │
│ codigo_region_nuts           │
│ ofertas_recibidas            │
│ id_plataforma                │
│ contr_empresa_id             │ FK
│ contr_organo_id              │ FK
└──────────────────────────────┘
         │           │
         │ N:1       │ N:1
         │           │
    ┌────▼────┐  ┌──▼─────────────────┐
    │ empresa │  │      organo        │
    ├─────────┤  ├────────────────────┤
    │empresa_id│  │ organo_id          │ PK
    │nif_empresa│ │ organo_dir3        │
    │empresa_nombre│organo_nombre      │
    │empresa_es_pyme│organo_nif        │
    │empresa_pais│ │ organo_postalcode │
    └─────────┘  │ organo_localidad   │
                 │ organo_email       │
                 │ organo_telefono    │
                 │ tipo_organo_codigo │ FK
                 │ actividad_organo_codigo│ FK
                 └────────────────────┘
                      │           │
                      │ N:1       │ N:1
                      │           │
         ┌────────────▼─┐   ┌─────▼──────────────────┐
         │ tipo_organo  │   │ tipo_actividad_organo  │
         ├──────────────┤   ├────────────────────────┤
         │codigo_tipo_organo│PK │codigo_actividad_organo│PK
         │nombre_tipo_organo│   │nombre_actividad_organo│
         └──────────────┘   └────────────────────────┘
```

### Tablas Principales

**contrato**: Registro individual de cada contrato menor con información completa de licitación y adjudicación.

**empresa**: Catálogo de empresas adjudicatarias con identificación única por NIF.

**organo**: Organismos de contratación del sector público con geolocalización y datos de contacto.

**tipo_contrato**: Clasificación oficial de contratos (obras, servicios, suministros, etc.).

**tipo_organo**: Clasificación de órganos según naturaleza jurídica (administración estatal, autonómica, local, etc.).

**tipo_actividad_organo**: Clasificación por área funcional (educación, sanidad, infraestructuras, etc.).

---

## Próximos Pasos

### Desarrollo Inmediato

**Dashboard Interactivo en Power BI**

Se desarrollará un dashboard analítico con las siguientes características:

- KPIs dinámicos de competencia y volumen de mercado
- Visualización geográfica con drill-down por provincia y código postal
- Análisis temporal de tendencias y estacionalidad
- Filtros interactivos por tipo de contrato, organismo y periodo
- Sistema de alertas para detección de nuevas oportunidades

### Mejoras Futuras

**Análisis Sectorial**
- Clasificación detallada por código CPV (Common Procurement Vocabulary)
- Identificación de nichos de mercado especializados

**Modelado Predictivo**
- Predicción de adjudicaciones futuras mediante machine learning
- Análisis de probabilidad de éxito en licitaciones

**Automatización**
- Integración con API de PLACSP para actualización automática de datos
- Pipeline continuo de actualización (ETL incremental)

**Sistema de Recomendación**
- Motor de recomendación personalizado según perfil empresarial
- Análisis de compatibilidad empresa-oportunidad

---

## Tecnologías Utilizadas

### Core

- **Python 3.11+**: Lenguaje de programación principal
- **Pandas**: Manipulación y análisis de datos estructurados
- **NumPy**: Operaciones numéricas de alto rendimiento
- **MySQL**: Sistema de gestión de base de datos relacional

### Análisis y Visualización

- **Matplotlib**: Generación de gráficos estáticos
- **Seaborn**: Visualizaciones estadísticas avanzadas
- **Folium**: Mapas interactivos basados en Leaflet.js
- **Jupyter Notebook**: Entorno de análisis exploratorio

### Data Engineering

- **SQLAlchemy**: ORM y abstracción de base de datos
- **python-dotenv**: Gestión de variables de entorno
- **PyMySQL**: Driver de conexión MySQL
- **lxml / xml.etree**: Parsing de documentos XML/ATOM

### En Desarrollo

- **Power BI**: Dashboards interactivos y reportes ejecutivos

---

## Estructura de Archivos de Datos

### Fuentes de Datos

**Feeds ATOM**: Archivos XML con formato Atom Syndication Format (RFC 4287) que contienen información estructurada de contratos publicados en la Plataforma de Contratación del Sector Público.

**Localidades**: Base de datos geográfica con coordenadas (latitud, longitud) de municipios españoles para geolocalización de contratos.

### Datasets Generados

**contratos_menores.parquet**: Dataset analítico denormalizado en formato Apache Parquet, optimizado para consultas con Pandas y herramientas de análisis.

**contratos_menores.csv**: Mismos datos en formato CSV para compatibilidad con herramientas externas (Excel, Power BI, Tableau).

---

## Referencias

### Marco Legal

- Ley 9/2017, de 8 de noviembre, de Contratos del Sector Público (LCSP)
- Real Decreto Legislativo 3/2011 (Texto Refundido de la Ley de Contratos del Sector Público - derogado pero referencia histórica)

### Fuentes de Datos

- Plataforma de Contratación del Sector Público (PLACSP): https://contrataciondelestado.es
- Portal de datos abiertos de la Administración General del Estado: https://datos.gob.es

### Documentación Técnica

- Especificación feeds ATOM: https://contrataciondelestado.es/wps/portal/plataforma
- Common Procurement Vocabulary (CPV): https://simap.ted.europa.eu/web/simap/cpv

---

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulte el archivo `LICENSE` para más información.

---

## Autor

**[Tu Nombre]**

- GitHub: [gogava-analytics](https://github.com/gogava-analytics)
- LinkedIn: [giorgi gogava](https://www.linkedin.com/in/gogava-analytic/)
- Email: gogavaanalytics@gmail.com

---

## Agradecimientos

- Plataforma de Contratación del Sector Público por proporcionar datos abiertos
- Comunidad Python por el ecosistema de librerías de análisis de datos
- [Institución/Mentor] por el apoyo académico durante el desarrollo del proyecto

---

**Nota**: Este proyecto tiene fines educativos y de análisis. Los datos utilizados son públicos y se encuentran disponibles en las fuentes oficiales mencionadas.
