#!/usr/bin/env python3
"""
GENERADOR VIDEO FINAL - Usando fuente Roboto REAL
"""
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

Path('output').mkdir(exist_ok=True)
Path('frames_temp').mkdir(exist_ok=True)

FONT_PATH = "fonts/Roboto-Bold.ttf"

# SCRIPT COMPLETO
SCRIPT = """
Imagina poder hablar con todos tus documentos como si fueran personas. 
Hoy te muestro cómo conectar Google Drive con Claude Code.
Tienes cientos de PDFs, informes y contratos. Leerlos todos llevaría días. 
¿Y si pudieras preguntarles directamente qué dicen?
Con Claude Code conectado a Drive, es súper fácil. Solo le dices: 
analiza mis documentos del último trimestre. Y en segundos, obtienes un resumen completo.
Claude extrajo tres insights clave: las ventas subieron un veintitrés por ciento, 
detectó tres contratos que expiran pronto, y recomendó enfocarse en el sector B2B 
donde el retorno de inversión es trescientos cuarenta por ciento.
Todo esto en minutos, no en días. Prueba Claude Code y transforma cómo trabajas con documentos. 
¡Dale like y sígueme para más trucos!
""".strip()

print("="*60)
print("🎬 GENERANDO VIDEO FINAL")
print("="*60)

# 1. GENERAR VOZ
print("\n🎙️ Generando voz...")
os.system(f"""
python3 -c "
import sys
sys.path.insert(0, 'src')
from generate_voice import generate_voice
generate_voice('{SCRIPT}', 'output/final_voice.mp3', voice='es-ES-AlvaroNeural')
"
""")

# 2. GENERAR FRAMES CON FUENTE REAL
print("\n🎨 Generando frames...")

def crear_frame(num, titulo, sub, duracion_segundos=5):
    """Crea múltiples frames para un segmento"""
    frames = []
    img = Image.new('RGB', (1080, 1920), (253, 253, 247))
    draw = ImageDraw.Draw(img)
    
    try:
        font_big = ImageFont.truetype(FONT_PATH, 260)
        font_sub = ImageFont.truetype(FONT_PATH, 90)
        font_num = ImageFont.truetype(FONT_PATH, 50)
    except:
        print("❌ Error fuente")
        return []
    
    # Título
    bbox = draw.textbbox((0,0), titulo, font=font_big)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (1080 - w) // 2
    y = 450
    
    # Outline naranja
    for dx in [-5, -4, -3, 3, 4, 5]:
        for dy in [-5, -4, -3, 3, 4, 5]:
            draw.text((x+dx, y+dy), titulo, font=font_big, fill=(212, 120, 56))
    draw.text((x, y), titulo, font=font_big, fill=(13, 13, 13))
    
    # Subtítulo
    if sub:
        bbox = draw.textbbox((0,0), sub, font=font_sub)
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        x = (1080 - w) // 2
        draw.text((x, y+300), sub, font=font_sub, fill=(212, 120, 56))
    
    # Número
    draw.text((50, 50), f"0{num}", fill=(212, 120, 56), font=font_num)
    
    # Guardar múltiples copias para duración
    for i in range(duracion_segundos * 30):  # 30fps
        path = f"frames_temp/frame_{num:02d}_{i:03d}.jpg"
        img.save(path, quality=95)
        frames.append(path)
    
    return frames

# 5 segmentos de 5 segundos cada uno = 25 segundos total
segmentos = [
    (1, "AHORRA", "40 HORAS", 5),
    (2, "PROBLEMA", "20+ PDFs", 5),
    (3, "SOLUCIÓN", "1 CLICK", 5),
    (4, "RESULTADOS", "+23% Ventas", 5),
    (5, "GRATIS", "PRUEBA YA", 5),
]

all_frames = []
for num, titulo, sub, dur in segmentos:
    frames = crear_frame(num, titulo, sub, dur)
    all_frames.extend(frames)
    print(f"   ✅ Segmento {num}: {titulo} ({len(frames)} frames)")

print(f"\n📊 Total frames: {len(all_frames)}")

# 3. RENDERIZAR VIDEO
print("\n🎬 Renderizando video...")
cmd = """
ffmpeg -y -framerate 30 -i frames_temp/frame_%02d_%03d.jpg \\
-i output/final_voice.mp3 \\
-c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \\
-c:a aac -b:a 192k -shortest \\
output/VIDEO_FINAL.mp4
"""

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# Limpiar frames temporales
import shutil
shutil.rmtree('frames_temp')

if os.path.exists('output/VIDEO_FINAL.mp4') and os.path.getsize('output/VIDEO_FINAL.mp4') > 10000:
    size_mb = os.path.getsize('output/VIDEO_FINAL.mp4') / (1024*1024)
    print(f"\n" + "="*60)
    print("✅ VIDEO FINAL COMPLETADO")
    print("="*60)
    print(f"📁 output/VIDEO_FINAL.mp4")
    print(f"💾 {size_mb:.1f} MB")
    print(f"⏱️  25 segundos (5 segmentos x 5s)")
    print(f"🎨 1080x1920 - Fuente Roboto REAL")
    print("="*60)
else:
    print("❌ Error generando video")
    print(result.stderr[:500])
