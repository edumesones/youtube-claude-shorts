# 🎬 YOUTUBE CLAUDE SHORTS - PROYECTO COMPLETO

## 📋 Resumen Ejecutivo

**Objetivo:** Canal de YouTube Shorts sobre tips de Claude Code, generados automáticamente cada día en español.

**Estado:** 95% automatizable (requiere setup inicial manual de 2-4 horas)

**Costo:** $0-10/mes (versión económica)

---

## 🚀 COMPONENTES AUTOMÁTICOS

### ✅ 100% Automáticos (después de setup)

| Componente | Tecnología | Costo |
|------------|------------|-------|
| Obtener tips | GitHub API (CHANGELOG) | Gratis |
| Generar scripts | Claude API | $0-5/mes |
| Texto a voz | ElevenLabs / edge-tts | $0-5/mes |
| Crear videos | MoviePy + FFmpeg | Gratis |
| Generar thumbnails | DALL-E 3 / Pillow | $0-4/mes |
| Subir a YouTube | YouTube Data API v3 | Gratis |
| Moderar comentarios | Claude API | $0-2/mes |
| Responder comentarios | Claude API | Incluido |
| A/B testing thumbnails | YouTube API | Gratis |
| Analytics/Optimización | Python + YouTube API | Gratis |

### ⚠️ Requiere Setup Inicial (una vez)

| Tarea | Tiempo | Automatizable |
|-------|--------|---------------|
| Crear canal YouTube | 15 min | ❌ NO |
| Verificar teléfono | 5 min | ❌ NO |
| Google Cloud project | 20 min | ❌ NO |
| OAuth + refresh token | 30 min | ⚠️ Semi |
| GitHub Secrets | 10 min | ❌ NO |

---

## 🏗️ ARQUITECTURA

```
GitHub Actions (9:00 AM UTC)
│
├─ 1. Fetch: CHANGELOG de claude-code (GitHub API)
│     └─ Extraer tip del día
│
├─ 2. Generate: Script con Claude API
│     └─ 30-45s, español, viral style
│
├─ 3. Safety: Check con Perspective API
│     └─ Si no pasa → skip día
│
├─ 4. Voice: ElevenLabs TTS
│     └─ Fallback: edge-tts (gratis)
│
├─ 5. Visual: DALL-E 3 thumbnail
│     └─ 2 variantes para A/B test
│
├─ 6. Render: MoviePy
│     └─ 1080x1920, 30fps, subs
│
├─ 7. Upload: YouTube Data API
│     └─ OAuth con refresh token
│
├─ 8. Test: A/B thumbnails (1h)
│     └─ Auto-selección mejor CTR
│
└─ 9. Log: Commit a repo
      └─ Stats y métricas
```

---

## 💰 COSTOS

### Opción Económica ($0/mes)
- Claude API: Gratis tier
- TTS: edge-tts (gratis)
- Thumbnails: Gradiente + texto (Pillow)
- Todo lo demás: Gratis

### Opción Profesional ($10/mes)
- Claude API: $5
- ElevenLabs: $5
- Thumbnails: DALL-E 3 (~$0.12/imagen)

### Opción Premium ($30/mes)
- Claude API: $20
- ElevenLabs Pro: $22
- Stable Diffusion API: $10

---

## 📁 ESTRUCTURA DEL REPO

```
youtube-claude-shorts/
├── .github/
│   └── workflows/
│       └── daily-short.yml      # Cron 9AM UTC
├── src/
│   ├── __init__.py
│   ├── fetch_tip.py             # GitHub API
│   ├── generate_script.py       # Claude API
│   ├── generate_voice.py        # ElevenLabs/edge-tts
│   ├── generate_thumbnail.py    # DALL-E/Pillow
│   ├── render_video.py          # MoviePy
│   ├── upload_youtube.py        # YouTube API
│   ├── moderate_comments.py     # Auto-moderación
│   └── utils.py                 # Helpers
├── assets/
│   ├── fonts/                   # Fuentes
│   └── templates/               # Templates base
├── output/                      # Videos (gitignored)
├── logs/                        # Métricas
├── requirements.txt
├── config.yaml
└── README.md
```

---

## 🔧 SETUP INICIAL

### Paso 1: Crear Canal YouTube (Manual)
```bash
# Ir a youtube.com
# Click "Crear canal"
# Nombre: "Claude Code Tips ES"
# Verificar con teléfono
```

### Paso 2: Google Cloud Project (Manual)
```bash
# 1. Ir a console.cloud.google.com
# 2. Crear nuevo proyecto
# 3. Habilitar "YouTube Data API v3"
# 4. Crear OAuth 2.0 credentials
# 5. Descargar client_secret.json
```

### Paso 3: Obtener Refresh Token (Semi-auto)
```bash
# Correr script localmente UNA VEZ
python get_refresh_token.py

# Abre browser, autoriza, copia refresh token
# Guardar en GitHub Secret: YOUTUBE_REFRESH_TOKEN
```

### Paso 4: GitHub Secrets
```
YOUTUBE_REFRESH_TOKEN=1//04xxxxxxxx...
YOUTUBE_CLIENT_ID=123456789.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=GOCSPX-xxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
ELEVENLABS_API_KEY=sk_xxxxxxxx
```

### Paso 5: Deploy
```bash
git push origin main
# GitHub Actions corre automáticamente
```

---

## 🎬 EJEMPLO DE FLUJO

### Input
```markdown
## 2.1.62

- Fixed prompt suggestion cache regression that reduced cache hit rates
```

### Output
**Video:** 28 segundos
**Título:** "🚀 Claude Code más RÁPIDO | Actualización 2.1.62"
**Views (estimado):** 500-2000

---

## 📊 MÉTRICAS ESPERADAS

| Métrica | Mes 1 | Mes 3 | Mes 6 |
|---------|-------|-------|-------|
| Videos | 30 | 90 | 180 |
| Subs | 100 | 1,000 | 5,000 |
| Views totales | 5,000 | 50,000 | 200,000 |
| Costo/video | $0.33 | $0.11 | $0.06 |

---

## ⚠️ RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| YouTube detecta automatización | Baja | Contenido original, delays humanos |
| API rate limits | Media | Exponential backoff, retries |
| Contenido inapropiado | Baja | Safety checks con Claude/Perspective |
| Cambios en APIs | Media | Abstracción de providers |
| Cuenta Google ban | Muy baja | Seguir TOS, contenido educativo |

---

## 🛠️ IMPLEMENTACIÓN

### ¿Quieres que lo construya?

Puedo crear:
1. ✅ Repo completo con código
2. ✅ GitHub Actions workflow
3. ✅ Scripts de setup
4. ✅ Documentación detallada
5. ✅ Primer video de prueba

**Tiempo estimado:** 4-6 horas de desarrollo

**¿Empezamos?**
