#!/usr/bin/env python3
"""
VIDEO SIMPLIFICADO - Método confiable
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

os.makedirs('output', exist_ok=True)
os.makedirs('final_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"

# Generar frames uno por uno
colors = {
    1: (230, 100, 30),  # Naranja
    2: (200, 50, 50),   # Rojo
    3: (50, 150, 50),   # Verde
    4: (50, 100, 200),  # Azul
    5: (212, 120, 56),  # Naranja Claude
}

texts = {
    1: ("AHORRA", "40 HORAS"),
    2: ("PROBLEMA", "20+ PDFs"),
    3: ("SOLUCIÓN", "1 CLICK"),
    4: ("RESULTADOS", "+23%"),
    5: ("GRATIS", "PRUEBA YA"),
}

print("🎬 Generando frames...")
frame_count = 0

for seg in range(1, 6):
    color = colors[seg]
    title, sub = texts[seg]
    
    for frame in range(150):  # 5 segundos
        # Crear imagen con fondo de color
        img = Image.new('RGB', (1080, 1920), color)
        draw = ImageDraw.Draw(img)
        
        try:
            font_big = ImageFont.truetype(FONT, 200)
            font_sub = ImageFont.truetype(FONT, 80)
        except:
            font_big = font_sub = ImageFont.load_default()
        
        # Título blanco grande
        bbox = draw.textbbox((0,0), title, font=font_big)
        w = bbox[2] - bbox[0]
        draw.text(((1080-w)//2, 600), title, fill=(255,255,255), font=font_big)
        
        # Subtítulo
        bbox = draw.textbbox((0,0), sub, font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text(((1080-w)//2, 900), sub, fill=(255,255,255), font=font_sub)
        
        # Guardar
        img.save(f"final_frames/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1
        
        if frame_count % 50 == 0:
            print(f"   {frame_count} frames...")

print(f"✅ {frame_count} frames generados")

# Renderizar video
print("\n🎬 Renderizando video...")
cmd = "ffmpeg -y -framerate 30 -i final_frames/frame_%04d.jpg -i output/voz_final.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output/VIDEO_LISTO.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

if os.path.exists('output/VIDEO_LISTO.mp4'):
    size = os.path.getsize('output/VIDEO_LISTO.mp4') / (1024*1024)
    print(f"\n✅ VIDEO LISTO: {size:.1f} MB")
    print("📁 output/VIDEO_LISTO.mp4")
else:
    print("❌ Error")

# Limpiar
import shutil
shutil.rmtree('final_frames')
