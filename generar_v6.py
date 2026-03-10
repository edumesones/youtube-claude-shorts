#!/usr/bin/env python3
"""
PREVIAS v6 - CON FUENTE REAL (Roboto-Bold descargada)
"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

Path('assets/preview_v6').mkdir(parents=True, exist_ok=True)
Path('pantallazos').mkdir(exist_ok=True)

# Usar fuente descargada
FONT_PATH = "fonts/Roboto-Bold.ttf"

def crear_frame_v6(numero, titulo, subtitulo=None):
    """Frame con fuente REAL descargada"""
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), (253, 253, 247))
    draw = ImageDraw.Draw(img)
    
    # CARGAR FUENTE REAL (no default)
    try:
        font_titulo = ImageFont.truetype(FONT_PATH, 280)
        font_sub = ImageFont.truetype(FONT_PATH, 100)
    except Exception as e:
        print(f"❌ Error cargando fuente: {e}")
        return None
    
    # Título - calcular posición centro
    bbox = draw.textbbox((0,0), titulo, font=font_titulo)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = 500
    
    # Dibujar con OUTLINE para legibilidad
    # Outline naranja
    for dx in [-6, -5, -4, 4, 5, 6]:
        for dy in [-6, -5, -4, 4, 5, 6]:
            draw.text((x+dx, y+dy), titulo, font=font_titulo, fill=(212, 120, 56))
    
    # Texto negro encima
    draw.text((x, y), titulo, font=font_titulo, fill=(13, 13, 13))
    
    # Subtítulo
    if subtitulo:
        bbox = draw.textbbox((0,0), subtitulo, font=font_sub)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        draw.text((x, y+320), subtitulo, font=font_sub, fill=(212, 120, 56))
    
    # Número de frame
    font_num = ImageFont.truetype(FONT_PATH, 60)
    draw.text((50, 50), f"0{numero}", fill=(212, 120, 56), font=font_num)
    
    return img

# Generar 5 frames
frames_data = [
    (1, "AHORRA", "40 HORAS"),
    (2, "PROBLEMA", "20+ PDFs"),
    (3, "SOLUCIÓN", "1 CLICK"),
    (4, "RESULTADOS", "+23%"),
    (5, "GRATIS", "PRUEBA YA"),
]

print("🎨 Generando frames V6 (con fuente Roboto REAL)...")
for num, titulo, sub in frames_data:
    img = crear_frame_v6(num, titulo, sub)
    if img:
        img.save(f"assets/preview_v6/frame_{num:02d}.jpg", quality=95)
        img.save(f"pantallazos/frame_{num:02d}_v6.jpg", quality=95)
        print(f"   ✅ Frame {num}: {titulo}")
    else:
        print(f"   ❌ Frame {num}: ERROR")

print("\n✅ FRAMES V6 GENERADOS CON FUENTE REAL")
print("📁 Revisa /pantallazos - versión con fuente descargada")
