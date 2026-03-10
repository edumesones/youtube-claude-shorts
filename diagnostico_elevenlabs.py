#!/usr/bin/env python3
"""
DIAGNÓSTICO ElevenLabs - Verificar API key y voz 'edus'
"""
import requests
import os

API_KEY = 'sk_2ed6c7ddd2ead25e9e0510e3be0b6c613c4b9f0ff5966bc0'
VOICE_ID = 'edus'

print("="*60)
print("🔍 DIAGNÓSTICO ELEVENLABS")
print("="*60)

# 1. Verificar API key
print("\n1. Verificando API key...")
headers = {"xi-api-key": API_KEY}
response = requests.get("https://api.elevenlabs.io/v1/user", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   ✅ API key válida")
    print(f"   📧 Usuario: {data.get('email', 'N/A')}")
    print(f"   📊 Tier: {data.get('subscription', {}).get('tier', 'N/A')}")
else:
    print(f"   ❌ Error: {response.text[:200]}")

# 2. Listar voces disponibles
print("\n2. Listando voces disponibles...")
response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
if response.status_code == 200:
    voices = response.json().get('voices', [])
    print(f"   Total voces: {len(voices)}")
    print("\n   Voces:")
    for v in voices:
        vid = v.get('voice_id', '')
        name = v.get('name', '')
        marker = " ⭐ TU VOZ" if vid == VOICE_ID else ""
        print(f"   - {vid}: {name}{marker}")
else:
    print(f"   ❌ Error: {response.text[:200]}")

# 3. Verificar voz específica 'edus'
print(f"\n3. Verificando voz '{VOICE_ID}'...")
response = requests.get(f"https://api.elevenlabs.io/v1/voices/{VOICE_ID}", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    voice_data = response.json()
    print(f"   ✅ Voz encontrada")
    print(f"   📛 Nombre: {voice_data.get('name', 'N/A')}")
    print(f"   📝 Descripción: {voice_data.get('description', 'N/A')}")
    print(f"   🏷️  Labels: {voice_data.get('labels', {})}")
else:
    print(f"   ❌ Error: {response.text[:200]}")

# 4. Probar generación de voz simple
print(f"\n4. Probando generación de voz...")
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}
data = {
    "text": "Hola, esto es una prueba",
    "model_id": "eleven_multilingual_v2",
}

response = requests.post(url, json=data, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✅ Voz generada correctamente")
    print(f"   📦 Tamaño: {len(response.content)} bytes")
    # Guardar para verificar
    with open('test_voz_edu.mp3', 'wb') as f:
        f.write(response.content)
    print(f"   💾 Guardado: test_voz_edu.mp3")
else:
    print(f"   ❌ Error: {response.text[:500]}")

print("\n" + "="*60)
print("DIAGNÓSTICO COMPLETADO")
print("="*60)
