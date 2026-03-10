#!/usr/bin/env python3
"""
PREVIAS v4 - Texto GIGANTE que llene la pantalla
Canvas 720x1280 (más pequeño = texto proporcionalmente más grande)
"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import shutil

Path('assets/preview_v4').mkdir(parents=True, exist_ok=True)

def crear_frame_v4(numero, palabra):
    """Una sola palabra GIGANTE centrada"""
    # Canvas más pequeño para mejor proporción en móvil
    width, height = 720, 1280
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        # Fuente ENORME
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 200)
    except:
        font = ImageFont.load_default()
    
    # Contar espacio disponible y ajustar
    bbox = draw.textbbox((0,0), palabra, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Reducir fuente si no cabe
    while text_width > width - 40 and font.size > 50:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font.size - 10)
        bbox = draw.textbbox((0,0), palabra, font=font)
        text_width = bbox[2] - bbox[0]
    
    # Centrar exacto
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 50
    
    # Outline grueso naranja
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            if abs(dx) > 3 or abs(dy) > 3:
                draw.text((x+dx, y+dy), palabra, font=font, fill=(230, 100, 30))
    
    # Outline negro
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            draw.text((x+dx, y+dy), palabra, font=font, fill=(0, 0, 0))
    
    # Texto blanco
    draw.text((x, y), palabra, font=font, fill=(255, 255, 255))
    
    # Número pequeño arriba
    num_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60) if font else ImageFont.load_default()
    draw.text((30, 30), f"0{numero}", fill=(230, 100, 30), font=num_font)
    
    return img

# 5 frames con palabras simples y grandes
palabras = ["AHORRA", "PROBLEMA", "SOLUCIÓN", "RESULTADOS", "GRATIS"]

print("🎨 Generando frames V4 (canvas 720x1280)...")
for i, palabra in enumerate(palabras, 1):
    img = crear_frame_v4(i, palabra)
    # Guardar como PNG en alta calidad
    img.save(f"assets/preview_v4/frame_0{i}_{palabra.lower()}.png", "PNG")
    shutil.copy(f"assets/preview_v4/frame_0{i}_{palabra.lower()}.png", "pantallazos/")
    print(f"   ✅ {palabra}")

print("\n✅ Frames V4 generados (720x1280)")
print("📁 Una palabra GIGANTE centrada por frame")
