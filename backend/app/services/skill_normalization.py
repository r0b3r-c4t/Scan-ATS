import re
from typing import Any


SKILL_ALIASES = {
    "node": "node.js", "nodejs": "node.js", "node.js": "node.js",
    "dotnet": ".net", ".net": ".net", ".net 8": ".net",
    "csharp": "c#", "c-sharp": "c#", "c#": "c#",
    "postgres": "postgresql", "postgresql": "postgresql",
    "mongo": "mongodb", "mongo db": "mongodb", "mongodb": "mongodb",
}

# Map soft skills to keywords that appear in CVs
SOFT_SKILL_KEYWORDS = {
    "trabajo en equipo": [
        "equipo", "teamwork", "team", "colaboración", "collaborative", "collectively",
        "trabajar juntos", "desarrollo de capacidades"
    ],
    "liderazgo": [
        "liderazgo", "leadership", "líder", "leader", "lideré", "led", "conducción",
        "guía", "dirección", "acompañamiento"
    ],
    "liderazgo operativo": [
        "liderazgo", "operativo", "operations", "operacionales", "acompañamiento",
        "ejecución", "cumplimiento", "procesos"
    ],
    "toma de decisiones": [
        "decisiones", "decision", "análisis de escenarios", "escenarios", "rentabilidad",
        "beneficio empresarial", "criterio", "análisis", "evaluar", "evaluación",
        "evaluando", "evalúa"
    ],
    "resolución de conflictos": [
        "conflictos", "conflict", "resolving", "soluciones", "incidencias", 
        "gestión", "efectivas", "inmediatas"
    ],
    "adaptabilidad": [
        "adaptabilidad", "adaptable", "adaptación", "learning", "aprendizaje",
        "retos laborales", "normativas", "agilidad", "capacidad de aprendizaje",
        "nuevos retos", "acelerado"
    ],
    "comunicación": [
        "comunicación", "comunicar", "communication", "communicate", "información"
    ],
    "gestión": [
        "gestión", "management", "manage", "managed", "gestionar", "administración"
    ],
    "administración": [
        "administración", "administration", "administrative", "administrar", "gestión"
    ],
    "coordinación": [
        "coordinación", "coordination", "coordinador", "coordinar", "articulación"
    ],
    "supervisión": [
        "supervisión", "supervision", "supervisor", "supervise", "supervisar", 
        "vigilancia", "control", "monitoreo"
    ],
    "negociación": [
        "negociación", "negotiation", "negotiate", "negociar", "acuerdos"
    ],
    "análisis": [
        "análisis", "analysis", "analyze", "analytical", "analítico", "escenarios",
        "evaluación", "evaluando"
    ],
    "planificación": [
        "planificación", "planning", "plan", "planned", "planificación", "estrategia",
        "estratégicos", "objetivos"
    ],
    "gestión de talento humano": [
        "talento humano", "rrhh", "recursos humanos", "personal", "empleados",
        "nómina", "afiliaciones", "evaluación de desempeño", "reclutamiento", "selección"
    ],
    "gestión financiera": [
        "financiero", "financial", "cartera", "cobros", "cobranzas", "caja",
        "depósitos", "conciliaciones", "nómina", "impuestos", "facturación", "pagos"
    ],
    "gestión de inventarios": [
        "inventario", "inventory", "inventarios", "existencias", "control", "auditoría"
    ],
}


def normalize_skill(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value.strip().lower())
    return SKILL_ALIASES.get(normalized, normalized)


def extract_skill_keywords(skill_str: str) -> set[str]:
    """
    Extract meaningful keywords from a skill string.
    For "Trabajo en equipo: desarrollo de capacidades...", returns ["trabajo", "equipo", "desarrollo", "capacidades"]
    """
    # Remove colon and take everything
    text = skill_str.split(":", 1)[-1] if ":" in skill_str else skill_str
    
    # Extract words (remove very short words like "de", "y", "en")
    words = set()
    for word in re.findall(r'\b\w+\b', text.lower()):
        if len(word) >= 3:  # Only words with 3+ characters
            words.add(word)
    
    return words


def normalized_skills(values: Any) -> set[str]:
    """
    Extract and normalize skills from a list.
    Supports both string and dict formats.
    """
    result: set[str] = set()
    for value in values if isinstance(values, list) else []:
        if isinstance(value, dict):
            # Try multiple field names
            value = value.get("name") or value.get("skill") or value.get("technology")
        
        if not isinstance(value, str):
            continue
        
        # Normalize and add the full skill
        text = value.split(":", 1)[-1]
        skill = normalize_skill(value)
        if skill:
            result.add(skill)
    
    return result


def skill_has_evidence(skill_str: str, evidence_text: str) -> bool:
    """
    Check if a skill has evidence in the evidence text.
    For skills with format "Skill Name: description", extracts the name part
    and matches against keywords and text.
    """
    # Extract just the skill name (before colon if present)
    if ":" in skill_str:
        skill_name = skill_str.split(":", 1)[0].strip()
    else:
        skill_name = skill_str.strip()
    
    skill_lower = skill_name.lower()
    evidence_lower = evidence_text.lower()
    
    # Check 1: Exact substring match of skill name
    if skill_lower in evidence_lower:
        return True
    
    # Check 2: Check if it's a known soft skill with predefined keywords
    if skill_lower in SOFT_SKILL_KEYWORDS:
        keywords = SOFT_SKILL_KEYWORDS[skill_lower]
        if any(keyword in evidence_lower for keyword in keywords):
            return True
    
    # Check 3: Extract keywords from skill name and check if they appear in evidence
    skill_keywords = extract_skill_keywords(skill_name)
    if len(skill_keywords) > 0:
        found_keywords = {kw for kw in skill_keywords if kw in evidence_lower}
        # If we find at least 50% of keywords, consider it evidence
        if found_keywords and len(found_keywords) >= len(skill_keywords) * 0.5:
            return True
    
    # Check 4: Also extract keywords from the description part if present
    if ":" in skill_str:
        description = skill_str.split(":", 1)[1].strip()
        description_keywords = extract_skill_keywords(description)
        if description_keywords:
            found_keywords = {kw for kw in description_keywords if kw in evidence_lower}
            # If we find any keywords from description, it counts
            if found_keywords:
                return True
    
    # Check 5: Common technical skill patterns
    if re.search(rf"(?<!\w){re.escape(skill_name)}(?!\w)", evidence_lower, re.I):
        return True
    
    return False
