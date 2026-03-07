"""
Renderiza videos con FFmpeg directo (más rápido y estable que MoviePy).
"""
import subprocess
import os
from typing import List


def render_with_ffmpeg(
    audio_path: str,
    output_path: str = "output/video.mp4",
    text_overlay: str = "CLAUDE CODE MENTORIA"
) -> bool:
    """
    Renderiza video usando FFmpeg directamente.
    Más rápido y estable que MoviePy.
    """
    try:
        print("🎬 Renderizando con FFmpeg...")
        
        # Crear un video de color con texto usando FFmpeg
        # Fondo degradado azul-morado
        cmd = [
            'ffmpeg',
            '-y',  # Sobrescribir
            '-f', 'lavfi',
            '-i', 'color=c=#1a1a2e:s=1080x1920:d=22',  # Fondo azul oscuro, 22 segundos
            '-i', audio_path,  # Audio
            '-vf', 
            f'drawtext=text=\'{text_overlay}\':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,'
            f'drawtext=text=@ClaudeTipsES:fontcolor=white:fontsize=40:x=20:y=20',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"✅ Video generado: {output_path}")
            return True
        else:
            print(f"❌ Error FFmpeg: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    # Test
    render_with_ffmpeg("output/mentoria_voice.mp3")
