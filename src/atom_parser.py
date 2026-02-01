"""
Parser de archivos .atom de la Plataforma de Contratación del Sector Público.

Responsabilidad:
- Leer archivos .atom (XML)
- Extraer la información relevante de cada <entry>
- Devolver los datos en forma de pandas.DataFrame

Este módulo NO:
- limpia datos
- deduplica
- guarda en base de datos
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
import re

import pandas as pd

from src.config import (
    XML_NAMESPACES,
    MAPA_TIPO_CONTRATO,
    MAPA_TIPO_ORGANO,
    MAPA_ACTIVIDAD_ORGANO,
)


# ======================================================
# FUNCIONES AUXILIARES
# ======================================================

def safe_float(value):
    """
    Convierte un valor numérico representado como texto en float.

    - Elimina símbolos no numéricos (€, espacios, etc.)
    - Devuelve None si el valor no es convertible

    NOTA:
    - No soporta coma como separador decimal.
    """
    if value is None or value == "":
        return None

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    s = re.sub(r"[^\d.\-]", "", s)

    if s in ("", "-", "."):
        return None

    if s.count(".") > 1:
        return None

    try:
        return float(s)
    except ValueError:
        return None


def get_text(element, path, default=None):
    """
    Extrae texto de un elemento XML usando un path con namespaces.

    Devuelve `default` si:
    - el elemento no existe
    - el nodo no existe
    - el texto está vacío
    """
    if element is None:
        return default

    node = element.find(path, XML_NAMESPACES)
    if node is None or node.text is None:
        return default

    return node.text.strip()


# ======================================================
# PARSEO DE UN ENTRY
# ======================================================

def parse_entry(entry):
    """
    Parsea un elemento <entry> de un feed Atom y devuelve un diccionario
    con los campos extraídos.
    """
    data = defaultdict(lambda: None)

    try:
        # ----------------------------------------------
        # Identificadores básicos del entry
        # ----------------------------------------------
        data["id_entry"] = get_text(entry, "atom:id")
        data["titulo"] = get_text(entry, "atom:title")
        data["fecha_actualizacion"] = pd.to_datetime(
            get_text(entry, "atom:updated"),
            errors="coerce"
        )

        # ----------------------------------------------
        # Información embebida en <atom:summary>
        # ----------------------------------------------
        summary_text = get_text(entry, "atom:summary") or ""

        id_match = re.search(
            r"(?i)Id\s*licitaci[oó]n:\s*([^;]+)",
            summary_text
        )
        organo_match = re.search(
            r"(?i)[ÓO]rgano\s*de\s*Contrataci[oó]n:\s*([^;]+)",
            summary_text
        )
        importe_match = re.search(
            r"(?i)Importe:\s*([-\d\.,\s€]+)",
            summary_text
        )
        estado_match = re.search(
            r"(?i)Estado:\s*([^;]+)",
            summary_text
        )

        data["id_licitacion"] = (
            id_match.group(1).strip() if id_match else None
        )
        data["organo_contratacion_resumen"] = (
            organo_match.group(1).strip() if organo_match else None
        )
        data["importe_resumen"] = (
            safe_float(importe_match.group(1)) if importe_match else None
        )
        data["estado_resumen"] = (
            estado_match.group(1).strip() if estado_match else None
        )

        # ----------------------------------------------
        # ContractFolderStatus
        # ----------------------------------------------
        cfs = entry.find(
            "cac_place_ext:ContractFolderStatus",
            XML_NAMESPACES
        )

        if cfs is not None:
            data["id_expediente"] = get_text(
                cfs, "cbc:ContractFolderID"
            )
            data["estado"] = get_text(
                cfs, "cbc_place_ext:ContractFolderStatusCode"
            )

            # ------------------------------------------
            # Órgano de contratación
            # ------------------------------------------
            lcp = cfs.find(
                "cac_place_ext:LocatedContractingParty",
                XML_NAMESPACES
            )

            if lcp is not None:
                tipo_codigo = get_text(
                    lcp, "cbc:ContractingPartyTypeCode"
                )
                data["tipo_organo_codigo"] = tipo_codigo
                data["tipo_organo_nombre"] = (
                    MAPA_TIPO_ORGANO.get(tipo_codigo)
                )

                actividad_codigo = get_text(
                    lcp, "cbc:ActivityCode"
                )
                data["actividad_organo_codigo"] = actividad_codigo
                data["actividad_organo_nombre"] = (
                    MAPA_ACTIVIDAD_ORGANO.get(actividad_codigo)
                )

                party = lcp.find("cac:Party", XML_NAMESPACES)

                if party is not None:
                    for pid in party.findall(
                        "cac:PartyIdentification",
                        XML_NAMESPACES
                    ):
                        id_elem = pid.find("cbc:ID", XML_NAMESPACES)
                        if id_elem is not None:
                            scheme = (
                                id_elem.get("schemeName")
                                or id_elem.get("schemeID")
                            )
                            value = (
                                id_elem.text.strip()
                                if id_elem.text else None
                            )

                            if scheme == "DIR3":
                                data["id_dir3"] = value
                            elif scheme == "NIF":
                                data["nif_organo"] = value
                            elif scheme == "ID_PLATAFORMA":
                                data["id_plataforma"] = value

                    data["nombre_organo"] = get_text(
                        party, "cac:PartyName/cbc:Name"
                    )
                    data["codigo_postal_organo"] = get_text(
                        party, "cac:PostalAddress/cbc:PostalZone"
                    )
                    data["localidad_organo"] = get_text(
                        party, "cac:PostalAddress/cbc:CityName"
                    )
                    data["pais_organo"] = get_text(
                        party, "cac:PostalAddress/cac:Country/cbc:Name"
                    )
                    data["email_organo"] = get_text(
                        party, "cac:Contact/cbc:ElectronicMail"
                    )
                    data["telefono_organo"] = get_text(
                        party, "cac:Contact/cbc:Telephone"
                    )

            # ------------------------------------------
            # Proyecto de contratación
            # ------------------------------------------
            pp = cfs.find(
                "cac:ProcurementProject",
                XML_NAMESPACES
            )

            if pp is not None:
                data["objeto_contrato"] = get_text(pp, "cbc:Name")

                tipo_code = get_text(pp, "cbc:TypeCode")
                data["codigo_tipo_contrato"] = tipo_code
                data["nombre_tipo_contrato"] = (
                    MAPA_TIPO_CONTRATO.get(tipo_code)
                )

                data["codigo_subtipo_contrato"] = get_text(
                    pp, "cbc:SubTypeCode"
                )

                ba = pp.find(
                    "cac:BudgetAmount",
                    XML_NAMESPACES
                )
                if ba is not None:
                    data["importe_estimado"] = safe_float(
                        get_text(
                            ba,
                            "cbc:EstimatedOverallContractAmount"
                        )
                    )
                    data["importe_total"] = safe_float(
                        get_text(ba, "cbc:TotalAmount")
                    )
                    data["importe_sin_impuestos"] = safe_float(
                        get_text(
                            ba,
                            "cbc:TaxExclusiveAmount"
                        )
                    )

                data["codigo_cpv_principal"] = get_text(
                    pp,
                    "cac:RequiredCommodityClassification/"
                    "cbc:ItemClassificationCode"
                )
                data["codigo_region_nuts"] = get_text(
                    pp,
                    "cac:RealizedLocation/"
                    "cbc:CountrySubentityCode"
                )

                duracion = pp.find(
                    "cac:PlannedPeriod/"
                    "cbc:ContractDurationMeasure",
                    XML_NAMESPACES
                )
                if duracion is not None:
                    data["duracion_contrato_valor"] = duracion.text
                    data["duracion_contrato_unidad"] = (
                        duracion.get("unitCode")
                    )

            # ------------------------------------------
            # Resultado de la licitación
            # ------------------------------------------
            trs = cfs.find(
                "cac:TenderResult",
                XML_NAMESPACES
            )

            if trs is not None:
                data["fecha_adjudicacion"] = pd.to_datetime(
                    get_text(trs, "cbc:AwardDate"),
                    errors="coerce"
                )
                data["ofertas_recibidas"] = get_text(
                    trs, "cbc:ReceivedTenderQuantity"
                )
                data["es_pyme_empresa"] = get_text(
                    trs, "cbc:SMEAwardedIndicator"
                )

                wp = trs.find(
                    "cac:WinningParty",
                    XML_NAMESPACES
                )
                if wp is not None:
                    data["nif_empresa"] = get_text(
                        wp, "cac:PartyIdentification/cbc:ID"
                    )
                    data["empresa_ganadora"] = get_text(
                        wp, "cac:PartyName/cbc:Name"
                    )
                    data["pais_empresa"] = get_text(
                        wp,
                        "cac:PhysicalLocation/"
                        "cac:Address/cac:Country/"
                        "cbc:IdentificationCode"
                    )

                data["importe_adjudicado_con_IVA"] = safe_float(
                    get_text(
                        trs,
                        "cac:AwardedTenderedProject/"
                        "cac:LegalMonetaryTotal/"
                        "cbc:PayableAmount"
                    )
                )
                data["importe_adjudicado_sin_IVA"] = safe_float(
                    get_text(
                        trs,
                        "cac:AwardedTenderedProject/"
                        "cac:LegalMonetaryTotal/"
                        "cbc:TaxExclusiveAmount"
                    )
                )

    except Exception as e:
        data["parse_error"] = str(e)

    return data


# ======================================================
# PARSEO DE ARCHIVOS .ATOM
# ======================================================

def parse_atom_file(path: Path) -> pd.DataFrame:
    """
    Parsea un archivo .atom y devuelve un DataFrame con todos los entries.
    """
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        entries = root.findall(
            ".//atom:entry",
            XML_NAMESPACES
        )
        if not entries:
            entries = root.findall(".//entry")

        records = [parse_entry(entry) for entry in entries]
        return pd.DataFrame(records)

    except ET.ParseError as e:
        print(f"Error de parseo XML en {path.name}: {e}")
        return pd.DataFrame()

    except Exception as e:
        print(f"Error procesando {path.name}: {e}")
        return pd.DataFrame()
