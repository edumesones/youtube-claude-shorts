#!/usr/bin/env python3
"""
VIDEO FINAL V7 - Enriquecido + Fuente Roboto REAL + Tamaños correctos
"""
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil

Path('output').mkdir(exist_ok=True)
Path('frames_final').mkdir(exist_ok=True)

FONT_PATH = "fonts/Roboto-Bold.ttf"

# COLORES
ORANGE = (230, 100, 30)
WHITE = (255, 255, 255)
BLACK = (13, 13, 13)
GRAY = (100, 100, 100)
BG = (253, 253, 247)

def crear_frame_enriquecido(numero, titulo, metrica_numero, metrica_texto, datos):
    """Frame con MUCHO contenido visual"""
    W, H = 1080, 1920
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    
    try:
        font_titulo = ImageFont.truetype(FONT_PATH, 180)
        font_numero = ImageFont.truetype(FONT_PATH, 300)
        font_med = ImageFont.truetype(FONT_PATH, 70)
        font_small = ImageFont.truetype(FONT_PATH, 50)
    except:
        print("❌ Error fuente")
        return []
    
    # HEADER: Número de segmento
    draw.text((50, 50), f"0{numero}", fill=ORANGE, font=font_med)
    draw.line([(50, 140), (200, 140)], fill=ORANGE, width=5)
    
    # TÍTULO PRINCIPAL (grande, arriba)
    words = titulo.split()[:2]
    y = 250
    for word in words:
        bbox = draw.textbbox((0,0), word, font=font_titulo)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        # Outline
        for dx in [-4, -3, 3, 4]:
            for dy in [-4, -3, 3, 4]:
                draw.text((x+dx, y+dy), word, font=font_titulo, fill=ORANGE)
        draw.text((x, y), word, font=font_titulo, fill=BLACK)
        y += 200
    
    # MÉTRICA NUMÉRICA GIGANTE (centro)
    bbox = draw.textbbox((0,0), metrica_numero, font=font_numero)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    y_num = 750
    # Caja de fondo naranja
    draw.rounded_rectangle([x-40, y_num-40, x+w+40, y_num+250], radius=30, fill=ORANGE)
    draw.text((x, y_num), metrica_numero, font=font_numero, fill=WHITE)
    
    # Texto debajo del número
    bbox = draw.textbbox((0,0), metrica_texto, font=font_med)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    draw.text((x, y_num+280), metrica_texto, font=font_med, fill=GRAY)
    
    # DATOS/BADGES (abajo)
    y_datos = 1300
    for i, dato in enumerate(datos[:3]):
        x_pos = 80 + (i * 340)
        draw.rounded_rectangle([x_pos, y_datos, x_pos+300, y_datos+100], radius=15, fill=ORANGE)
        bbox = draw.textbbox((0,0), dato, font=font_small)
        w = bbox[2] - bbox[0]
        draw.text((x_pos + (300-w)//2, y_datos+25), dato, font=font_small, fill=WHITE)
    
    # FOOTER
    draw.text((80, 1800), "Claude + Drive", fill=ORANGE, font=font_med)
    
    # Generar múltiples frames para duración
    frames = []
    for i in range(150):  # 5 segundos a 30fps
        path = f"frames_final/frame_{numero:02d}_{i:03d}.jpg"
        img.save(path, quality=95)
        frames.append(path)
    
    return frames

print("="*60)
print("🎬 VIDEO FINAL V7 - Enriquecido + Roboto REAL")
print("="*60)

# GENERAR FRAMES
print("\n🎨 Generando frames enriquecidos...")

segmentos = [
    (1, "AHORRA", "40h", "horas ahoradas", ["Automático", "Rápido", "Gratis"]),
    (2, "EL PROBLEMA", "20+", "documentos sin leer", ["PDFs", "Informes", "Contratos"]),
    (3, "SOLUCIÓN", "1", "solo click", ["Conectar", "Analizar", "Listo"]),
    (4, "RESULTADOS", "+23%", "más ventas", ["Insights", "Acciones", "Rápido"]),
    (5, "GRATIS", "$0", "costo total", ["Prueba", "Suscríbete", "Comparte"]),
]

all_frames = []
for num, tit, num_metric, txt_metric, datos in segmentos:
    frames = crear_frame_enriquecido(num, tit, num_metric, txt_metric, datos)
    all_frames.extend(frames)
    print(f"   ✅ Segmento {num}: {tit} ({len(frames)} frames)")

print(f"\n📊 Total: {len(all_frames)} frames")

# GENERAR VOZ
print("\n🎙️ Generando voz...")
from src.generate_voice import generate_voice
script = "Hoy te muestro cómo ahorrar 40 horas semanales con Claude Code y Google Drive. Tienes 20 documentos sin analizar. La solución es un solo click. Obtén resultados como más ventas y todo es completamente gratis. Prueba ahora."
generate_voice(script, "output/voz_final.mp3")

# RENDERIZAR VIDEO
print("\n🎬 Renderizando video final...")
cmd = "ffmpeg -y -framerate 30 -i frames_final/frame_%02d_%03d.jpg -i output/voz_final.mp3 -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -c:a aac -shortest output/VIDEO_FINAL_V7.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# Limpiar
shutil.rmtree('frames_final')

if os.path.exists('output/VIDEO_FINAL_V7.mp4'):
    size = os.path.getsize('output/VIDEO_FINAL_V7.mp4') / (1024*1024)
    print(f"\n" + "="*60)
    print("✅ VIDEO FINAL V7 COMPLETADO")
    print("="*60)
    print(f"📁 output/VIDEO_FINAL_V7.mp4")
    print(f"💾 {size:.1f} MB")
    print(f"🎨 Enriquecido + Roboto REAL")
    print("="*60)
else:
    print("❌ Error")
    print(result.stderr[:300])
