# 🎬 YouTube Shorts Claude Code - Investigación Completa

## 📋 Resumen Ejecutivo

Proyecto: Canal de YouTube Shorts sobre tips de Claude Code, generados automáticamente cada día en español.

---

## 1. 📦 DEPENDENCIAS Y TECNOLOGÍAS

### 1.1 Generación de Contenido (Scripts)

| Opción | Costo | Pros | Contras |
|--------|-------|------|---------|
| **Claude API** (Anthropic) | $3-5/mes (usage-based) | Nativo para Claude Code, español excelente | Rate limits |
| **OpenAI GPT-4** | $5-10/mes | Muy rápido, buen español | Más caro |
| **Gemini 2.0 Flash** | Gratis (generous limit) | Costo cero, buen rendimiento | Menos control de tono |

**Recomendación**: Claude API + Gemini como backup

**Fuentes de contenido:**
- GitHub: `anthropics/claude-code/CHANGELOG.md`
- Docs: `code.claude.com/docs` (via GitHub commits)
- `/help` de Claude Code (comandos disponibles)
- Comunidad: Reddit r/claude, Discord Anthropic

### 1.2 Texto a Voz (TTS)

| Proveedor | Costo | Calidad | Latencia |
|-----------|-------|---------|----------|
| **ElevenLabs** | $5/mes (starter) | ⭐⭐⭐⭐⭐ Excelente | Media |
| **Azure TTS** | $4/mes (500K chars) | ⭐⭐⭐⭐ Muy buena | Baja |
| **Google TTS** | $4/mes (1M chars) | ⭐⭐⭐ Buena | Baja |
| **Amazon Polly** | $4/mes (1M chars) | ⭐⭐⭐ Buena | Baja |
| **edge-tts** (gratis) | $0 | ⭐⭐ Regular | Baja |

**Recomendación**: ElevenLabs para calidad, edge-tts para testing/gratis

**Voces recomendadas ElevenLabs (español):**
- `Bella` (femenino, claro)
- `Adam` (masculino, profesional)
- `Antoni` (español neutro)

### 1.3 Edición de Video

#### Opción A: Python puro
```bash
pip install moviepy pillow numpy
```

**Pros:** Control total, gratuito
**Contras:** Más lento, requiere ffmpeg

#### Opción B: FFmpeg directo
```bash
# Más rápido, menos flexible
ffmpeg -i input.mp4 -vf "..." output.mp4
```

#### Opción C: Servicios cloud
- **Remotion** ($7/mes) - React-based video
- **Shotstack** (pay-per-render)
- **Bannerbear** (templates)

**Recomendación**: MoviePy + FFmpeg para empezar

### 1.4 Generación de Imágenes/Fondos

| Opción | Costo | Calidad | Uso |
|--------|-------|---------|-----|
| **Stable Diffusion XL** (local) | $0 (GPU) | ⭐⭐⭐⭐ | Fondos únicos |
| **DALL-E 3** | $0.04/imagen | ⭐⭐⭐⭐⭐ | Alta calidad |
| **Midjourney** | $10/mes | ⭐⭐⭐⭐⭐ | Estilo consistente |
| **Unsplash API** | Gratis | ⭐⭐⭐ | Fotos reales |
| **Pexels API** | Gratis | ⭐⭐⭐ | Fotos/videos |

**Recomendación**: Fondos gradientes animados (sin costo) + Unsplash para thumbnails

### 1.5 YouTube API

**YouTube Data API v3:**
- Costo: Gratis (10,000 unidades/día)
- Límites: 100 videos/día para channels nuevos
- Requiere: OAuth 2.0 + consentimiento

**Endpoints necesarios:**
- `videos.insert` - Subir video
- `thumbnails.set` - Subir thumbnail
- `playlistItems.insert` - Añadir a playlist

### 1.6 Infraestructura

| Componente | Opción | Costo |
|------------|--------|-------|
| **Compute** | GitHub Actions | Gratis (2,000 min/mes) |
| **Almacenamiento** | GitHub repo + LFS | Gratis (hasta 1GB) |
| **Secrets** | GitHub Secrets | Gratis |
| **Logs** | GitHub Actions logs | Gratis |

**Alternativa**: Railway/Render ($5/mes) para más control

---

## 2. 🏗️ ARQUITECTURA PROPUESTA

```
┌─────────────────────────────────────────────────────────────┐
│                     DAILY PIPELINE                          │
└─────────────────────────────────────────────────────────────┘

9:00 AM UTC (GitHub Actions Cron)
│
├─► 1. FETCH CONTENT
│   ├─ Scrapear CHANGELOG de claude-code (GitHub API)
│   ├─ Obtener commits recientes
│   └─ Elegir 1 tip/feature nuevo
│
├─► 2. GENERATE SCRIPT
│   ├─ Prompt a Claude API:
│   │   "Genera un script de 30-45 segundos sobre [TIP] 
│   │    en español, estilo viral de TikTok/Shorts"
│   └─ Output: texto + timestamps
│
├─► 3. GENERATE ASSETS
│   ├─ TTS: ElevenLabs → voz.mp3
│   ├─ Background: Gradiente animado o imagen
│   └─ Subtitles: SRT file
│
├─► 4. RENDER VIDEO
│   ├─ MoviePy: combinar voz + texto + fondo
│   ├─ Formato: 1080x1920 (9:16), 30fps
│   └─ Output: video.mp4 (30-60 segundos)
│
├─► 5. GENERATE THUMBNAIL
│   └─ Pillow: texto + imagen de fondo
│
├─► 6. UPLOAD TO YOUTUBE
│   ├─ YouTube Data API: upload video
│   ├─ Añadir título, descripción, tags
│   └─ Publicar como Short
│
└─► 7. COMMIT & LOG
    ├─ Guardar stats del video
    └─ Subir a repo para historial
```

### Estructura del Repositorio

```
youtube-claude-shorts/
├── .github/
│   └── workflows/
│       └── daily-video.yml      # Cron job
├── src/
│   ├── __init__.py
│   ├── content_fetcher.py       # Obtener tips
│   ├── script_generator.py      # Generar scripts
│   ├── tts_generator.py         # ElevenLabs
│   ├── video_renderer.py        # MoviePy
│   ├── thumbnail_generator.py   # Pillow
│   └── youtube_uploader.py      # YouTube API
├── assets/
│   ├── fonts/                   # Fuentes para texto
│   ├── templates/               # Templates base
│   └── backgrounds/             # Fondos reutilizables
├── output/                      # Videos generados (gitignored)
├── logs/                        # Logs de ejecución
├── requirements.txt
├── config.yaml                  # Configuración
└── README.md
```

---

## 3. 💰 COSTOS ESTIMADOS (Mensuales)

### Opción Económica (MVP)

| Servicio | Costo |
|----------|-------|
| Claude API (generoso tier) | $0 (gratis) |
| edge-tts | $0 |
| GitHub Actions | $0 |
| YouTube API | $0 |
| **TOTAL** | **$0/mes** |

### Opción Profesional

| Servicio | Costo |
|----------|-------|
| Claude API Pro | $5 |
| ElevenLabs Starter | $5 |
| GitHub Actions (extra minutes) | $0 |
| YouTube API | $0 |
| **TOTAL** | **$10/mes** |

### Opción Premium

| Servicio | Costo |
|----------|-------|
| Claude API | $20 |
| ElevenLabs Pro | $22 |
| Stable Diffusion API | $10 |
| Hosting (Railway/Render) | $5 |
| **TOTAL** | **$57/mes** |

**Recomendación**: Empezar con Económica ($0), escalar a Profesional ($10)

---

## 4. 🎬 EJEMPLO DE FLUJO COMPLETO

### Input: Commit del CHANGELOG
```
## 2.1.62

- Fixed prompt suggestion cache regression that reduced cache hit rates
```

### Paso 1: Generar Script (Claude API)

**Prompt:**
```
Eres un creador de contenido viral sobre tecnología. 
Crea un guión de 30 segundos en español sobre este tip de Claude Code:

"Fixed prompt suggestion cache regression that reduced cache hit rates"

El guión debe:
- Empezar con hook ("¿Claude lento?")
- Explicar el problema simple
- Dar la solución (actualizar)
- Terminar con CTA ("Sígueme para más tips")
- Incluir timestamps para cada sección

Formato:
[0:00-0:05] TEXTO
[0:05-0:15] TEXTO
...
```

**Output:**
```
[0:00-0:05] ¿Sientes que Claude Code va más lento últimamente? 🤔
[0:05-0:15] Tenías razón. Había un bug en el cache de sugerencias que ralentizaba todo.
[0:15-0:25] La solución: actualiza a la versión 2.1.62. Ahora va como un tiro. 🚀
[0:25-0:30] Sígueme para más tips de Claude Code. ¡Dale like! 👆
```

### Paso 2: Generar Voz (ElevenLabs)

```python
from elevenlabs import generate, set_api_key

set_api_key("sk_...")

audio = generate(
    text=script,
    voice="Bella",
    model="eleven_multilingual_v2"
)

with open("voice.mp3", "wb") as f:
    f.write(audio)
```

**Duración:** 28 segundos

### Paso 3: Crear Video (MoviePy)

```python
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout

# Cargar audio
audio = AudioFileClip("voice.mp3")
duration = audio.duration

# Crear fondo gradiente
bg = ColorClip(size=(1080, 1920), color=(10, 10, 30))
bg = bg.set_duration(duration)

# Añadir texto animado (subtítulos)
# ... (sincronizar con timestamps)

# Combinar
video = CompositeVideoClip([bg, text_overlay])
video = video.set_audio(audio)

# Exportar
video.write_videofile(
    "output.mp4",
    fps=30,
    codec="libx264",
    audio_codec="aac"
)
```

### Paso 4: Generar Thumbnail

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (1080, 1920), color=(20, 20, 40))
draw = ImageDraw.Draw(img)

# Título grande
draw.text((540, 960), "CLAUDE MÁS RÁPIDO 🚀", 
          font=font_title, anchor="mm")

draw.text((540, 1100), "Actualiza ahora →", 
          font=font_sub, anchor="mm")

img.save("thumbnail.jpg")
```

### Paso 5: Subir a YouTube

```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

youtube = build('youtube', 'v3', credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "🚀 Claude Code más RÁPIDO | Actualización 2.1.62",
            "description": "Descubre cómo la última actualización mejora el rendimiento de Claude Code...",
            "tags": ["claude", "claude code", "ai", "programación", "tutorial"],
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload("output.mp4")
)

response = request.execute()
print(f"Video subido: https://youtube.com/shorts/{response['id']}")
```

### Output Final

- **Video:** 28 segundos, 1080x1920
- **Título:** "🚀 Claude Code más RÁPIDO | Actualización 2.1.62"
- **Descripción:** Con explicación y links
- **Tags:** claude, claude code, ai, tutorial, tips

---

## 5. 🗺️ ROADMAP

### Fase 1: Setup (Semana 1)

- [ ] Crear canal de YouTube
- [ ] Crear proyecto Google Cloud (YouTube API)
- [ ] Crear repo GitHub
- [ ] Configurar secrets (API keys)
- [ ] Crear estructura de carpetas
- [ ] Instalar dependencias localmente

### Fase 2: MVP (Semana 2)

- [ ] Implementar `content_fetcher.py`
- [ ] Implementar `script_generator.py` (con Claude)
- [ ] Implementar `tts_generator.py` (edge-tts gratis)
- [ ] Implementar `video_renderer.py` básico
- [ ] Crear primer video manualmente
- [ ] Testear flujo completo

### Fase 3: Automatización (Semana 3)

- [ ] Implementar GitHub Actions workflow
- [ ] Configurar cron job (9 AM UTC)
- [ ] Implementar `youtube_uploader.py`
- [ ] Añadir logging y error handling
- [ ] Testear pipeline end-to-end

### Fase 4: Mejoras (Semana 4)

- [ ] Mejorar calidad de video (transiciones, efectos)
- [ ] Implementar thumbnails automáticos
- [ ] Añadir análisis de engagement
- [ ] Optimizar prompts para virality
- [ ] Implementar A/B testing de títulos

### Fase 5: Escalar (Mes 2+)

- [ ] Migrar a ElevenLabs (mejor voz)
- [ ] Múltiples videos por día
- [ ] Variaciones en otros idiomas
- [ ] Monetización

---

## 6. ⚠️ RIESGOS Y CONSIDERACIONES

### YouTube
- **Quota API:** 10,000 unidades/día (suficiente para ~20 videos)
- **Límites de subida:** Channels nuevos limitados a 100 videos/día
- **Community Guidelines:** Contenido debe ser original/educativo
- **Monetización:** Requiere 1,000 subs + 4,000 horas vistas

### Técnicos
- **API rate limits:** Implementar retry con backoff
- **Fallos de generación:** Tener fallback (video por defecto)
- **Almacenamiento:** Limpiar archivos temporales

### Legales
- **Marca:** No usar logo de Anthropic sin permiso
- **Música:** Usar solo música libre de derechos
- **Disclaimer:** Mencionar que es contenido no oficial

---

## 7. 🛠️ CÓDIGO BASE

### requirements.txt
```
anthropic>=0.18.0
google-api-python-client>=2.100.0
google-auth-oauthlib>=1.0.0
moviepy>=1.0.3
Pillow>=10.0.0
requests>=2.31.0
pyyaml>=6.0.1
```

### Configuración (config.yaml)
```yaml
# Fuentes de contenido
sources:
  github_changelog:
    repo: "anthropics/claude-code"
    file: "CHANGELOG.md"
  
  github_releases:
    repo: "anthropics/claude-code"

# Configuración de video
video:
  width: 1080
  height: 1920
  fps: 30
  duration_min: 25
  duration_max: 60

# TTS
tts:
  provider: "elevenlabs"  # o "edge"
  voice: "Bella"
  model: "eleven_multilingual_v2"

# YouTube
youtube:
  category_id: "28"
  privacy: "public"
  tags:
    - "claude"
    - "claude code"
    - "inteligencia artificial"
    - "programación"
    - "tutorial"
```

---

## 8. 📊 KPIs Y MÉTRICAS

Seguimiento recomendado:

| Métrica | Objetivo (30 días) |
|---------|-------------------|
| Videos publicados | 30 |
| Views totales | 10,000 |
| Subs ganados | 500 |
| CTR (thumbnail) | >5% |
| Avg view duration | >50% |
| Costo por video | <$0.50 |

---

## 🎯 CONCLUSIÓN

**Es viable:** Sí, con inversión inicial de $0-10/mes

**Tiempo de implementación:** 2-4 semanas para MVP

**Diferenciación:** Contenido diario, español, tips específicos de Claude Code

**Próximo paso:** ¿Quieres que empiece a crear el repo y el código base?
