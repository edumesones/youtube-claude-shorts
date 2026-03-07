#!/usr/bin/env python3
"""
PREVIAS v5 - EMERGENCIA: Garantizar que el texto se vea
Fondo naranja + texto blanco grande, coordenadas fijas
"""
from PIL import Image, ImageDraw, ImageFont
import shutil

# Canvas 720x1280 
W, H = 720, 1280

# PALABRAS
FRAMES = [
    (1, "AHORRA"),
    (2, "40H"),
    (3, "1 CLICK"),
    (4, "+23%"),
    (5, "GRATIS"),
]

print("🚨 Generando frames EMERGENCIA...")

for num, texto in FRAMES:
    # Fondo NARANJA sólido
    img = Image.new('RGB', (W, H), (230, 100, 30))
    draw = ImageDraw.Draw(img)
    
    # Fuente grande
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
    except:
        font = ImageFont.load_default()
    
    # Coordenadas FIJAS centro
    x, y = 100, 500
    
    # TEXTO BLANCO
    draw.text((x, y), texto, fill=(255,255,255), font=font)
    
    # Guardar
    path = f"pantallazos/frame_{num:02d}_emergencia.png"
    img.save(path, "PNG")
    print(f"   ✅ Frame {num}: '{texto}'")

print("\n✅ LISTOS - Fondo naranja + texto blanco")
