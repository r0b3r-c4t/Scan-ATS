#!/usr/bin/env python3
"""
Test the candidate evaluation service with Otilia's real CV data.
This simulates what the AI service would extract.
"""

import sys
sys.path.insert(0, '/reps/Scan-ATS/backend')

from app.services.candidate_evaluation_service import evaluate_candidate

# Otilia's CV data as extracted by AIService
otilia_candidate = {
    "name": "OTILIA PAAU",
    "email": "otiliaapaual@gmail.com",
    "phone": "5536-0713 / 5908-8874",
    "location": "Zona 4 de Mexico, Guatemala",
    "summary": "Licenciada en Administración de Empresas con experiencia en gestión administrativa, financiera y de talento humano. Profesional proactiva con habilidades en liderazgo, toma de decisiones y resolución de conflictos.",
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
    ],
    "education": [
        {
            "institution": "Universidad Rafael Landivar",
            "degree": "Licenciatura en Administración de Empresas | Magna Cum Laude",
            "dates": "2013 - 2018",
            "campus": "Campus la Verapaz"
        },
        {
            "institution": "Universidad del Valle de Guatemala",
            "degree": "Técnico Universitario en Turismo | Suma Cum Laude",
            "dates": "2010 - 2011",
            "campus": "Campus El Altiplano"
        }
    ],
    "certifications": [],
    "projects": []
}

print("\n" + "="*60)
print("TESTING CANDIDATE EVALUATION WITH OTILIA'S REAL CV")
print("="*60 + "\n")

try:
    result = evaluate_candidate(otilia_candidate)
    
    print("\n" + "="*60)
    print("EVALUATION RESULT")
    print("="*60)
    print(f"\nFinal Score: {result['score']}/100")
    print(f"Classification: {result['classification']}")
    
    print("\n--- Component Breakdown ---")
    for component, score in result['components'].items():
        print(f"{component:20s}: {score:3d}/100")
    
    print("\n--- Strengths ---")
    for strength in result['strengths']:
        print(f"  ✓ {strength}")
    
    print("\n--- Areas to Improve ---")
    for area in result['areas_to_improve']:
        print(f"  • {area}")
    
    if result['warnings']:
        print("\n--- Warnings ---")
        for warning in result['warnings']:
            print(f"  ⚠ {warning}")
    
    print("\n" + "="*60)
    
    # Validation checks
    print("\nVALIDATION CHECKS:")
    print("-" * 60)
    
    checks = [
        ("Final score > 0", result['score'] > 0),
        ("Final score <= 100", result['score'] <= 100),
        ("Experience score > 0", result['components']['experience'] > 0),
        ("Education score > 0", result['components']['education'] > 0),
        ("CV Quality score > 70", result['components']['cv_quality'] > 70),
        ("Achievements score > 0", result['components']['achievements'] > 0),
        ("Final score >= 70 (Expected: Good Candidate)", result['score'] >= 70),
        ("Classification is not 'Poor'", "Poor" not in result['classification']),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL CHECKS PASSED!")
    else:
        print("✗ SOME CHECKS FAILED - REVIEW ABOVE")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
