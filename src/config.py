from pathlib import Path

# =============================
# RUTAS BASE
# =============================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

SQL_DIR = BASE_DIR / "sql"

# =============================
# ARCHIVOS
# =============================

DDL_PATH = SQL_DIR / "ddl.sql"

# =============================
# XML NAMESPACES
# =============================

XML_NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "cbc": "urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2",
    "cac_place_ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2",
    "cbc_place_ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2",
}

# =============================
# MAPAS DE CÓDIGOS
# =============================

# Mapa de códigos oficiales de tipo de contrato a descripciones legibles.
MAPA_TIPO_CONTRATO = {
    "1": "Suministros",
    "2": "Servicios",
    "3": "Obras",
    "21": "Gestión de Servicios Públicos",
    "22": "Concesión de Servicios",
    "31": "Concesión de Obras Públicas",
    "32": "Concesión de Obras",
    "40": "Colaboración entre el sector público y sector privado",
    "7": "Administrativo especial",
    "8": "Privado",
    "50": "Patrimonial"
}

# Mapa de códigos oficiales de tipo de órgano a descripciones legibles.
MAPA_TIPO_ORGANO = {
    "1": "Autoridad estatal",
    "2": "Autoridad regional",
    "3": "Autoridad local",
    "4": "Organismo de Derecho público",
    "5": "Otras Entidades del Sector Público",
    "6": "Organismo de Derecho público bajo el control de una autoridad estatal",
    "7": "Organismo de Derecho público bajo el control de una autoridad regional",
    "8": "Organismo de Derecho público bajo el control de una autoridad local",
    "9": "Empresa pública bajo el control de una autoridad estatal",
    "10": "Empresa pública bajo el control de una autoridad regional",
    "11": "Empresa pública bajo el control de una autoridad local",
    "12": "Entidad con derechos especiales o exclusivos"
}

# Mapa de códigos oficiales de actividad del órgano a descripciones legibles.
MAPA_ACTIVIDAD_ORGANO = {
    '1': 'Justicia',
    '2': 'Defensa',
    '3': 'Seguridad Ciudadana e Instituciones Penitenciarias',
    '4': 'Política Exterior',
    '5': 'Pensiones',
    '6': 'Otras Prestaciones Económicas',
    '7': 'Servicios Sociales y Promoción Social',
    '8': 'Fomento del Empleo',
    '9': 'Desempleo',
    '10': 'Acceso a la Vivienda y Fomento de la Edificación',
    '11': 'Gestión y Administración de la Seguridad Social',
    '12': 'Sanidad',
    '13': 'Educación',
    '14': 'Cultura',
    '15': 'Agricultura, Pesca y Alimentación',
    '16': 'Industria y Energía',
    '17': 'Comercio, Turismo y Pymes',
    '18': 'Subvenciones al Transporte',
    '19': 'Infraestructuras',
    '20': 'Investigación, Desarrollo e Innovación',
    '21': 'Otras Actuaciones de Carácter Económico',
    '22': 'Servicios de Carácter General',
    '23': 'Administración Financiera y Tributaria',
    '24': 'Transferencias a otras Administraciones Públicas',
    '25': 'Deuda Pública',
    '26': 'Medio Ambiente',
    '27': 'Interior',
    '28': 'Economía y Hacienda',
    '29': 'Ocio',
    '101': 'Actividades relacionadas con Aeropuerto',
    '102': 'Electricidad',
    '103': 'Exploración y extracción de carbón u otro combustible solido',
    '104': 'Exploración y extracción de Gas',
    '105': 'Actividades relacionadas con Puertos',
    '106': 'Servicios Postales',
    '107': 'Distribución de Gas',
    '108': 'Servicios Ferroviarios',
    '109': 'Servicios de tranvía, metro y autobus',
    '110': 'Agua'
}