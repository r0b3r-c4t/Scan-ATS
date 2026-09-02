# 🚀 Scan-ATS

**Scan-ATS** es un sistema de seguimiento de candidatos (Applicant Tracking System) potenciado por IA, diseñado para automatizar el análisis de CV y la evaluación de candidatos. El sistema utiliza visión por computadora y procesamiento de lenguaje natural para extraer información y calcular puntuaciones de candidatos de forma determinística.

---

## 📋 Tabla de Contenidos

- [Características Principales](#características-principales)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Cómo Ejecutar](#cómo-ejecutar)
- [Flujo de Datos](#flujo-de-datos)
- [API Endpoints](#api-endpoints)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🎯 Características Principales

### 1. **Análisis Inteligente de CV**
- Extracción automática de información de CV (PDF/JPG)
- Análisis con IA usando Ollama (LLM local)
- Soporte para múltiples idiomas (español, inglés, etc.)
- Extrae: nombre, email, skills, experiencia, educación, proyectos, certificaciones

### 2. **Evaluación Determinística de Candidatos**
- Sistema de puntuación basado en 8 componentes:
  - Experiencia (25%)
  - Skills Técnicos (20%)
  - Proyectos (15%)
  - Educación (10%)
  - Logros (10%)
  - Certificaciones (10%)
  - Calidad del CV (5%)
  - Consistencia (5%)
- Scoring reproducible (mismo CV = mismo score)
- Clasificación: Pobre < Débil < Moderado < Fuerte < Excelente

### 3. **Gestión de Candidatos**
- Almacenamiento en MongoDB con GridFS
- Búsqueda y filtrado por puntuación
- Visualización de perfiles detallados
- Descarga/visualización de CV original

### 4. **Gestión de Puestos de Trabajo**
- Crear y gestionar ofertas de empleo
- Listar puestos disponibles
- Metadata de puestos (descripción, requisitos, etc.)

### 5. **Matching Inteligente**
- Emparejar candidatos con puestos
- Análisis de compatibilidad
- Scores de coincidencia

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React + Vite)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Upload Resume                                          │  │
│  │ • Candidate List & Detail                               │  │
│  │ • Job Management                                        │  │
│  │ • Matching & Scores                                     │  │
│  │ • Dashboard                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND API (FastAPI + Python)                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routes:                                                 │  │
│  │  • /api/candidates (upload, list, detail)               │  │
│  │  • /api/candidates/{id}/resume (download CV)            │  │
│  │  • /api/jobs (CRUD operations)                          │  │
│  │  • /api/matches (candidate-job matching)                │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Services:                                               │  │
│  │  • AIService (LLM integration)                           │  │
│  │  • DocumentService (PDF/Image processing)               │  │
│  │  • CandidateEvaluationService (Scoring logic)            │  │
│  │  • CandidateService (Data management)                    │  │
│  │  • FileService (GridFS operations)                       │  │
│  │  • SkillNormalization (Skill matching)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          ↓ PyMuPDF                    ↓ Ollama              ↓ MongoDB
    ┌──────────────┐            ┌───────────────┐     ┌──────────────┐
    │ PDF/Image    │            │  LLM Local    │     │  Database    │
    │ Processing   │            │  (Ollama)     │     │  + GridFS    │
    └──────────────┘            └───────────────┘     └──────────────┘
```

---

## 📦 Stack Tecnológico

### **Backend**
| Tecnología | Versión | Propósito |
|---|---|---|
| **FastAPI** | 0.141.1 | Framework web moderno y rápido |
| **Python** | 3.9+ | Lenguaje principal |
| **PyMongo** | 4.17.0 | Driver MongoDB |
| **PyMuPDF** | 1.28.2 | Extracción de páginas de PDF/imagenes |
| **Ollama** | 0.6.2 | Integración con LLM local |
| **Uvicorn** | 0.52.4 | Servidor ASGI |
| **Pydantic** | 2.13.5 | Validación de datos |
| **python-dotenv** | 1.2.3 | Gestión de variables de entorno |

### **Frontend**
| Tecnología | Versión | Propósito |
|---|---|---|
| **React** | 18.3.1 | UI Framework |
| **Vite** | 5.4.0 | Build tool y dev server |
| **React Router** | 6.26.0 | Enrutamiento |
| **Axios** | 1.7.7 | HTTP client |
| **CSS3** | - | Estilos |

### **Infraestructura**
| Servicio | Propósito |
|---|---|
| **MongoDB** | Base de datos NoSQL |
| **GridFS** | Almacenamiento de archivos binarios |
| **Ollama** | Servidor LLM local |
| **Qwen3-Vision:4b** | Modelo IA para análisis de CV (vision + language) |
| **Docker** | Containerización |

---

## 🤖 Configuración de Ollama y Modelos

### **Modelos Disponibles**

| Modelo | Tamaño | Tipo | Descripción |
|--------|--------|------|-------------|
| **scan-ats-qwen3-vl-instruct:4b** | 3.3 GB | Vision + Language | ⭐ Recomendado - Optimizado para Scan-ATS |
| **qwen3-vl:4b** | 3.3 GB | Vision + Language | Modelo base original |

### **Instalación de Ollama**

1. **Descargar e instalar** desde [ollama.ai](https://ollama.ai)
2. **Ejecutar el servidor**:
   ```bash
   ollama serve
   ```
3. **En otra terminal, instalar modelo**:
   ```bash
   # Recomendado (variante optimizada)
   ollama pull scan-ats-qwen3-vl-instruct:4b
   
   # O modelo base
   ollama pull qwen3-vl:4b
   ```
4. **Verificar instalación**:
   ```bash
   ollama list
   ```

### **Rendimiento**

- **GPU NVIDIA**: ~5-10 segundos por análisis de CV
- **GPU AMD**: ~8-15 segundos por análisis de CV
- **CPU Only**: 1-3 minutos por análisis de CV (no recomendado)

**Recomendación**: Usar GPU para mejor performance

---



```
Scan-ATS/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Entry point FastAPI
│   │   ├── config/
│   │   │   ├── settings.py            # Configuración (DB, Ollama, etc)
│   │   ├── database/
│   │   │   └── mongodb.py             # Conexión MongoDB + GridFS
│   │   ├── models/
│   │   │   └── candidate.py           # Modelos de datos
│   │   ├── routes/
│   │   │   ├── candidates.py          # Endpoints de candidatos
│   │   │   └── jobs.py                # Endpoints de trabajos
│   │   ├── schemas/
│   │   │   ├── candidate_schema.py    # Validación de candidatos
│   │   │   ├── job_schema.py          # Validación de trabajos
│   │   │   └── matching_schema.py     # Validación de matching
│   │   ├── services/
│   │   │   ├── ai_service.py          # Integración Ollama
│   │   │   ├── candidate_evaluation_service.py  # Lógica de scoring
│   │   │   ├── candidate_service.py   # Gestión de candidatos
│   │   │   ├── document_service.py    # Procesamiento de documentos
│   │   │   ├── file_service.py        # Gestión de archivos
│   │   │   ├── matching_service.py    # Lógica de matching
│   │   │   └── skill_normalization.py # Normalización de skills
│   ├── requirements.txt               # Dependencias Python
│   ├── docker-compose.yml             # Setup Docker local
│   ├── Modelfile                      # Configuración Ollama
│   ├── test_evaluation_otilia.py      # Tests de evaluación
│   └── debug_skills.py                # Debug de skills
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Componente raíz
│   │   ├── main.jsx                   # Entry point
│   │   ├── components/
│   │   │   ├── Layout.jsx             # Layout wrapper
│   │   │   ├── ScoreRing.jsx          # Visualización de score
│   │   │   ├── ScoreBreakdown.jsx     # Desglose de componentes
│   │   │   ├── SkillBadge.jsx         # Badges de skills
│   │   │   ├── StateComponents.jsx    # Estados (loading, error)
│   │   │   └── CardComponents.jsx     # Componentes reutilizables
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx          # Dashboard principal
│   │   │   ├── UploadResume.jsx       # Upload de CV
│   │   │   ├── CandidateList.jsx      # Listado de candidatos
│   │   │   ├── CandidateDetail.jsx    # Detalle del candidato
│   │   │   ├── JobList.jsx            # Listado de trabajos
│   │   │   ├── JobDetail.jsx          # Detalle del trabajo
│   │   │   ├── Matches.jsx            # Matching de candidatos
│   │   │   └── Settings.jsx           # Configuración
│   │   ├── services/
│   │   │   ├── api.js                 # Cliente HTTP
│   │   │   ├── candidateService.js    # API candidatos
│   │   │   ├── jobService.js          # API trabajos
│   │   │   └── matchingService.js     # API matching
│   │   ├── styles/
│   │   │   └── *.css                  # Estilos globales
│   │   └── utils/
│   ├── package.json                   # Dependencias Node
│   ├── vite.config.js                 # Config Vite
│   └── Dockerfile                     # Containerización
│
├── docker-compose.yml                 # Orquestación de servicios
└── README.md                          # Este archivo
```

---

## 🔧 Instalación

### **Requisitos Previos**
- Python 3.9+
- Node.js 18+
- MongoDB 4.4+
- Ollama (para análisis IA)
- Docker y Docker Compose (opcional)

### **1. Clonar Repositorio**
```bash
git clone https://github.com/yourusername/Scan-ATS.git
cd Scan-ATS
```

### **2. Configurar Backend**

```bash
# Navegar a carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### **3. Configurar Frontend**

```bash
# Navegar a carpeta frontend
cd frontend

# Instalar dependencias (con pnpm recomendado)
pnpm install

# O con npm
npm install
```

### **4. Iniciar Servicios Necesarios**

#### **MongoDB**
```bash
# Opción 1: Docker
docker run -d -p 27017:27017 --name mongodb mongo

# Opción 2: Instalado localmente
mongod
```

#### **Ollama (Servidor LLM)**
```bash
# Instalar desde https://ollama.ai
ollama serve

# En otra terminal, descargar modelo base
ollama pull qwen3-vl:4b

# O usar la variante customizada del proyecto (recomendado)
ollama pull scan-ats-qwen3-vl-instruct:4b

# Verificar modelos instalados
ollama list
```

**Modelos Disponibles**:
- **qwen3-vl:4b** (3.3 GB) - Modelo base original
- **scan-ats-qwen3-vl-instruct:4b** (3.3 GB) - Variante optimizada para Scan-ATS (recomendado)

La variante optimizada tiene mejor performance para extracción de datos de CV.

---

## ⚙️ Configuración

### **Backend - Variables de Entorno**

Crear archivo `.env` en `backend/`:

```bash
# MongoDB
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=scan_ats

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=scan-ats-qwen3-vl-instruct:4b

# API
API_HOST=127.0.0.1
API_PORT=8000
```

**Nota sobre OLLAMA_MODEL**:
- Por defecto usa `scan-ats-qwen3-vl-instruct:4b` (variante optimizada)
- Si no tienes la variante, puedes cambiar a `qwen3-vl:4b` (modelo base)
- Asegúrate de que el modelo está instalado: `ollama list`

### **Frontend - Configuración de API**

El archivo `frontend/src/services/api.js` configura la URL base:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
```

---

## 🚀 Cómo Ejecutar

### **Opción 1: Ejecución Manual**

**Terminal 1 - Backend API:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API disponible en: `http://127.0.0.1:8000`
Swagger UI: `http://127.0.0.1:8000/docs`

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm dev
```

Frontend disponible en: `http://localhost:5173`

**Terminal 3 - Ollama (si no está en background):**
```bash
ollama serve
```

### **Opción 2: Con Docker Compose**

```bash
# En la raíz del proyecto
docker-compose up -d

# Verificar servicios
docker-compose ps

# Ver logs
docker-compose logs -f
```

### **Verificar que Todo Funciona**

```bash
# Health check del backend
curl http://127.0.0.1:8000/health

# Verificar conexión MongoDB
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017').admin.command('ismaster')"

# Verificar Ollama
curl http://localhost:11434/api/tags

# Listar modelos instalados
ollama list

# Verificar que el modelo configurado está disponible
ollama show scan-ats-qwen3-vl-instruct:4b
```

---

## 📊 Flujo de Datos

### **1. Upload de CV → Análisis**

```
┌─────────────────────────┐
│  Usuario sube CV (PDF)  │
└────────────┬────────────┘
             ↓
┌─────────────────────────────────────────┐
│  DocumentService.get_resume_images()    │  
│  (PyMuPDF extrae páginas)               │
└────────────┬────────────────────────────┘
             ↓
┌──────────────────────────────────────────────┐
│  AIService.analyze_resume(images)            │
│  (Ollama LLM extrae información en JSON)    │
└────────────┬─────────────────────────────────┘
             ↓
    ┌────────────────────────┐
    │ JSON Estructurado:     │
    │ - name                 │
    │ - email                │
    │ - experience[]         │
    │ - education[]          │
    │ - technical_skills[]   │
    │ - soft_skills[]        │
    │ - certifications[]     │
    │ - projects[]           │
    └────────┬───────────────┘
             ↓
┌──────────────────────────────────────────────────────┐
│  create_candidate(candidate_data)                    │
│  • Guarda CV en MongoDB                              │
│  • Guarda archivo en GridFS                          │
│  • Retorna candidate_id                              │
└────────────┬─────────────────────────────────────────┘
             ↓
┌────────────────────────────────────────────────────────┐
│  evaluate_candidate(candidate_data)                    │
│  • Calcula 8 componentes de score                      │
│  • Retorna objeto con score, clasificación,           │
│    breakdown de componentes                           │
└────────────┬───────────────────────────────────────────┘
             ↓
┌──────────────────────────────────────────────────────┐
│  Guarda score en MongoDB                             │
│  candidate.candidate_score = evaluation              │
└──────────────────────────────────────────────────────┘
```

### **2. Evaluación de Candidato**

```
Datos Crudos del CV
        ↓
   ┌─────────────────────────────────────┐
   │  Normalización de Datos             │
   │  • Parse dates (NOVIEMBRE 2022...)  │
   │  • Normaliza skills                 │
   │  • Extrae información estructurada  │
   └──────────────┬──────────────────────┘
                  ↓
        ┌─────────────────────────────────────┐
        │  Cálculo de 8 Componentes           │
        ├─────────────────────────────────────┤
        │  1. Experience (25%)                │
        │     - Años de experiencia           │
        │     - Seniority (gerente, lead)     │
        │                                     │
        │  2. Technical Skills (20%)          │
        │     - Cantidad de skills            │
        │     - Evidencia en experiencia      │
        │                                     │
        │  3. Education (10%)                 │
        │     - Grado (Licenciatura, Master)  │
        │     - Honores (Magna Cum Laude)     │
        │     - Campo relevante               │
        │                                     │
        │  4. Achievements (10%)              │
        │     - Métricas cuantificadas        │
        │     - Lenguaje de resultado         │
        │     - Leadership                    │
        │                                     │
        │  5. Certifications (10%)            │
        │     - Cantidad de certificaciones   │
        │     - Relevancia                    │
        │                                     │
        │  6. Projects (15%)                  │
        │     - Cantidad de proyectos         │
        │     - Complejidad                   │
        │                                     │
        │  7. CV Quality (5%)                 │
        │     - Estructura y completitud      │
        │     - Claridad                      │
        │                                     │
        │  8. Consistency (5%)                │
        │     - Coherencia temporal           │
        │     - Alineación con perfil         │
        └──────────────┬──────────────────────┘
                       ↓
           ┌───────────────────────────────┐
           │  Aplicar Pesos y Normalizar   │
           │  Score = Σ(Componente × Peso)│
           │  / Σ(Pesos Aplicables)       │
           └───────────────┬───────────────┘
                           ↓
                ┌────────────────────────┐
                │  Score: 0-100          │
                │  Clasificación:        │
                │  - Pobre (< 40)        │
                │  - Débil (40-60)       │
                │  - Moderado (60-75)    │
                │  - Fuerte (75-90)      │
                │  - Excelente (≥ 90)    │
                └────────────────────────┘
```

### **3. Visualización en Frontend**

```
CandidateDetail.jsx
        ↓
┌─────────────────────────────────────┐
│  GET /api/candidates/{id}           │
│  • Datos del candidato              │
│  • Desglose de componentes          │
│  • Información de skills            │
└────────────┬────────────────────────┘
             ↓
   ┌─────────────────────────────────────┐
   │  Renderizar Componentes             │
   ├─────────────────────────────────────┤
   │  • ScoreCard (visualización gráfica)│
   │  • ScoreBreakdown (8 componentes)   │
   │  • SkillBadges (skills)             │
   │  • Experience Timeline              │
   │  • Education Info                   │
   │  • Button: "📄 View Resume"         │
   └─────────────────────────────────────┘
```

---

## 🔌 API Endpoints

### **Candidatos**

#### **Upload de CV**
```http
POST /api/candidates/upload
Content-Type: multipart/form-data

Body:
- file: <binary PDF/JPG>

Response: 200 OK
{
  "message": "Resume processed successfully",
  "candidate_id": "507f1f77bcf86cd799439011",
  "candidate": {
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "candidate_score": {
      "score": 64,
      "classification": "Moderate Candidate",
      "scores": {...}
    }
  }
}
```

#### **Listar Candidatos**
```http
GET /api/candidates

Response: 200 OK
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "Juan Pérez",
    "candidate_score": 64,
    "classification": "Moderate Candidate"
  },
  ...
]
```

#### **Obtener Candidato**
```http
GET /api/candidates/{candidate_id}

Response: 200 OK
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+34 612 345 678",
  "location": "Madrid",
  "experience": [...],
  "education": [...],
  "technical_skills": [...],
  "candidate_score": {...},
  "resume": {
    "file_id": "507f1f77bcf86cd799439012",
    "filename": "cv_juan.pdf",
    "content_type": "application/pdf"
  }
}
```

#### **Descargar CV**
```http
GET /api/candidates/{candidate_id}/resume

Response: 200 OK (Binary PDF/Image file)
```

#### **Obtener Score**
```http
GET /api/candidates/{candidate_id}/score

Response: 200 OK
{
  "candidate_id": "507f1f77bcf86cd799439011",
  "score": 64,
  "classification": "Moderate Candidate",
  "scores": {
    "experience": 100,
    "education": 100,
    "achievements": 85,
    ...
  }
}
```

#### **Recalcular Score de Candidato**
```http
POST /api/candidates/{candidate_id}/recalculate-score

Response: 200 OK
{
  "message": "Score recalculated successfully",
  "candidate_id": "507f1f77bcf86cd799439011",
  "score": 64,
  ...
}
```

#### **Recalcular Todos los Scores**
```http
POST /api/candidates/recalculate-scores

Response: 200 OK
{
  "message": "Recalculated scores for 5 candidate(s)",
  "updated_count": 5,
  "total_candidates": 5,
  "errors": null
}
```

### **Trabajos**

#### **Crear Trabajo**
```http
POST /api/jobs

Body:
{
  "title": "Senior Python Developer",
  "description": "...",
  "requirements": [...],
  "skills": [...]
}

Response: 201 Created
```

#### **Listar Trabajos**
```http
GET /api/jobs

Response: 200 OK
[...]
```

#### **Obtener Trabajo**
```http
GET /api/jobs/{job_id}

Response: 200 OK
```

---

## 💡 Ejemplos de Uso

### **Ejemplo 1: Upload y Evaluación Completa**

```python
# Backend - Python
import requests

# 1. Preparar archivo
with open('cv.pdf', 'rb') as f:
    files = {'file': f}
    
    # 2. Upload
    response = requests.post(
        'http://127.0.0.1:8000/api/candidates/upload',
        files=files
    )
    
    # 3. Procesar respuesta
    data = response.json()
    candidate_id = data['candidate_id']
    score = data['candidate']['candidate_score']['score']
    
    print(f"Candidato creado: {candidate_id}")
    print(f"Score: {score}/100")
```

### **Ejemplo 2: Consultar Detalles del Candidato**

```javascript
// Frontend - React
import candidateService from '../services/candidateService'

// Obtener datos del candidato
const candidate = await candidateService.getCandidate(candidateId)

// Ver CV en nueva pestaña
const resumeUrl = candidateService.getResumeUrl(candidateId)
window.open(resumeUrl, '_blank')

// Descargar CV
const resumeBlob = await candidateService.downloadResume(candidateId)
// Crear link de descarga...
```

### **Ejemplo 3: Debugging de Evaluación**

```bash
# Ejecutar test de evaluación
cd backend
python test_evaluation_otilia.py

# Ver desglose de skills
python debug_skills.py
```

---

## 🔍 Troubleshooting

### **Problema: "MongoDB connection refused"**
```bash
# Verificar que MongoDB está corriendo
mongod --version

# Iniciar MongoDB
mongod

# O con Docker
docker run -d -p 27017:27017 mongo
```

### **Problema: "Ollama connection refused"**
```bash
# Verificar que Ollama está corriendo
ollama serve

# En otra terminal, verificar disponibilidad
curl http://localhost:11434/api/tags

# Descargar modelo si falta
ollama pull scan-ats-qwen3-vl-instruct:4b

# O el modelo base
ollama pull qwen3-vl:4b

# Listar modelos instalados
ollama list
```

### **Problema: "Model not found" en backend**
- Verificar que el modelo especificado en `.env` está instalado
- Ejecutar `ollama list` para ver modelos disponibles
- Cambiar `OLLAMA_MODEL` en `.env` al nombre exacto del modelo
- Reiniciar el backend después de cambiar variables de entorno

### **Problema: "CORS errors en frontend"**
- Verificar que el backend tiene CORS habilitado
- En `backend/app/main.py`, revisar configuración de CORSMiddleware
- Asegurarse que `http://localhost:5173` está en `allow_origins`

### **Problema: Score = 0**
```bash
# Verificar logs del backend
# Look for "=== CANDIDATE EVALUATION ===" section

# Ejecutar test de evaluación
cd backend
python test_evaluation_otilia.py

# Ver qué skills fueron detectados
python debug_skills.py
```

---

## 📈 Performance y Escalabilidad

### **Optimizaciones Implementadas**
- Evaluación determinística (sin AI en scoring)
- Caching de skills normalizados
- GridFS para almacenamiento eficiente de binarios
- Índices MongoDB para búsquedas rápidas

### **Limitaciones Actuales**
- Ollama requiere GPU para mejor performance
- MongoDB local adecuada para desarrollo
- Frontend single-instance sin load balancing

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📄 Licencia

Proyecto bajo licencia MIT - ver archivo `LICENSE`

---

## 📧 Contacto y Soporte

Para preguntas o soporte, contactar al equipo de desarrollo.

---

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)

---

**Última actualización**: Septiembre 2026
**Versión**: 0.1.0