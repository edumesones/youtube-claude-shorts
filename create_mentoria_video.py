"""
Genera un video completo de mentoría con Claude Code.
Ejecutar: python create_mentoria_video.py
"""
import asyncio
import os
import sys
from pathlib import Path

# Asegurar que src está en path
sys.path.insert(0, 'src')

from generate_voice import generate_voice
from generate_thumbnail import generate_thumbnail
from render_video import render_short_video, get_video_info


def main():
    """Genera video de mentoría Claude Code."""
    
    print("=" * 60)
    print("🎬 CREANDO VIDEO: Mentoría con Claude Code")
    print("=" * 60)
    
    # Crear directorios
    Path('output').mkdir(exist_ok=True)
    
    # DATOS DEL VIDEO
    title = "Cómo mentorizo con Claude Code 🤖"
    
    # SCRIPT EN CASTELLANO (30-40 segundos)
    script_sections = [
        "[0:00-0:05] Así enseño programación en 2025.",
        "[0:05-0:15] Antes, revisar código de estudiantes me tomaba horas.",
        "[0:15-0:28] Ahora, Claude Code analiza el código, detecta errores y explica las soluciones paso a paso.",
        "[0:28-0:38] Es como tener un mentor experto disponible 24 horas al día.",
        "[0:38-0:42] Sígueme para más técnicas de productividad."
    ]
    
    full_script = " ".join([s.split(']', 1)[1].strip() for s in script_sections])
    
    print(f"\n📝 Script ({len(full_script)} caracteres):")
    for section in script_sections:
        print(f"   {section}")
    
    # 1. GENERAR VOZ
    print("\n🎙️ Generando voz (edge-tts)...")
    audio_path = "output/mentoria_voice.mp3"
    
    success = generate_voice(full_script, audio_path, voice='es-ES-AlvaroNeural')
    if not success:
        print("❌ Falló generación de voz")
        return False
    
    print(f"   ✅ Audio guardado: {audio_path}")
    
    # 2. GENERAR THUMBNAIL
    print("\n🎨 Generando thumbnail...")
    thumbnail_path = "output/mentoria_thumbnail.jpg"
    
    success = generate_thumbnail(
        title="MENTORÍA CON CLAUDE CODE",
        subtitle="Mi flujo de trabajo 2025",
        output_path=thumbnail_path,
        style="dark"
    )
    if not success:
        print("⚠️ Falló thumbnail, continuando...")
        thumbnail_path = None
    else:
        print(f"   ✅ Thumbnail: {thumbnail_path}")
    
    # 3. RENDERIZAR VIDEO
    print("\n🎬 Renderizando video...")
    video_path = "output/mentoria_video.mp4"
    
    success = render_short_video(
        audio_path=audio_path,
        script_sections=script_sections,
        thumbnail_path=thumbnail_path,
        output_path=video_path,
        add_subtitles=True
    )
    
    if not success:
        print("❌ Falló renderizado")
        return False
    
    # 4. INFO FINAL
    print("\n" + "=" * 60)
    print("✅ VIDEO COMPLETADO")
    print("=" * 60)
    
    video_info = get_video_info(video_path)
    if video_info:
        print(f"\n📁 Archivo: {video_path}")
        print(f"⏱️  Duración: {video_info['duration']:.1f} segundos")
        print(f"📐 Resolución: {video_info['size'][0]}x{video_info['size'][1]}")
        print(f"💾 Tamaño: {video_info['file_size_mb']:.1f} MB")
    
    print(f"\n🎙️  Audio: {audio_path}")
    print(f"🖼️  Thumbnail: {thumbnail_path}")
    
    print("\n" + "=" * 60)
    print("📝 NOTA: Este video usa voz TTS de prueba.")
    print("   Para usar tu voz real:")
    print("   1. Reemplaza 'output/mentoria_voice.mp3' con tu audio")
    print("   2. Vuelve a ejecutar render_short_video()")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
