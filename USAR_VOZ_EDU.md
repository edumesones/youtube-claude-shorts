# 🎙️ USAR VIDEO CON TU VOZ EDU

## ⚠️ IMPORTANTE - Seguridad

**NUNCA subas tu API key al repo.** 

La uso así:

## Paso 1: Exportar API key (solo en tu terminal)

```bash
export ELEVENLABS_API_KEY='sk_2ed6c7ddd2ead25e9e0510e3be0b6c613c4b9f0ff5966bc0'
```

## Paso 2: Ejecutar generador

```bash
cd youtube-claude-shorts
python3 video_con_voz_edu.py
```

## ¿Qué hace el script?

1. **Genera audio** con tu voz "edus" via ElevenLabs API
2. **Crea frames** sincronizados con ese audio
3. **Renderiza video** final con tu voz

## Output

📁 `output/VIDEO_VOZ_EDU.mp4`

## Si no quieres exponer la API key

Puedo crear un **GitHub Actions workflow** que:
- Use el secreto `ELEVENLABS_API_KEY` (configurado en Settings > Secrets)
- Genere el video automáticamente
- Suba el resultado

¿Prefieres ejecutarlo local o con GitHub Actions?
