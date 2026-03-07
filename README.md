# 🎬 YouTube Claude Shorts - 100% Automático

## ⚡ Versión Mínimo Costo ($0/mes)

| Componente | Tecnología | Costo |
|------------|------------|-------|
| Scripts | Claude API | $0 (free tier) |
| Voz | edge-tts | **$0** |
| Video | MoviePy | $0 |
| Thumbnails | Pillow (código) | $0 |
| Hosting | GitHub Actions | $0 |
| YouTube API | Google | $0 |
| **TOTAL** | | **$0/mes** |

---

## 🚀 Quick Start

### 1. Fork/Clone este repo

### 2. Configurar Secrets en GitHub

Ve a Settings → Secrets and variables → Actions → New repository secret:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
YOUTUBE_REFRESH_TOKEN=1//04...
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
```

### 3. Setup inicial (una vez)

```bash
# Local, para obtener refresh token
python scripts/get_youtube_token.py
```

### 4. Listo

El workflow corre automáticamente cada día a las 9:00 AM UTC.

---

## 📁 Estructura

```
.
├── .github/workflows/daily-short.yml  # Automatización
├── src/
│   ├── fetch_tip.py                   # Obtener tips
│   ├── generate_script.py             # Generar guion
│   ├── generate_voice.py              # edge-tts (GRATIS)
│   ├── generate_thumbnail.py          # Pillow (GRATIS)
│   ├── render_video.py                # MoviePy
│   ├── upload_youtube.py              # Subir video
│   └── moderate_comments.py           # Moderación
├── scripts/
│   └── get_youtube_token.py           # Setup OAuth
├── assets/
│   ├── fonts/                         # Fuentes
│   └── music/                         # Música libre
├── output/                            # Videos (gitignored)
└── requirements.txt
```

---

## 🛠️ Setup Paso a Paso

### Paso 1: Crear Canal YouTube
1. Ve a youtube.com
2. Click en tu avatar → "Crear un canal"
3. Nombre sugerido: "Claude Code Tips ES"
4. Verifica con tu teléfono

### Paso 2: Google Cloud Console
1. Ve a [console.cloud.google.com](https://console.cloud.google.com)
2. Crea nuevo proyecto
3. Ve a "APIs & Services" → "Library"
4. Busca "YouTube Data API v3" → Enable
5. Ve a "Credentials" → "Create Credentials" → "OAuth client ID"
6. Tipo: "Desktop app"
7. Descarga el JSON (client_secret.json)

### Paso 3: Obtener Refresh Token
```bash
pip install google-auth-oauthlib
python scripts/get_youtube_token.py
# Sigue instrucciones, copia el refresh_token
```

### Paso 4: Configurar GitHub Secrets
```
ANTHROPIC_API_KEY=tu_clave_de_anthropic
YOUTUBE_CLIENT_ID=xxxxx.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=GOCSPX-xxxxx
YOUTUBE_REFRESH_TOKEN=1//04xxxxx
```

---

## 📋 Cómo funciona

Cada día a las 9:00 AM UTC:

1. **Fetch**: Obtiene último cambio de CHANGELOG de claude-code
2. **Script**: Claude genera guion viral de 30-45s
3. **Voz**: edge-tts (Microsoft Azure, gratis) genera audio
4. **Thumbnail**: Pillow crea imagen con texto
5. **Video**: MoviePy combina todo en 1080x1920
6. **Upload**: Sube a YouTube como Short
7. **Log**: Guarda métricas

---

## 💡 Tips para éxito

- Publicar a la misma hora ayuda al algoritmo
- Primeros 3 segundos son CRÍTICOS (hook fuerte)
- Hashtags: #claude #claudecode #ai #programacion
- Responder comentarios en las primeras 2 horas

---

## 📊 Métricas esperadas

| Mes | Videos | Subs | Views |
|-----|--------|------|-------|
| 1 | 30 | 100 | 5,000 |
| 3 | 90 | 1,000 | 50,000 |
| 6 | 180 | 5,000 | 200,000 |

---

## 🆘 Soporte

Si algo falla, revisa:
1. GitHub Actions logs
2. Secrets configurados correctamente
3. Cuotas de API no excedidas

---

*Generado automáticamente* 🤖
