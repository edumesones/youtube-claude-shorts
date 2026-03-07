#!/usr/bin/env python3
"""
DIAGNÓSTICO RÁPIDO - ¿Por qué el texto no se ve grande?
"""
from PIL import Image, ImageDraw, ImageFont
import os

print("="*60)
print("🔍 DIAGNÓSTICO DE TEXTO EN PIL")
print("="*60)

# 1. Verificar fuente existe
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
print(f"\n1. ¿Existe la fuente? {font_path}")
print(f"   {os.path.exists(font_path)}")

# 2. Probar carga de fuente
print("\n2. Probando cargar fuente a diferentes tamaños:")
for size in [50, 100, 200, 340, 500]:
    try:
        font = ImageFont.truetype(font_path, size)
        print(f"   Tamaño {size}: ✅ OK")
    except Exception as e:
        print(f"   Tamaño {size}: ❌ {e}")

# 3. Crear imagen de prueba
print("\n3. Creando imagen de prueba...")
img = Image.new('RGB', (1080, 1920), (253, 253, 247))
draw = ImageDraw.Draw(img)

# 4. Probar con tamaño 340
try:
    font_big = ImageFont.truetype(font_path, 340)
    
    # Obtener bounding box
    bbox = draw.textbbox((0,0), "TEST", font=font_big)
    print(f"\n4. Bounding box de 'TEST' a 340px:")
    print(f"   Ancho: {bbox[2]-bbox[0]}px")
    print(f"   Alto: {bbox[3]-bbox[1]}px")
    
    # Dibujar en centro
    text = "AHORRA"
    bbox = draw.textbbox((0,0), text, font=font_big)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (1080 - w) // 2
    y = (1920 - h) // 2
    
    print(f"\n5. Posición calculada para '{text}':")
    print(f"   x={x}, y={y}")
    print(f"   texto: {w}x{h}px")
    
    # Dibujar con alto contraste
    draw.rectangle([x-10, y-10, x+w+10, y+h+10], fill=(230, 100, 30))  # Fondo naranja
    draw.text((x, y), text, fill=(255,255,255), font=font_big)  # Texto blanco
    
    # Guardar
    os.makedirs('test_output', exist_ok=True)
    img.save('test_output/diagnostico.jpg', quality=95)
    print(f"\n6. ✅ Imagen guardada: test_output/diagnostico.jpg")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "="*60)
print("Revisa la imagen generada en test_output/")
print("="*60)
