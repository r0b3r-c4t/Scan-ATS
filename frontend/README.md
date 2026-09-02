# Scan-ATS Frontend

Frontend completo de Scan-ATS construido con React, Vite y TypeScript.

## Requisitos

- Node.js 18+
- pnpm

## Instalación

```bash
cd frontend
pnpm install
```

## Desarrollo

Para iniciar el servidor de desarrollo en http://localhost:5173:

```bash
pnpm dev
```

## Build

Para crear un build de producción:

```bash
pnpm build
```

## Características Implementadas

✅ **Dashboard** - Resumen de estadísticas, candidatos principales y recientes
✅ **Candidates** - Listado de candidatos con búsqueda, filtrado y ordenamiento
✅ **Candidate Detail** - Detalle completo del candidato con evaluación, habilidades, experiencia, educación
✅ **Upload Resume** - Carga de CVs con análisis automático mediante IA
✅ **Jobs** - Listado de posiciones/empleos
✅ **Create Job** - Formulario para crear nuevos empleos
✅ **Job Detail** - Detalle del empleo con lista de candidatos compatibles
✅ **Matches** - Visualización de candidatos emparejados con empleos
✅ **Responsive Design** - Funciona en desktop, tablet y mobile
✅ **Modern UI** - Diseño minimalista con colores corporativos (#F9FAFB, #1B5E3B, #0A0A0A)

## Estructura de Carpetas

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── Layout.jsx       # Layout principal con sidebar
│   │   ├── ScoreRing.jsx    # Componente de puntuación
│   │   ├── ScoreBreakdown.jsx
│   │   ├── SkillBadge.jsx
│   │   ├── CardComponents.jsx
│   │   └── StateComponents.jsx (Loading, Error, Empty)
│   ├── pages/               # Páginas de la aplicación
│   │   ├── Dashboard.jsx
│   │   ├── CandidateList.jsx
│   │   ├── CandidateDetail.jsx
│   │   ├── UploadResume.jsx
│   │   ├── JobList.jsx
│   │   ├── CreateJob.jsx
│   │   ├── JobDetail.jsx
│   │   ├── Matches.jsx
│   │   └── Settings.jsx
│   ├── services/            # Servicios de API
│   │   ├── api.js           # Cliente Axios configurado
│   │   ├── candidateService.js
│   │   ├── jobService.js
│   │   └── matchingService.js
│   ├── styles/
│   │   └── index.css        # Estilos globales
│   ├── utils/
│   │   └── scoreUtils.js    # Utilidades para puntuaciones
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── vite.config.js
├── package.json
└── .env                     # Variables de entorno
```

## Variables de Entorno

```
VITE_API_URL=http://127.0.0.1:8000
```

## Endpoints de API Utilizados

### Candidates
- `POST /api/candidates/upload` - Subir CV
- `GET /api/candidates` - Listar candidatos
- `GET /api/candidates/{candidate_id}` - Obtener detalle
- `GET /api/candidates/{candidate_id}/score` - Obtener puntuación

### Jobs
- `POST /api/jobs` - Crear empleo
- `GET /api/jobs` - Listar empleos
- `GET /api/jobs/{job_id}` - Obtener detalle

### Matching
- `GET /api/jobs/{job_id}/candidates/{candidate_id}/match` - Obtener compatibilidad
- `GET /api/jobs/{job_id}/matches` - Obtener todos los matchings

## Ejecución Completa

### Terminal 1 - Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Terminal 2 - Frontend
```bash
cd frontend
pnpm dev
```

Luego abre http://localhost:5173 en tu navegador.

## Colores Utilizados

- **Background Principal**: #F9FAFB
- **Verde Principal**: #1B5E3B
- **Texto**: #0A0A0A
- **Texto Secundario**: #6B7280
- **Borde**: #E5E7EB
