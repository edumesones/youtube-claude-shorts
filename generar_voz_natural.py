#!/usr/bin/env python3
"""
GENERAR VOZ EDU v2 - Guion mejorado con pausas y énfasis natural
"""
import requests

API_KEY = 'sk_2ed6c7ddd2ead25e9e0510e3be0b6c613c4b9f0ff5966bc0'
VOICE_ID = 'DJqL9GvhCdRJNarEEzXU'

# GUION MEJORADO - Con pausas, énfasis y tono natural
# Técnicas aplicadas:
# - Puntos suspensivos (...) para pausas de pensamiento
# - Guiones largos (—) para respirar
# - MAYÚSCULAS para énfasis
# - Signos forzados para variación de tono

texto_mejorado = """Voy a analizar... estos cinco PDFs financieros.

Primero — los listo... luego ejecuto el análisis con Claude.

¿El resultado? En segundos... extrae TODAS las métricas clave.

¡Y aquí está! El reporte completo... listo para revisar."""

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

# Configuración optimizada para naturalidad
data = {
    "text": texto_mejorado,
    "model_id": "eleven_flash_v2_5",  # Probar modelo más natural
    "voice_settings": {
        "stability": 0.35,        # Menor = más expresivo
        "similarity_boost": 0.85,  # Mantener similitud a voz
        "style": 0.4,             # Añadir estilo/expressividad
        "use_speaker_boost": True
    }
}

print("🎙️ Generando voz Edu NATURAL...")
print("⚙️  Modelo: eleven_flash_v2_5")
print("⚙️  Stability: 0.35 (más expresivo)")
print("⚙️  Similarity: 0.85")
print()

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    with open('demo_v2_output/audio_edu_natural.mp3', 'wb') as f:
        f.write(response.content)
    print(f"✅ Audio generado: {len(response.content)} bytes")
    print("📁 Guardado: demo_v2_output/audio_edu_natural.mp3")
    
    # Guardar guion usado
    with open('demo_v2_output/guion_natural.txt', 'w') as f:
        f.write(texto_mejorado)
    print("📝 Guion guardado: demo_v2_output/guion_natural.txt")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text[:500])
