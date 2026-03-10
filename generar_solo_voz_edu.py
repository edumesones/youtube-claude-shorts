#!/usr/bin/env python3
"""
GENERAR VOZ EDU - Script directo con API key
"""
import requests

API_KEY = 'sk_2ed6c7ddd2ead25e9e0510e3be0b6c613c4b9f0ff5966bc0'
VOICE_ID = 'DJqL9GvhCdRJNarEEzXU'

texto = "Voy a analizar estos cinco PDFs financieros. Primero los listo, luego ejecuto el análisis con Claude. En segundos, extrae todas las métricas. Y aquí está el reporte completo, listo para revisar."

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}
data = {
    "text": texto,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.9  # Aumentar similitud a tu voz
    }
}

print("🎙️ Generando voz con Edu...")
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    with open('demo_v2_output/audio_edu_real.mp3', 'wb') as f:
        f.write(response.content)
    print(f"✅ Audio generado: {len(response.content)} bytes")
    print("📁 Guardado: demo_v2_output/audio_edu_real.mp3")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text[:500])
