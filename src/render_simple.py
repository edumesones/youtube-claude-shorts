"""
Renderiza video usando PIL + OpenCV (sin dependencias complejas).
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import os


def create_frame(text, width=1080, height=1920, bg_color=(26, 26, 46)):
    """Crea un frame con texto."""
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Intentar cargar fuente
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = font_large
    
    # Texto principal (centrado)
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = height // 2 - 100
    
    # Contorno negro
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx != 0 or dy != 0:
                draw.text((x+dx, y+dy), text, font=font_large, fill=(0, 0, 0))
    
    # Texto blanco
    draw.text((x, y), text, font=font_large, fill=(255, 255, 255))
    
    # Watermark
    draw.text((20, 20), "@ClaudeTipsES", font=font_small, fill=(200, 200, 200))
    
    return np.array(img)


def render_simple_video(
    audio_path: str,
    output_path: str = "output/mentoria_video_final.mp4",
    duration: float = 22.0
):
    """
    Renderiza video simple con frames estáticos + audio.
    """
    print("🎬 Generando video con OpenCV...")
    
    fps = 30
    width, height = 1080, 1920
    
    # Crear video temporal (sin audio)
    temp_video = "output/temp_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
    
    # Generar frames
    text = "MENTORÍA CON\nCLAUDE CODE"
    frame = create_frame(text)
    
    num_frames = int(fps * duration)
    for i in range(num_frames):
        # Convertir RGB a BGR para OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
        
        if i % 30 == 0:
            print(f"   Frame {i}/{num_frames}")
    
    out.release()
    
    # Combinar con audio usando ffmpeg
    print("🎵 Añadiendo audio...")
    cmd = [
        'ffmpeg', '-y',
        '-i', temp_video,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Limpiar temp
    if os.path.exists(temp_video):
        os.remove(temp_video)
    
    if result.returncode == 0:
        print(f"✅ Video final: {output_path}")
        return True
    else:
        print(f"❌ Error: {result.stderr[:200]}")
        return False


if __name__ == "__main__":
    render_simple_video("output/mentoria_voice.mp3")
