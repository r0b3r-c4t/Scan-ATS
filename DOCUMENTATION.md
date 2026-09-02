# 📚 Scan-ATS - Documentación Completa

## 🎯 Inicio Rápido

### Para ejecutar la aplicación:

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
# http://127.0.0.1:8000
# Swagger: http://127.0.0.1:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm install  # Primera vez
pnpm dev
# http://localhost:5173
```

---

## 📖 Documentación por Sección

### Frontend Documentation
- [README Frontend](frontend/README.md) - Documentación principal del frontend
- [SUMMARY](SUMMARY.md) - Resumen ejecutivo del proyecto
- [VERIFICATION_CHECKLIST](VERIFICATION_CHECKLIST.md) - Checklist de verificación completo
- [IMPLEMENTATION_SUMMARY](frontend/IMPLEMENTATION_SUMMARY.md) - Detalles técnicos de implementación

### Instrucciones de Ejecución
- [GETTING_STARTED.sh](GETTING_STARTED.sh) - Script para Linux/Mac
- [GETTING_STARTED.bat](GETTING_STARTED.bat) - Script para Windows

---

## 🏗️ Estructura del Proyecto

```
Scan-ATS/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── main.py            # ✅ CORS configurado
│   │   ├── routes/
│   │   │   ├── candidates.py
│   │   │   └── jobs.py
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── models/
│   │   └── database/
│   └── requirements.txt
│
├── frontend/                   # ✅ Nuevo - React + Vite
│   ├── src/
│   │   ├── components/        # 6 componentes reutilizables
│   │   ├── pages/             # 9 páginas
│   │   ├── services/          # 4 servicios de API
│   │   ├── styles/            # Estilos globales
│   │   ├── utils/             # Funciones auxiliares
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json           # ✅ Con pnpm
│   ├── vite.config.js
│   ├── .env
│   └── README.md
│
├── docker-compose.yml
└── README.md
```

---

## 🎯 Funcionalidades por Página

### 📊 Dashboard
Archivos: `frontend/src/pages/Dashboard.jsx`
- Estadísticas en tiempo real
- Top candidatos
- Candidatos recientes
- Conexión a API real

### 👥 Candidates
**List:**
- Archivos: `frontend/src/pages/CandidateList.jsx`
- Búsqueda por nombre/email
- Ordenamiento por puntuación
- Grid responsivo de candidatos

**Detail:**
- Archivos: `frontend/src/pages/CandidateDetail.jsx`
- Información completa del candidato
- Candidate Score visual
- Desglose de evaluación
- Habilidades, experiencia, educación, certificaciones, proyectos

### 📄 Upload Resume
Archivos: `frontend/src/pages/UploadResume.jsx`
- Drag & drop de archivos
- Carga con análisis IA
- Estados de progreso
- Pantalla de éxito con puntuación

### 💼 Jobs
**List:**
- Archivos: `frontend/src/pages/JobList.jsx`
- Listado de empleos
- Cards con información resumida

**Create:**
- Archivos: `frontend/src/pages/CreateJob.jsx`
- Formulario completo
- Habilidades dinámicas
- Validación

**Detail:**
- Archivos: `frontend/src/pages/JobDetail.jsx`
- Información del empleo
- Candidatos emparejados
- Match Score por candidato

### 🎯 Matches
Archivos: `frontend/src/pages/Matches.jsx`
- Selector de empleos
- Tabla de compatibilidad
- Detalles de matching
- Clasificación visual

---

## 🔌 Integración API

### Servicios Implementados

**candidateService.js**
- `uploadResume(file)` → POST /api/candidates/upload
- `getCandidates()` → GET /api/candidates
- `getCandidate(id)` → GET /api/candidates/{id}
- `getCandidateScore(id)` → GET /api/candidates/{id}/score

**jobService.js**
- `createJob(data)` → POST /api/jobs
- `getJobs()` → GET /api/jobs
- `getJob(id)` → GET /api/jobs/{id}

**matchingService.js**
- `getMatch(jobId, candidateId)` → GET /api/jobs/{jobId}/candidates/{candidateId}/match
- `getJobMatches(jobId)` → GET /api/jobs/{jobId}/matches

### Configuración CORS
El backend ahora permite peticiones desde:
- http://localhost:5173
- http://127.0.0.1:5173

---

## 🎨 Componentes Reutilizables

### Layout (`components/Layout.jsx`)
- Sidebar con navegación
- Header con usuario
- Área de contenido principal
- Responsivo (colapsable en desktop, drawer en mobile)

### ScoreRing (`components/ScoreRing.jsx`)
- Visualización circular de puntuación
- Rango 0-100 con clasificación
- Dos variantes: Candidate Score y Match Score
- Tamaños: sm, md, lg

### ScoreBreakdown (`components/ScoreBreakdown.jsx`)
- Desglose de componentes
- Barras de progreso animadas
- Muestra porcentajes

### SkillBadge (`components/SkillBadge.jsx`)
- Badges para habilidades
- Soporte para strings con separador "·"
- Variantes de color

### CardComponents (`components/CardComponents.jsx`)
- CandidateCard: Información resumida de candidato
- JobCard: Información resumida de empleo

### StateComponents (`components/StateComponents.jsx`)
- LoadingState: Spinner con mensaje
- ErrorState: Mensaje de error con retry
- EmptyState: Estado vacío con CTA

---

## 🎨 Diseño Visual

### Paleta de Colores
```css
--color-bg-primary: #F9FAFB;        /* Fondo principal */
--color-green-primary: #1B5E3B;     /* Verde corporativo */
--color-text-primary: #0A0A0A;      /* Texto principal */
--color-border: #E5E7EB;            /* Bordes */
--color-error: #EF4444;             /* Error */
--color-success: #10B981;           /* Éxito */
```

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1023px
- Laptop: 1024px - 1399px
- Desktop: ≥ 1400px

### Componentes de Diseño
- Cards con shadow y hover
- Botones con estados (hover, disabled)
- Inputs con focus state
- Badges para etiquetas
- Progress bars animadas
- Loading spinner

---

## 📊 Stack Tecnológico

### Frontend
- **React** 18.3.1 - UI library
- **Vite** 5.4.21 - Build tool y dev server
- **React Router** 6.30.6 - Enrutamiento
- **Axios** 1.20.0 - HTTP client
- **CSS** Moderno - Estilos (sin frameworks CSS)

### Backend
- **FastAPI** - API framework
- **FastAPI CORS** - Soporte CORS
- **Python** 3.8+ - Lenguaje
- **MongoDB** - Base de datos
- **AI Service** - Análisis de CVs (Ollama)

---

## 📋 Variables de Entorno

### Frontend (.env)
```
VITE_API_URL=http://127.0.0.1:8000
```

### Backend (.env)
```
MONGODB_URI=...
OLLAMA_API_URL=...
```

---

## 🚀 Comandos Útiles

### Frontend
```bash
# Instalar dependencias
pnpm install

# Desarrollo (http://localhost:5173)
pnpm dev

# Build de producción
pnpm build

# Preview de build
pnpm preview
```

### Backend
```bash
# Desarrollo con reload
python -m uvicorn app.main:app --reload

# Producción
python -m uvicorn app.main:app

# Swagger UI
# http://127.0.0.1:8000/docs
```

---

## 📝 Notas Importantes

1. **Sin Datos Mock**: Toda la aplicación funciona con datos reales del backend
2. **CORS Configurado**: El backend permite peticiones del frontend
3. **Responsive**: Funciona en todos los dispositivos
4. **Componentes Reutilizables**: Fácil de mantener y escalar
5. **Manejo de Errores**: Estados consistentes en toda la aplicación
6. **Rendimiento**: Optimizado para carga rápida

---

## 🔍 Estructura de Datos

### Candidate (del backend)
```javascript
{
  _id: ObjectId,
  name: string,
  email: string,
  phone: string,
  location: string,
  summary: string,
  technical_skills: string | array,
  experience: array,
  education: array,
  certifications: array,
  projects: array,
  candidate_score: {
    score: 0-100,
    classification: "Excellent" | "Strong" | "Moderate" | "Weak" | "Poor",
    components: { ... },
    strengths: array,
    areas_to_improve: array,
    warnings: array
  },
  resume: { file_id, filename, content_type, size }
}
```

### Job (del backend)
```javascript
{
  _id: ObjectId,
  title: string,
  description: string,
  required_skills: array,
  preferred_skills: array,
  minimum_experience: string,
  education_requirements: string,
  required_certifications: array
}
```

### Match (del backend)
```javascript
{
  candidate_id: string,
  job_id: string,
  match_percentage: 0-100,
  classification: "Excellent" | "Strong" | "Moderate" | "Weak" | "Poor",
  scores: { ... },
  explanation: string
}
```

---

## 🎓 Tutorial de Uso

### 1. Subir un CV
1. Ir a "Candidates" → "Upload Resume"
2. Arrastra un PDF/JPG/PNG o selecciona archivo
3. Espera análisis (estados de progreso mostrados)
4. Ver score y hacer clic en "View Candidate Profile"

### 2. Crear una Vacante
1. Ir a "Jobs" → "+ Create Job"
2. Completa título y descripción
3. Agrega habilidades requeridas y preferidas
4. Haz clic en "Create Job"

### 3. Ver Candidatos
1. Ir a "Candidates"
2. Busca por nombre o email
3. Ordena por score
4. Haz clic en una card para ver detalles

### 4. Emparejar Candidatos
1. Ir a "Matches"
2. Selecciona un empleo
3. Ve la tabla de candidatos emparejados
4. Haz clic en un candidato para ver detalles del match

---

## 🐛 Troubleshooting

**Error de CORS:**
- Asegúrate de que el backend tiene CORS configurado
- Verifica que VITE_API_URL es correcto

**Frontend no se conecta:**
- Checa que backend está corriendo en http://127.0.0.1:8000
- Verifica la consola del navegador para errores

**Componentes no cargan:**
- Revisa que vite está corriendo correctamente
- Limpia cache: `rm -rf node_modules && pnpm install`

---

## 📞 Soporte

Para más información:
- Ver archivos README.md en cada carpeta
- Revisar comentarios en el código
- Consultar documentación de dependencias

---

**Documentación completa de Scan-ATS Frontend ✅**
