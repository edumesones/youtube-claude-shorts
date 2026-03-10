"""
Genera voz usando edge-tts (Microsoft Azure Edge, GRATIS).
Versión: $0 - Usa los servidores TTS de Microsoft Edge
"""
import asyncio
import edge_tts
import os
from typing import Optional

# Voces en español disponibles (gratis)
SPANISH_VOICES = {
    'es-es': 'es-ES-AlvaroNeural',      # Masculino, español de España
    'es-mx': 'es-MX-JorgeNeural',       # Masculino, español de México
    'es-ar': 'es-AR-TomasNeural',       # Masculino, español de Argentina
    'es-co': 'es-CO-GonzaloNeural',     # Masculino, español de Colombia
    'es-es-f': 'es-ES-ElviraNeural',    # Femenino, español de España
    'es-mx-f': 'es-MX-DaliaNeural',     # Femenino, español de México
}

DEFAULT_VOICE = 'es-ES-AlvaroNeural'  # Buena calidad, neutro


async def generate_voice_async(text: str, output_path: str, voice: str = None) -> bool:
    """
    Genera archivo de audio MP3 desde texto.
    
    Args:
        text: Texto a convertir
        output_path: Ruta de salida (ej: "output/voice.mp3")
        voice: ID de voz (ver SPANISH_VOICES)
    
    Returns:
        True si exitoso
    """
    try:
        voice = voice or DEFAULT_VOICE
        
        # edge-tts es completamente gratuito
        # Usa los servidores de Microsoft Edge
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
        print(f"✅ Voz generada: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generando voz: {e}")
        return False


def generate_voice(text: str, output_path: str, voice: str = None) -> bool:
    """
    Wrapper síncrono para generate_voice_async.
    """
    return asyncio.run(generate_voice_async(text, output_path, voice))


async def list_voices():
    """
    Lista todas las voces disponibles.
    Útil para debugging.
    """
    voices = await edge_tts.list_voices()
    
    print("🎙️ Voces en español disponibles:")
    for voice in voices:
        if voice['Locale'].startswith('es'):
            print(f"   {voice['ShortName']} - {voice['Locale']}")


def get_voice_duration(audio_path: str) -> float:
    """
    Obtiene la duración del audio en segundos.
    Requiere ffprobe (viene con ffmpeg).
    """
    try:
        from moviepy.editor import AudioFileClip
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        return duration
    except Exception as e:
        print(f"⚠️ No se pudo obtener duración: {e}")
        return 0.0


if __name__ == "__main__":
    # Test
    test_text = "¿Sabías que Claude Code ahora es más rápido? La última actualización arregla un problema con el cache. ¡Actualiza ahora!"
    
    # Crear directorio si no existe
    os.makedirs("output", exist_ok=True)
    
    # Generar voz
    success = generate_voice(test_text, "output/test_voice.mp3")
    
    if success:
        duration = get_voice_duration("output/test_voice.mp3")
        print(f"✅ Audio generado: {duration:.1f} segundos")
        print(f"💰 Costo: $0.00 (edge-tts es gratis)")
    else:
        print("❌ Falló la generación")
    
    # Opcional: listar voces
    # asyncio.run(list_voices())
