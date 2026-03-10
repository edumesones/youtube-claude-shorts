#!/usr/bin/env python3
"""
VIDEO RICH v8 - Contenido enriquecido con MUCHOS elementos visuales
Estilo marketing high-engagement
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil

os.makedirs('output', exist_ok=True)
os.makedirs('rich_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"
FONT_REG = "fonts/Roboto-Bold.ttf"

# COLORES
ORANGE = (230, 100, 30)
ORANGE_LIGHT = (255, 150, 80)
WHITE = (255, 255, 255)
BLACK = (13, 13, 13)
GRAY = (120, 120, 120)
BG = (253, 253, 247)
GREEN = (35, 150, 50)
RED = (220, 60, 60)

def draw_rounded_rect(draw, coords, radius, fill, outline=None, width=1):
    """Dibuja rectángulo redondeado"""
    x1, y1, x2, y2 = coords
    draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline, width=width)

def crear_frame_rich(numero, titulo, numero_grande, sub_numero, badges, color_acento):
    """Frame con MUCHO contenido visual"""
    W, H = 1080, 1920
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    
    try:
        font_titulo = ImageFont.truetype(FONT, 160)
        font_numero = ImageFont.truetype(FONT, 350)
        font_sub = ImageFont.truetype(FONT, 70)
        font_badge = ImageFont.truetype(FONT, 50)
        font_small = ImageFont.truetype(FONT, 40)
    except:
        font_titulo = font_numero = font_sub = font_badge = font_small = ImageFont.load_default()
    
    # HEADER: Badge de número
    draw.rounded_rectangle([40, 40, 180, 130], radius=20, fill=color_acento)
    bbox = draw.textbbox((0,0), f"0{numero}", font=font_sub)
    w = bbox[2] - bbox[0]
    draw.text((40 + (140-w)//2, 55), f"0{numero}", fill=WHITE, font=font_sub)
    
    # TÍTULO PRINCIPAL (arriba, grande)
    palabras = titulo.split()[:2]
    y = 200
    for palabra in palabras:
        bbox = draw.textbbox((0,0), palabra, font=font_titulo)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        # Shadow/outline
        for dx in [-4, -3, 3, 4]:
            for dy in [-4, -3, 3, 4]:
                draw.text((x+dx, y+dy), palabra, font=font_titulo, fill=color_acento)
        draw.text((x, y), palabra, font=font_titulo, fill=BLACK)
        y += 180
    
    # NÚMERO GIGANTE (centro) en caja
    box_y = 650
    draw.rounded_rectangle([80, box_y, 1000, box_y+380], radius=40, fill=color_acento, outline=BLACK, width=5)
    bbox = draw.textbbox((0,0), numero_grande, font=font_numero)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (W - w) // 2
    y = box_y + (380 - h) // 2 - 30
    draw.text((x, y), numero_grande, fill=WHITE, font=font_numero)
    
    # SUBTÍTULO debajo del número
    bbox = draw.textbbox((0,0), sub_numero, font=font_sub)
    w = bbox[2] - bbox[0]
    draw.text(((W-w)//2, box_y+400), sub_numero, fill=GRAY, font=font_sub)
    
    # BADGES (abajo, múltiples)
    y_badges = 1200
    x_start = 60
    for i, badge in enumerate(badges[:4]):
        x = x_start + (i * 260)
        # Caja de badge
        bw = 240
        draw.rounded_rectangle([x, y_badges, x+bw, y_badges+100], radius=20, fill=ORANGE)
        # Texto centrado
        bbox = draw.textbbox((0,0), badge, font=font_badge)
        w = bbox[2] - bbox[0]
        draw.text((x + (bw-w)//2, y_badges+25), badge, fill=WHITE, font=font_badge)
    
    # Línea decorativa
    draw.line([(80, 1400), (1000, 1400)], fill=color_acento, width=6)
    
    # FOOTER con iconos simulados
    footer_y = 1550
    draw.text((80, footer_y), "⚡", fill=ORANGE, font=font_sub)
    draw.text((160, footer_y), "Claude", fill=ORANGE, font=font_sub)
    draw.text((380, footer_y), "Code", fill=GRAY, font=font_small)
    draw.text((600, footer_y), "+ Google Drive", fill=GRAY, font=font_small)
    
    # CTA pequeño
    draw.rounded_rectangle([350, 1700, 730, 1820], radius=50, fill=BLACK)
    bbox = draw.textbbox((0,0), "VER MÁS", font=font_sub)
    w = bbox[2] - bbox[0]
    draw.text((350 + (380-w)//2, 1720), "VER MÁS", fill=WHITE, font=font_sub)
    
    # Guardar múltiples frames
    frames = []
    for i in range(150):  # 5 segundos
        path = f"rich_frames/rich_{numero:02d}_{i:03d}.jpg"
        img.save(path, quality=95)
        frames.append(path)
    
    return frames

print("="*60)
print("🎬 VIDEO RICH v8 - Enriquecido máximo")
print("="*60)

# 5 SEGMENTOS con MUCHO contenido
segmentos = [
    {
        'num': 1,
        'titulo': 'AHORRA',
        'numero': '40h',
        'sub': 'horas semanales',
        'badges': ['Auto', 'Rápido', 'Fácil', 'Gratis'],
        'color': ORANGE,
    },
    {
        'num': 2,
        'titulo': 'PROBLEMA',
        'numero': '47',
        'sub': 'documentos',
        'badges': ['PDFs', 'Excels', 'Word', 'Imágenes'],
        'color': RED,
    },
    {
        'num': 3,
        'titulo': 'SOLUCIÓN',
        'numero': '1',
        'sub': 'solo click',
        'badges': ['Conectar', 'Seleccionar', 'Analizar', 'Listo'],
        'color': GREEN,
    },
    {
        'num': 4,
        'titulo': 'RESULTADOS',
        'numero': '+23%',
        'sub': 'más productividad',
        'badges': ['Ventas ↑', 'Alertas', 'Tips', 'ROI'],
        'color': (50, 120, 200),  # Azul
    },
    {
        'num': 5,
        'titulo': 'GRATIS',
        'numero': '$0',
        'sub': 'costo total',
        'badges': ['Prueba', 'Suscríbete', 'Comparte', 'Like'],
        'color': ORANGE,
    },
]

print("\n🎨 Generando frames RICH...")
all_frames = []
for seg in segmentos:
    frames = crear_frame_rich(
        seg['num'], seg['titulo'], seg['numero'], 
        seg['sub'], seg['badges'], seg['color']
    )
    all_frames.extend(frames)
    print(f"   ✅ {seg['titulo']}: {len(frames)} frames, {len(seg['badges'])} badges")

print(f"\n📊 Total: {len(all_frames)} frames")

# Renderizar
print("\n🎬 Renderizando video RICH...")
cmd = "ffmpeg -y -framerate 30 -i rich_frames/rich_%02d_%03d.jpg -i output/voz_final.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output/VIDEO_RICH_v8.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('rich_frames')

if os.path.exists('output/VIDEO_RICH_v8.mp4'):
    size = os.path.getsize('output/VIDEO_RICH_v8.mp4') / (1024*1024)
    print(f"\n" + "="*60)
    print("✅ VIDEO RICH v8 COMPLETADO")
    print("="*60)
    print(f"📁 output/VIDEO_RICH_v8.mp4")
    print(f"💾 {size:.1f} MB")
    print(f"⏱️  25 segundos")
    print(f"🎨 5 segmentos + 4 badges + números gigantes")
    print("="*60)
else:
    print("❌ Error")
    print(result.stderr[:300])
