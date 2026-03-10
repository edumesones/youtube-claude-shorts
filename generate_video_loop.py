#!/usr/bin/env python3
"""
GENERADOR DE VIDEO - MODO LOOP
No para hasta generar el video completo.
"""
import os
import sys
import subprocess
from pathlib import Path

# Asegurar directorio
Path('output').mkdir(exist_ok=True)

audio_path = "output/mentoria_voice.mp3"
output_path = "output/video_final.mp4"

print("="*60)
print("🎬 GENERANDO VIDEO - MODO LOOP")
print("="*60)

# Verificar audio existe
if not os.path.exists(audio_path):
    print("❌ No existe audio. Generando...")
    sys.exit(1)

# MÉTODO 1: FFmpeg simple (imagen estática + audio)
print("\n📹 Método 1: FFmpeg con imagen...")

try:
    # Crear imagen simple con ImageMagick si existe, sino usar color
    img_cmd = "convert -size 1080x1920 xc:darkblue -pointsize 60 -fill white -gravity center -annotate +0+0 'MENTORÍA CON\nCLAUDE CODE' output/temp_bg.jpg"
    subprocess.run(img_cmd, shell=True, capture_output=True)
    
    if os.path.exists("output/temp_bg.jpg"):
        # Usar imagen generada
        cmd = f"""
        ffmpeg -y -loop 1 -i output/temp_bg.jpg -i {audio_path} \
        -c:v libx264 -preset ultrafast -tune stillimage \
        -c:a aac -b:a 192k -shortest -pix_fmt yuv420p \
        {output_path}
        """
    else:
        # Usar color sólido
        cmd = f"""
        ffmpeg -y -f lavfi -i color=c=darkblue:s=1080x1920:d=22 \
        -i {audio_path} -c:v libx264 -preset ultrafast \
        -c:a aac -shortest {output_path}
        """
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
        size_mb = os.path.getsize(output_path) / (1024*1024)
        print(f"✅ ÉXITO! Video generado: {size_mb:.1f} MB")
        print(f"📁 {output_path}")
        
        # Info del video
        probe = subprocess.run(
            f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {output_path}",
            shell=True, capture_output=True, text=True
        )
        duration = float(probe.stdout.strip()) if probe.returncode == 0 else 0
        print(f"⏱️  Duración: {duration:.1f} segundos")
        
        sys.exit(0)
    else:
        print(f"❌ Falló método 1")
        print(result.stderr[:500])
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n❌ Todos los métodos fallaron")
sys.exit(1)
