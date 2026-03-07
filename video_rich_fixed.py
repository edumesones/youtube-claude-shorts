#!/usr/bin/env python3
"""
VIDEO RICH - Versión corregida con método confiable
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil

os.makedirs('output', exist_ok=True)
os.makedirs('frames_rich_final', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"

# Colores
ORANGE = (230, 100, 30)
WHITE = (255, 255, 255)
BLACK = (13, 13, 13)
GRAY = (120, 120, 120)
BG = (253, 253, 247)

print("🎬 GENERANDO VIDEO RICH v8...")

frame_count = 0

# 5 SEGMENTOS con contenido enriquecido
segmentos = [
    (1, "AHORRA", "40h", "horas ahoradas", ["Auto", "Rápido", "Fácil", "Gratis"], ORANGE),
    (2, "PROBLEMA", "47", "documentos", ["PDFs", "Excels", "Word", "Docs"], (200, 60, 60)),
    (3, "SOLUCIÓN", "1", "solo click", ["Conectar", "Elegir", "Analizar", "Listo"], (50, 150, 50)),
    (4, "RESULTADOS", "+23%", "más ventas", ["Datos", "Alertas", "Tips", "ROI"], (50, 100, 200)),
    (5, "GRATIS", "$0", "costo total", ["Prueba", "Suscríbete", "Comparte", "Like"], ORANGE),
]

for seg_num, titulo, numero, subtexto, badges, color in segmentos:
    print(f"\n📦 Segmento {seg_num}: {titulo}")
    
    for f in range(150):  # 5 segundos a 30fps
        # Crear imagen
        img = Image.new('RGB', (1080, 1920), BG)
        draw = ImageDraw.Draw(img)
        
        try:
            font_titulo = ImageFont.truetype(FONT, 160)
            font_numero = ImageFont.truetype(FONT, 300)
            font_sub = ImageFont.truetype(FONT, 70)
            font_badge = ImageFont.truetype(FONT, 50)
            font_small = ImageFont.truetype(FONT, 40)
        except:
            font_titulo = font_numero = font_sub = font_badge = font_small = ImageFont.load_default()
        
        # HEADER: Badge número
        draw.rounded_rectangle([40, 40, 160, 120], radius=15, fill=color)
        bbox = draw.textbbox((0,0), f"0{seg_num}", font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text((40 + (120-w)//2, 50), f"0{seg_num}", fill=WHITE, font=font_sub)
        
        # TÍTULO (arriba)
        palabras = titulo.split()
        y = 200
        for palabra in palabras:
            bbox = draw.textbbox((0,0), palabra, font=font_titulo)
            w = bbox[2] - bbox[0]
            x = (1080 - w) // 2
            # Outline
            for dx in [-3, -2, 2, 3]:
                for dy in [-3, -2, 2, 3]:
                    draw.text((x+dx, y+dy), palabra, font=font_titulo, fill=color)
            draw.text((x, y), palabra, font=font_titulo, fill=BLACK)
            y += 160
        
        # NÚMERO GIGANTE en caja
        box_y = 600
        draw.rounded_rectangle([100, box_y, 980, box_y+320], radius=30, fill=color)
        bbox = draw.textbbox((0,0), numero, font=font_numero)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (1080 - w) // 2
        y = box_y + (320 - h) // 2 - 20
        draw.text((x, y), numero, fill=WHITE, font=font_numero)
        
        # Subtítulo
        bbox = draw.textbbox((0,0), subtexto, font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text(((1080-w)//2, box_y+340), subtexto, fill=GRAY, font=font_sub)
        
        # BADGES (4 abajo)
        y_badges = 1050
        for i, badge in enumerate(badges):
            x = 70 + (i * 250)
            draw.rounded_rectangle([x, y_badges, x+230, y_badges+90], radius=15, fill=ORANGE)
            bbox = draw.textbbox((0,0), badge, font=font_badge)
            w = bbox[2] - bbox[0]
            draw.text((x + (230-w)//2, y_badges+20), badge, fill=WHITE, font=font_badge)
        
        # FOOTER
        draw.text((80, 1300), f"⚡ Claude + Drive", fill=color, font=font_sub)
        
        # CTA Botón
        draw.rounded_rectangle([340, 1450, 740, 1570], radius=40, fill=BLACK)
        bbox = draw.textbbox((0,0), "VER MÁS", font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text((340 + (400-w)//2, 1470), "VER MÁS", fill=WHITE, font=font_sub)
        
        # Guardar frame
        path = f"frames_rich_final/frame_{frame_count:04d}.jpg"
        img.save(path, quality=95)
        frame_count += 1
    
    print(f"   ✅ {frame_count} frames totales")

print(f"\n📊 Total frames: {frame_count}")

# Renderizar video
print("\n🎬 Renderizando video...")
cmd = "ffmpeg -y -framerate 30 -i frames_rich_final/frame_%04d.jpg -i output/voz_final.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output/VIDEO_RICH_FINAL.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

# Limpiar
shutil.rmtree('frames_rich_final')

if os.path.exists('output/VIDEO_RICH_FINAL.mp4'):
    size = os.path.getsize('output/VIDEO_RICH_FINAL.mp4') / (1024*1024)
    print(f"\n✅ VIDEO RICH FINAL: {size:.1f} MB")
    print("📁 output/VIDEO_RICH_FINAL.mp4")
else:
    print("❌ Error:", result.stderr[:200])
