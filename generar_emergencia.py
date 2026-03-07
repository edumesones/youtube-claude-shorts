#!/usr/bin/env python3
"""
PREVIAS v5 - EMERGENCIA: Garantizar que el texto se vea
"""
from PIL import Image, ImageDraw, ImageFont
import shutil

# Canvas 720x1280 (proporción 9:16 pero más pequeño)
W, H = 720, 1280

# PALABRAS - una por frame
FRAMES = [
    (1, "AHORRA"),
    (2, "40H"),
    (3, "1 CLICK"),
    (4, "+23%"),
    (5, "GRATIS"),
]

print("🚨 Generando frames EMERGENCIA...")

for num, texto in FRAMES:
    # Crear imagen blanca
    img = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # INTENTAR cargar fuente grande
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
    except:
        font = ImageFont.load_default()
        print(f"   ⚠️ Frame {num}: usando fuente default")
    
    # FONDO RECTÁNGULO NARANJA (para asegurar visibilidad)
    bbox = draw.textbbox((0,0), texto, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    # Centrar
    x = (W - text_w) // 2
    y = (H - text_h) // 2 - 50
    
    # RECTÁNGULO de fondo naranja
    margin = 40
    draw.rectangle(
        [x-margin, y-margin, x+text_w+margin, y+text_h+margin],
        fill=(230, 100, 30),  # Naranja Claude
        outline=(0,0,0),
        width=5
    )
    
    # TEXTO BLANCO encima
    draw.text((x, y), texto, fill=(255,255,255), font=font)
    
    # Número en esquina
    num_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50) if font else ImageFont.load_default()
    draw.text((20, 20), str(num), fill=(230,100,30), font=num_font)
    
    # Guardar
    path = f"pantallazos/frame_{num:02d}_emergencia.png"
    img.save(path, "PNG")
    print(f"   ✅ Frame {num}: '{texto}' - {text_w}x{text_h}px")

print("\n✅ FRAMES EMERGENCIA LISTOS")
print("📁 Revisa /pantallazos")
print("\nCada frame tiene:")
print("  - Fondo rectángulo NARANJA")
print("  - Texto BLANCO encima")
print("  - Dimensiones garantizadas")
