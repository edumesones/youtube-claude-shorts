#!/usr/bin/env python3
"""
PREVIAS v3 - Solución técnica: Mejor contraste, anti-aliasing, PNG
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from pathlib import Path
import shutil

Path('assets/preview_v3').mkdir(parents=True, exist_ok=True)

# COLORES ALTO CONTRASTE
COLORS = {
    'bg': (255, 255, 255),           # Blanco puro
    'orange': (230, 100, 30),        # Naranja más intenso
    'text': (0, 0, 0),               # Negro puro (máximo contraste)
    'text_gray': (80, 80, 80),
}

def add_text_with_outline(draw, text, position, font, fill, outline_width=4):
    """Añade texto con contorno para mejor legibilidad"""
    x, y = position
    # Contorno negro
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx != 0 or dy != 0:
                draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0))
    # Texto principal
    draw.text((x, y), text, font=font, fill=fill)

def crear_frame_optimizado(numero, titulo, subtitulo=None):
    """Frame optimizado para legibilidad móvil"""
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # Fuentes masivas con antialiasing implícito
    try:
        font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 320)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
        font_num = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 400)
    except:
        font_titulo = font_sub = font_num = ImageFont.load_default()
    
    # Número de frame ENORME en esquina
    bbox = draw.textbbox((0,0), str(numero), font=font_num)
    draw.text((50, 50), str(numero), fill=(240,240,240), font=font_num)  # Gris claro, fondo
    
    # TÍTULO - Una sola palabra enorme centrada
    words = titulo.split()[:2]  # Máximo 2 palabras
    y_pos = 600
    for word in words:
        bbox = draw.textbbox((0,0), word, font=font_titulo)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        # Contorno naranja
        for dx in [-5, -4, -3, 3, 4, 5]:
            for dy in [-5, -4, -3, 3, 4, 5]:
                draw.text((x+dx, y_pos+dy), word, font=font_titulo, fill=COLORS['orange'])
        # Texto blanco encima
        draw.text((x, y_pos), word, font=font_titulo, fill=(255,255,255))
        y_pos += 360
    
    # Subtítulo
    if subtitulo:
        bbox = draw.textbbox((0,0), subtitulo, font=font_sub)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y_sub = y_pos + 100
        add_text_with_outline(draw, subtitulo, (x, y_sub), font_sub, COLORS['orange'], 3)
    
    # Footer simple
    footer = "Claude + Drive"
    bbox = draw.textbbox((0,0), footer, font=font_sub)
    draw.text(((width-(bbox[2]-bbox[0]))//2, 1750), footer, fill=COLORS['text_gray'], font=font_sub)
    
    return img

# Generar 5 frames
frames_data = [
    (1, "AHORRA", "40 HORAS"),
    (2, "EL", "PROBLEMA"),
    (3, "UN", "CLICK"),
    (4, "RESULTADOS", "+23%"),
    (5, "GRATIS", "PRUEBA"),
]

print("🎨 Generando frames V3 (optimizado legibilidad)...")
for num, titulo, sub in frames_data:
    img = crear_frame_optimizado(num, titulo, sub)
    # Guardar como PNG (sin compresión) para máxima calidad
    img.save(f"assets/preview_v3/frame_0{num}_optimized.png", "PNG")
    print(f"   ✅ Frame {num}: {titulo}")

# Copiar a pantallazos
for num, _, _ in frames_data:
    shutil.copy(f"assets/preview_v3/frame_0{num}_optimized.png", f"pantallazos/")

print("\n✅ Guardados en PNG (sin pérdida)")
print("📁 Revisa /pantallazos - versión optimizada")
