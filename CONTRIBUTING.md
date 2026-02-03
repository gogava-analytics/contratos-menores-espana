# Guía de Contribución

Esta guía establece las normas y procedimientos para contribuir al proyecto de análisis de contratos menores del sector público español.

---

## Tabla de Contenidos

- [Formas de Contribuir](#formas-de-contribuir)
- [Proceso de Contribución](#proceso-de-contribución)
- [Estándares de Código](#estándares-de-código)
- [Convenciones de Commits](#convenciones-de-commits)
- [Testing](#testing)
- [Áreas Prioritarias](#áreas-prioritarias)
- [Código de Conducta](#código-de-conducta)

---

## Formas de Contribuir

### Reporte de Errores

Antes de reportar un error, verifique que no exista un issue similar en el repositorio.

**Información requerida**:
- Descripción clara y concisa del problema
- Pasos exactos para reproducir el error
- Comportamiento esperado versus comportamiento observado
- Entorno de ejecución:
  - Sistema operativo y versión
  - Versión de Python
  - Versiones de dependencias relevantes
- Logs de error (si aplica)

### Propuestas de Mejora

Para sugerir nuevas funcionalidades o mejoras:

1. Abrir un issue con la etiqueta `enhancement`
2. Incluir:
   - Justificación técnica o científica de la propuesta
   - Descripción del problema que resuelve
   - Impacto esperado en el análisis o rendimiento
   - Propuesta de implementación (opcional)

### Contribuciones de Código

Las contribuciones de código son bienvenidas en las siguientes áreas:

- Mejoras de rendimiento del pipeline ETL
- Nuevos módulos de análisis estadístico
- Optimización de consultas SQL
- Documentación técnica
- Tests unitarios y de integración

---

## Proceso de Contribución

### 1. Preparación del Entorno

```bash
# Fork del repositorio en GitHub

# Clonar el fork localmente
git clone https://github.com/tu-usuario/contratos-menores-espana.git
cd contratos-menores-espana

# Configurar el repositorio upstream
git remote add upstream https://github.com/original-usuario/contratos-menores-espana.git

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Desarrollo

```bash
# Crear rama para la nueva funcionalidad
git checkout -b feature/nombre-descriptivo

# Realizar cambios siguiendo los estándares de código
# (ver sección siguiente)

# Verificar cambios
git status
git diff
```

### 3. Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest tests/

# Verificar estilo de código
flake8 src/

# Verificar tipos (si se usan type hints)
mypy src/
```

### 4. Commit y Push

```bash
# Añadir cambios
git add .

# Commit con mensaje descriptivo (ver convenciones)
git commit -m "Add: análisis de estacionalidad por trimestre"

# Push a fork
git push origin feature/nombre-descriptivo
```

### 5. Pull Request

1. Ir al repositorio original en GitHub
2. Crear Pull Request desde tu rama
3. Completar template del PR:
   - Descripción de los cambios
   - Motivación técnica
   - Tests realizados
   - Screenshots (si aplica)

### 6. Revisión y Merge

- El mantenedor revisará el código
- Se solicitarán cambios si es necesario
- Una vez aprobado, se realizará el merge

---

## Estándares de Código

### Python

**PEP 8**: Seguir la guía oficial de estilo de Python.

**Estructura de funciones**:

```python
def nombre_funcion(param1: tipo1, param2: tipo2) -> tipo_retorno:
    """
    Descripción breve de la función.
    
    Descripción detallada del comportamiento, casos especiales
    y consideraciones de rendimiento si aplica.
    
    Parameters
    ----------
    param1 : tipo1
        Descripción del parámetro 1
    param2 : tipo2
        Descripción del parámetro 2
        
    Returns
    -------
    tipo_retorno
        Descripción del valor de retorno
        
    Raises
    ------
    TipoExcepcion
        Condiciones bajo las cuales se lanza
        
    Examples
    --------
    >>> nombre_funcion(valor1, valor2)
    resultado_esperado
    
    Notes
    -----
    Consideraciones adicionales sobre complejidad,
    rendimiento o limitaciones.
    """
    # Implementación
    return resultado
```

**Type Hints**: Obligatorio para todas las funciones públicas.

```python
from typing import List, Dict, Optional, Tuple
import pandas as pd

def procesar_contratos(
    df: pd.DataFrame,
    columnas: List[str],
    umbral: Optional[float] = None
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Procesar DataFrame de contratos."""
    # Implementación
    return df_procesado, estadisticas
```

**Docstrings**: Formato NumPy/SciPy para consistencia con la comunidad científica de Python.

**Nombres**:
- Variables y funciones: `snake_case`
- Clases: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Variables privadas: `_nombre_privado`

### SQL

```sql
-- Comentarios descriptivos antes de cada consulta compleja

SELECT
    c.id_entry_num,
    c.fecha_adjudicacion,
    e.empresa_nombre,
    o.organo_nombre
FROM contrato AS c
INNER JOIN empresa AS e
    ON c.contr_empresa_id = e.empresa_id
INNER JOIN organo AS o
    ON c.contr_organo_id = o.organo_id
WHERE c.fecha_adjudicacion >= '2020-01-01'
ORDER BY c.fecha_adjudicacion DESC;
```

**Convenciones**:
- Keywords SQL en MAYÚSCULAS
- Nombres de tablas y columnas en minúsculas con guiones bajos
- Alias descriptivos
- Indentación clara para legibilidad

### Notebooks

- Cada celda debe tener un propósito claro
- Incluir celdas markdown con explicaciones antes de código complejo
- Reiniciar kernel y ejecutar todas las celdas antes de commit
- Limpiar outputs si el notebook es grande (usar nbstripout)

---

## Convenciones de Commits

### Formato

```
Tipo: Descripción breve (máximo 72 caracteres)

Descripción detallada opcional explicando el QUÉ y el POR QUÉ,
no el CÓMO (el código debe ser autoexplicativo).

Incluir referencias a issues si aplica: Refs #123
```

### Tipos de Commit

- **Add**: Nueva funcionalidad o archivo
- **Fix**: Corrección de bug
- **Update**: Actualización de funcionalidad existente
- **Refactor**: Mejora de código sin cambiar funcionalidad
- **Docs**: Cambios en documentación
- **Test**: Añadir o modificar tests
- **Perf**: Mejoras de rendimiento
- **Style**: Cambios de formato (espacios, comas, etc.)
- **Build**: Cambios en dependencias o configuración

### Ejemplos

```bash
Add: módulo de análisis de estacionalidad por trimestre

Implementa análisis estadístico de distribución temporal
de contratos con identificación de patrones estacionales.
Incluye tests unitarios y documentación.

Refs #45

---

Fix: error en parsing de fechas con timezone

Corrige AttributeError cuando la fecha incluye información
de zona horaria. Ahora normaliza a UTC antes de procesar.

Fixes #78

---

Refactor: optimización de consulta SQL en export_dataset

Reduce tiempo de ejecución de 45s a 12s mediante uso de
índices y eliminación de subconsultas innecesarias.
```

---

## Testing

### Filosofía

- Test-Driven Development (TDD) cuando sea posible
- Cobertura mínima objetivo: 80% para módulos core
- Tests deben ser determinísticos y reproducibles

### Estructura

```
tests/
├── unit/
│   ├── test_atom_parser.py
│   ├── test_cleaning.py
│   └── test_db_operations.py
├── integration/
│   └── test_etl_pipeline.py
└── fixtures/
    └── sample_data.xml
```

### Ejemplo de Test

```python
import pytest
import pandas as pd
from src.transform.cleaning import limpiar_contratos

class TestLimpiarContratos:
    """Tests para función de limpieza de contratos."""
    
    @pytest.fixture
    def df_sample(self):
        """Fixture con datos de ejemplo."""
        return pd.DataFrame({
            'id_entry': ['entry_001', 'entry_002'],
            'importe_sin_impuestos': [10000, 20000]
        })
    
    def test_elimina_duplicados(self, df_sample):
        """Verificar eliminación de registros duplicados."""
        df_duplicado = pd.concat([df_sample, df_sample])
        resultado = limpiar_contratos(df_duplicado)
        assert len(resultado) == len(df_sample)
    
    def test_preserva_columnas_esenciales(self, df_sample):
        """Verificar que no se eliminan columnas necesarias."""
        resultado = limpiar_contratos(df_sample)
        assert 'id_entry' in resultado.columns
        assert 'importe_sin_impuestos' in resultado.columns
```

---

## Áreas Prioritarias

### Alta Prioridad

1. **Testing**: Implementación de suite de tests completa
   - Tests unitarios para parsers y transformaciones
   - Tests de integración para pipeline ETL
   - Tests de regresión para análisis estadísticos

2. **Optimización de Rendimiento**
   - Parsing paralelo de archivos ATOM
   - Inserción batch en base de datos
   - Caching de consultas frecuentes

3. **Documentación**
   - Documentación técnica de API
   - Guía de arquitectura del sistema
   - Notebooks de ejemplo para casos de uso comunes

### Prioridad Media

1. **Análisis Sectorial**
   - Clasificación detallada por códigos CPV
   - Análisis de nichos de mercado especializados

2. **Validación de Datos**
   - Verificación de integridad referencial
   - Detección de anomalías en importes
   - Validación de formatos de NIF/CIF

3. **Logging y Monitoreo**
   - Sistema de logging estructurado
   - Métricas de rendimiento del pipeline
   - Alertas de errores críticos

### Prioridad Baja

1. **Interfaz Web**
   - Dashboard con Streamlit o Dash
   - API REST para consultas

2. **Machine Learning**
   - Predicción de adjudicaciones
   - Clustering de organismos por perfil de contratación

---

## Código de Conducta

### Principios

- **Profesionalismo**: Mantener comunicación respetuosa y constructiva
- **Colaboración**: Compartir conocimiento y ayudar a otros contribuidores
- **Calidad**: Priorizar código robusto, mantenible y bien documentado
- **Integridad**: Citar fuentes y dar crédito apropiadamente

### Comportamientos Esperados

- Crítica constructiva centrada en el código, no en las personas
- Apertura a diferentes perspectivas y soluciones
- Reconocimiento de contribuciones de otros
- Cumplimiento de estándares técnicos establecidos

### Comportamientos Inaceptables

- Comentarios ofensivos o discriminatorios
- Acoso de cualquier tipo
- Publicación de información privada de terceros
- Conducta no profesional o disruptiva

---

## Recursos Adicionales

### Documentación

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [NumPy Docstring Standard](https://numpydoc.readthedocs.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)

### Contacto

Para preguntas sobre contribuciones:

- Abrir un issue con la etiqueta `question`
- Contactar al mantenedor: tu.email@ejemplo.com

---

Última actualización: Febrero 2025
