#!/usr/bin/env python3
"""
Debug script to understand skill matching
"""

import sys
sys.path.insert(0, '/reps/Scan-ATS/backend')

from app.services.skill_normalization import normalized_skills, skill_has_evidence

# Otilia's CV data - FULL with all three jobs
otilia_candidate = {
    "skills": [
        "Trabajo en equipo: desarrollo de capacidades individuales alineadas a objetivos estratégicos del área",
        "Liderazgo operativo: acompañamiento estratégico y ejecución con el ejemplo para el cumplimiento de procesos",
        "Toma de decisiones: análisis de escenarios orientado a la rentabilidad y beneficio empresarial",
        "Resolución de conflictos: gestión de soluciones inmediatas y efectivas ante incidencias operativas",
        "Adaptabilidad: capacidad de aprendizaje acelerado de normativas y agilidad ante nuevos retos laborales"
    ],
    "experience": [
        {
            "company": "PIXEL MOBILE S.A.",
            "position": "SUBGERENTE ADMINISTRATIVA",
            "dates": "NOVIEMBRE 2022 - A LA FECHA",
            "responsibilities": [
                "Administración de recursos humanos, materialesy financieros",
                "Optimización de Inventarios: implementación de procesos para el control y auditoría de existencias, generando reducción del 95% en errores operativos",
                "Gestión de Cartera: implementación de estrategias de cobros resultando en 88% de eficacia en la recuperación de cartera de más de 2 millones",
                "Ejecución de nómina mensual, provisiones y pagos de impuestos"
            ]
        },
        {
            "company": "AGENCIAS WAY S.A.",
            "position": "ASISTENTE - EJECUTIVA DE CAJA",
            "dates": "ENERO 2020 - NOVIEMBRE 2022",
            "responsibilities": [
                "Arqueo, cuadre y cierre de caja diario",
                "Depósitos y conciliaciones bancarias",
                "Facturación y control de cartera de clientes",
                "Gestión de cobranzas con 72% de recuperación de cartera",
                "Apoyo en procesos de nómina y afiliaciones",
                "Procesamiento de documentación para trámites legales"
            ]
        },
        {
            "company": "SALON DE BELLEZA Y SUMINISTROS X-PRESSION",
            "position": "ASISTENTE ADMINISTRATIVA",
            "dates": "ABRIL 2019 - ENERO 2020",
            "responsibilities": [
                "Atención al cliente",
                "Facturación y cobros",
                "Control de inventario",
                "Implementación de un sistema digital para control de citas"
            ]
        }
    ]
}

# Extract skills
skills = normalized_skills(otilia_candidate.get("skills", []))
print("Extracted Skills:")
for i, skill in enumerate(skills, 1):
    print(f"  {i}. {skill}")

# Get evidence text
def flatten(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    return ""

evidence_text = flatten(otilia_candidate.get("experience", []))
print("\nFull Evidence Text:")
print(f"  {evidence_text}\n")

# Check evidence for each skill
print("Skill Evidence Matching:")
matched = 0
for skill in skills:
    has_evidence = skill_has_evidence(skill, evidence_text)
    if has_evidence:
        matched += 1
    print(f"  {skill}: {'✓ YES' if has_evidence else '✗ NO'}")

print(f"\nTotal matched: {matched}/{len(skills)} = {matched/len(skills)*100:.0f}% evidence ratio")
