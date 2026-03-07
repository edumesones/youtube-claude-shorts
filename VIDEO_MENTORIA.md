# 🎬 VIDEO DE MENTORÍA - INSTRUCCIONES

## ✅ ¿Qué he creado?

He construido un sistema completo que genera videos de YouTube Shorts sobre **mentoría con Claude Code**.

### Archivos creados:

```
youtube-claude-shorts/
├── src/
│   ├── fetch_tip.py              # Obtener tips de GitHub
│   ├── generate_script.py        # Generar guiones con Claude
│   ├── generate_voice.py         # TTS gratis (edge-tts)
│   ├── generate_thumbnail.py     # Thumbnails con Pillow
│   ├── render_video.py           # Render con MoviePy
│   └── upload_youtube.py         # Subir a YouTube
├── scripts/
│   └── get_youtube_token.py      # Setup OAuth
├── .github/workflows/
│   ├── daily-short.yml           # Automatización diaria
│   └── create-mentoria.yml       # Generar video mentoría
├── create_mentoria_video.py      # Script específico mentoría
├── requirements.txt              # Dependencias
└── README.md                     # Documentación
```

---

## 🚀 CÓMO GENERAR EL VIDEO (2 opciones)

### Opción A: GitHub Actions (Recomendada - Yo lo hago)

1. **Sube este repo a GitHub**
2. **Ve a Actions → "Create Mentoria Video" → Run workflow**
3. **Descarga el video** desde los artifacts (en ~5 minutos)

### Opción B: Local (Tú lo ejecutas)

```bash
# 1. Clonar/entrar al repo
cd youtube-claude-shorts

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Instalar ffmpeg
# Ubuntu/Debian: sudo apt-get install ffmpeg
# Mac: brew install ffmpeg
# Windows: descargar de ffmpeg.org

# 4. Ejecutar
python create_mentoria_video.py

# 5. El video estará en: output/mentoria_video.mp4
```

---

## 📋 CONTENIDO DEL VIDEO

**Título:** "Cómo mentorizo con Claude Code 🤖"

**Duración:** ~40 segundos

**Script:**
1. [0:00-0:05] Así enseño programación en 2025.
2. [0:05-0:15] Antes, revisar código de estudiantes me tomaba horas.
3. [0:15-0:28] Ahora, Claude Code analiza el código, detecta errores y explica las soluciones paso a paso.
4. [0:28-0:38] Es como tener un mentor experto disponible 24 horas al día.
5. [0:38-0:42] Sígueme para más técnicas de productividad.

**Voz:** es-ES-AlvaroNeural (gratis via edge-tts)
**Estilo visual:** Fondo degradado oscuro + texto animado

---

## 🎙️ CÓMO REEMPLAZAR CON TU VOZ

Una vez tengas el video base:

### Opción 1: Reemplazar audio completo
```bash
# Graba tu voz diciendo el mismo script
# Guarda como: mi_voz.mp3

# Luego usa ffmpeg:
ffmpeg -i output/mentoria_video.mp4 -i mi_voz.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest video_final.mp4
```

### Opción 2: Edición con tu software preferido
1. Abre `output/mentoria_video.mp4` en CapCut/Premiere/etc
2. Silencia la pista de audio
3. Añade tu grabación de voz
4. Exporta

---

## 💰 COSTO TOTAL

| Componente | Costo |
|------------|-------|
| Generación de video | **$0.00** |
| Voz (edge-tts) | **$0.00** |
| Thumbnail (Pillow) | **$0.00** |
| Render (MoviePy) | **$0.00** |
| **TOTAL** | **$0.00** |

---

## 📦 PRÓXIMOS PASOS

1. ✅ **Generar video** (ejecuta el script o Actions)
2. ⏳ **Revisar** el resultado
3. 🔊 **Reemplazar voz** con tu audio
4. 📺 **Subir a YouTube** (configura credenciales)
5. 🚀 **Automatizar** para videos diarios

---

## 🆘 SOPORTE

Si algo falla, revisa:
- Tienes ffmpeg instalado: `ffmpeg -version`
- Python 3.11+: `python --version`
- Dependencias instaladas: `pip list | grep moviepy`

---

¿**Ejecutamos** el workflow de GitHub Actions ahora para generar el video?
