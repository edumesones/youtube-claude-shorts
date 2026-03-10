#!/usr/bin/env python3
"""
PREVIAS v2 - Más contenido visual, estilo marketing high-engagement
"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

Path('assets/preview_v2').mkdir(parents=True, exist_ok=True)

# COLORES CLAUDE
COLORS = {
    'bg': (253, 253, 247),
    'orange': (212, 120, 56),
    'orange_dark': (180, 90, 40),
    'text': (13, 13, 13),
    'text_gray': (100, 100, 100),
    'green': (35, 134, 54),
    'red': (248, 81, 73),
}

def crear_frame_rico(numero, titulo, datos, metricas, iconos):
    """Frame con MUCHO contenido visual"""
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 280)  # ENORME
        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_num = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 350)  # NÚMEROS GIGANTES
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
    except:
        font_big = font_med = font_num = font_small = ImageFont.load_default()
    
    # HEADER con badge de segmento
    draw.rounded_rectangle([40, 40, 180, 120], radius=20, fill=COLORS['orange'])
    draw.text((75, 55), f"0{numero}", fill=(255,255,255), font=font_med)
    
    # TÍTULO PRINCIPAL (más arriba)
    words = titulo.split()
    y = 200
    for word in words[:3]:  # Máx 3 palabras
        bbox = draw.textbbox((0,0), word, font=font_big)
        x = (width - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), word, fill=COLORS['text'], font=font_big)
        y += 200
    
    # MÉTRICAS GRANDES (centro)
    y_metric = 900
    for label, value, color in metricas:
        # Caja de fondo
        draw.rounded_rectangle([80, y_metric-20, 1000, y_metric+200], radius=30, fill=(240,240,240))
        # Número enorme
        draw.text((150, y_metric), value, fill=color, font=font_num)
        # Label
        draw.text((150, y_metric+170), label, fill=COLORS['text_gray'], font=font_small)
        y_metric += 280
    
    # DATOS ADICIONALES (badges)
    y_data = 1550
    for i, dato in enumerate(datos[:3]):
        x_pos = 100 + (i * 320)
        draw.rounded_rectangle([x_pos, y_data, x_pos+280, y_data+100], radius=15, fill=COLORS['orange'])
        bbox = draw.textbbox((0,0), dato, font=font_small)
        text_w = bbox[2] - bbox[0]
        draw.text((x_pos + (280-text_w)//2, y_data+25), dato, fill=(255,255,255), font=font_small)
    
    # FOOTER con branding
    draw.text((80, 1820), "⚡ Claude Code", fill=COLORS['orange'], font=font_med)
    draw.text((600, 1820), "+ Google Drive", fill=COLORS['text_gray'], font=font_small)
    
    return img

# CREAR 5 FRAMES CON MUCHO CONTENIDO
frames = [
    {
        'num': 1,
        'titulo': 'AHORRA 40 HORAS',
        'metricas': [
            ('Tiempo ahorrado', '40h', COLORS['green']),
            ('Por semana', '↑ 300%', COLORS['orange']),
        ],
        'datos': ['Automático', 'Instantáneo', 'Sin esfuerzo'],
    },
    {
        'num': 2,
        'titulo': 'EL PROBLEMA',
        'metricas': [
            ('PDFs sin leer', '47', COLORS['red']),
            ('Horas perdidas', '60h', COLORS['red']),
        ],
        'datos': ['Informes', 'Contratos', 'Facturas'],
    },
    {
        'num': 3,
        'titulo': '1 CLICK',
        'metricas': [
            ('Comando', '"Analiza"', COLORS['orange']),
            ('Tiempo', '3 seg', COLORS['green']),
        ],
        'datos': ['Conecta Drive', 'Selecciona', 'Listo'],
    },
    {
        'num': 4,
        'titulo': 'RESULTADOS',
        'metricas': [
            ('Ventas ↑', '+23%', COLORS['green']),
            ('Insights', '12', COLORS['orange']),
        ],
        'datos': ['Accionables', 'Claros', 'Rápidos'],
    },
    {
        'num': 5,
        'titulo': 'GRATIS',
        'metricas': [
            ('Costo', '$0', COLORS['green']),
            ('Prueba', 'Ahora', COLORS['orange']),
        ],
        'datos': ['Suscríbete', 'Comparte', 'Comenta'],
    },
]

print("🎨 Generando frames V2 (rico contenido)...")
for f in frames:
    img = crear_frame_rico(f['num'], f['titulo'], f['datos'], f['metricas'], [])
    img.save(f"assets/preview_v2/frame_0{f['num']}_rich.jpg", quality=95)
    print(f"   ✅ Frame {f['num']}: {f['titulo']}")

# Copiar a pantallazos
import shutil
for f in frames:
    shutil.copy(f"assets/preview_v2/frame_0{f['num']}_rich.jpg", f"pantallazos/")

print("\n✅ Actualizados en /pantallazos")
