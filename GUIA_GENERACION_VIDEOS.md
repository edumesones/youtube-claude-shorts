# 📚 GUÍA COMPLETA - Generación de YouTube Shorts con Voz Clonada

> Basado en el proyecto de Edu Mesones - Marzo 2026

---

## 🎯 CONFIGURACIÓN ELEVENLABS

### API Key
```
sk_2ed6c7ddd2ead25e9e0510e3be0b6c613c4b9f0ff5966bc0
```

### Voice ID Correcto
| Voz | ID |
|-----|-----|
| edus (Edu Mesones) | `DJqL9GvhCdRJNarEEzXU` |

⚠️ **IMPORTANTE:** El nombre "edus" NO funciona, usar siempre el ID completo.

### Configuración Óptima para Voz Natural
```python
{
    "model_id": "eleven_multilingual_v2",  # Más natural que flash
    "voice_settings": {
        "stability": 0.35,        # Menos robótico
        "similarity_boost": 0.65, # Balance similitud
        "style": 0.10,            # Ligero estilo
        "use_speaker_boost": True
    }
}
```

---

## 📝 TÉCNICAS DE GUION PARA VOZ NATURAL

### 1. Pausas y Respiración
```python
# Usar puntos suspensivos (...) para pausas de pensamiento
# Usar guiones largos (—) para respirar
# Usar saltos de línea (\n\n) para pausas largas

texto = """Voy a analizar... estos documentos.

Primero — los reviso uno por uno."""
```

### 2. Énfasis
```python
# MAYÚSCULAS para énfasis
# "comillas" para destacar conceptos
# Signos ¿? y ¡! para variación de tono (aunque no sea pregunta real)

texto = "El resultado es INCREÍBLE. ¿Lo ves? ¡Aquí está!"
```

### 3. Ejemplo de Guion Óptimo
```python
"""Voy a analizar... estos cinco PDFs financieros.

Primero — los listo... luego ejecuto el análisis con Claude.

¿El resultado? En segundos... extrae TODAS las métricas clave.

¡Y aquí está! El reporte completo... listo para revisar."""
```

---

## 🎨 ESPECIFICACIONES TÉCNICAS DE VIDEO

### Canvas
- **Resolución:** 1080x1920 (9:16 vertical)
- **FPS:** 30
- **Formato:** MP4 (H.264)

### Colores Claude
```python
CLAW_ORANGE = (230, 100, 30)  # #E6643E
DARK_BG = (13, 13, 13)
TERMINAL_BG = (30, 30, 30)
```

### Fuentes
- **Título:** Roboto Bold (descargar, no usar sistema)
- **Terminal:** Roboto Bold (mismo archivo)
- **Tamaños:** 200px títulos, 80px subtítulos, 32px terminal

### Estructura de Video Recomendada
```
[1s] Silencio inicial (hook visual)
[2s] Intro/Hola
[3s] Problema
[4s] Solución  
[3s] Demo/Resultado
[8s] PDF/Reporte final con scroll
```

---

## 🖥️ ESTRUCTURA DE ESCENAS

### Versión TÉCNICA (desarrolladores)
```
$ claude
$ ls *.pdf
$ /analyze
$ open reporte.pdf
```

### Versión NO TÉCNICA (público general)
```
"Hola, soy Claude..."
"Aquí tengo 5 documentos..."
"Voy a analizarlos automáticamente..."
"¡Listo! Aquí está el informe..."
```

---

## 📊 PDF FINAL - Elementos Visuales

### KPIs en Cajas
- Ventas: +23%
- Clientes: 156
- Retención: 92%

### Gráficos
1. **Barras:** Crecimiento trimestral (Q1-Q4)
2. **Circular:** Distribución de ingresos (SaaS, Servicios, Otros)
3. **Alertas:** Iconos de warning

### Contenido del Reporte
```
1. MÉTRICAS PRINCIPALES
2. CRECIMIENTO POR TRIMESTRE [GRÁFICO]
3. DISTRIBUCIÓN DE INGRESOS [GRÁFICO]
4. ALERTAS DETECTADAS
5. RECOMENDACIONES
```

---

## 🛠️ HERRAMIENTAS

### Stack Actual
| Herramienta | Uso |
|-------------|-----|
| Python + Pillow | Generar frames |
| FFmpeg | Renderizar video |
| ElevenLabs API | Voz clonada |
| edge-tts | Voz alternativa (gratis) |

### Alternativa: Remotion
**¿Qué es?** Librería de React para generar videos con código

**Pros:**
- Animaciones más fluidas (CSS/React)
- Componentes reutilizables
- Preview en tiempo real
- Mejor para complejos

**Contras:**
- Requiere conocimiento de React
- Más pesado que Python puro
- Necesita Node.js

**¿Cuándo usar Remotion?**
- ✅ Animaciones complejas con muchos elementos
- ✅ Necesitas preview antes de renderizar
- ✅ Quieres reusar componentes entre videos
- ❌ Videos simples (Python es más rápido)

**Veredicto:** Para el caso actual (terminal + PDF scroll), Python es suficiente. Si quieres animaciones tipo "after effects" complejas, Remotion sería mejor.

---

## 🔧 COMANDOS ÚTILES

### Verificar audio generado
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio.mp3
```

### Unir silencio + audio
```bash
ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t 1 -acodec libmp3lame silence.mp3
ffmpeg -y -i 'concat:silence.mp3|audio.mp3' -acodec copy final.mp3
```

### Renderizar video
```bash
ffmpeg -y -framerate 30 -i frame_%04d.jpg -i audio.mp3 \
       -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output.mp4
```

---

## ⚠️ ERRORES COMUNES Y SOLUCIONES

### "Voz no suena como la original"
**Causa:** Voice ID incorrecto
**Solución:** Usar `DJqL9GvhCdRJNarEEzXU`, no "edus"

### "Error ElevenLabs, usando alternativa"
**Causas:**
- API key no configurada
- Límite de caracteres excedido
- Voice ID incorrecto

### "Font not found"
**Solución:** Descargar Roboto-Bold.ttf en carpeta `fonts/`

---

## 🚀 FLUJO DE TRABAJO RECOMENDADO

1. **Escribir guion** con técnicas de pausas/énfasis
2. **Generar audio** con ElevenLabs
3. **Verificar audio** suena bien
4. **Generar frames** sincronizados con duración del audio
5. **Renderizar** con FFmpeg
6. **Revisar** y ajustar si es necesario
7. **Subir** a YouTube

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
youtube-claude-shorts/
├── fonts/
│   └── Roboto-Bold.ttf
├── src/
│   ├── generate_voice.py
│   └── render_video.py
├── output/
│   └── (videos finales)
├── generar_voz_natural.py
├── render_final_graficos.py
└── README.md
```

---

## 💡 TIPS PARA VIDEOS VIRALES

1. **Hook en los primeros 3 segundos**
2. **Silencio inicial** para que el algoritmo de YouTube capture bien el audio
3. **Texto grande** y contrastado
4. **Cortes rápidos** mantienen atención
5. **CTA claro** al final
6. **PDF/reporte final** que scrollee = prueba de valor

---

## 🔮 PRÓXIMOS PASOS / IDEAS

- [ ] Sistema automático: GitHub Action que genere video diario
- [ ] Templates parametrizables (cambiar solo texto)
- [ ] Añadir música de fondo (libre de derechos)
- [ ] Subtítulos incrustados (SRT -> burn in)
- [ ] Variantes A/B para testing

---

*Documento vivo - actualizar con nuevos aprendizajes*
