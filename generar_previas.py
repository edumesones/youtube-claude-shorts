#!/usr/bin/env python3
"""
Genera frames con ESTILO CLAUDE (blanco + naranja)
y crea pantallazos para revisión ANTES de subir.
"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

Path('assets/preview').mkdir(parents=True, exist_ok=True)

# PALETA DE COLORES OFICIAL CLAUDE
COLORS = {
    'bg_white': (255, 255, 255),        # Fondo blanco
    'bg_cream': (253, 253, 247),        # Fondo crema claro (Anthropic)
    'orange': (212, 120, 56),           # Naranja Claude #D47838
    'orange_light': (235, 160, 120),    # Naranja claro
    'text_dark': (13, 13, 13),          # Texto principal casi negro
    'text_gray': (80, 80, 80),          # Texto secundario
    'accent': (212, 120, 56),           # Acentos naranja
}

def crear_frame_claude(titulo, subtitulo=None, elementos=None, numero=1):
    """Crea frame con estilo visual Claude (clean, minimal, blanco+naranja)"""
    
    # Canvas blanco/crema
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), COLORS['bg_cream'])
    draw = ImageDraw.Draw(img)
    
    # Fuentes ENORMES para legibilidad móvil (ocupar casi toda la pantalla)
    try:
        font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 340)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 130)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 110)
    except:
        font_titulo = ImageFont.load_default()
        font_sub = font_titulo
        font_body = font_titulo
    
    # Header con número de segmento
    draw.text((60, 50), f"0{numero}", fill=COLORS['orange'], font=font_sub)
    draw.line([(60, 200), (280, 200)], fill=COLORS['orange'], width=8)

    # Título principal ENORME y centrado
    # Dividir en líneas cortas para que cada palabra sea grande
    palabras = titulo.split()
    lineas = []
    linea_actual = []

    for palabra in palabras:
        linea_actual.append(palabra)
        if len(' '.join(linea_actual)) > 10:  # Máx 10 chars por línea
            lineas.append(' '.join(linea_actual[:-1]))
            linea_actual = [linea_actual[-1]]
    if linea_actual:
        lineas.append(' '.join(linea_actual))

    # Dibujar título centrado verticalmente
    y_titulo = 300
    for i, linea in enumerate(lineas[:3]):
        bbox = draw.textbbox((0, 0), linea, font=font_titulo)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_titulo + i*380), linea, fill=COLORS['text_dark'], font=font_titulo)

    # Subtítulo
    if subtitulo:
        y_sub = y_titulo + len(lineas)*380 + 80
        # Dividir subtítulo si es largo
        if len(subtitulo) > 20:
            partes = subtitulo.split(' · ') if ' · ' in subtitulo else [subtitulo]
            for j, parte in enumerate(partes):
                bbox = draw.textbbox((0, 0), parte, font=font_sub)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                draw.text((x, y_sub + j*160), parte, fill=COLORS['orange'], font=font_sub)
        else:
            bbox = draw.textbbox((0, 0), subtitulo, font=font_sub)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_sub), subtitulo, fill=COLORS['orange'], font=font_sub)

    # Elementos adicionales (más grandes, más espaciados)
    if elementos:
        y_elem = 1250
        for elem in elementos:
            draw.text((80, y_elem), f"• {elem}", fill=COLORS['text_gray'], font=font_body)
            y_elem += 160

    # Footer con branding (más grande)
    draw.text((60, height-200), "Claude", fill=COLORS['orange'], font=font_sub)
    draw.text((380, height-200), "Code", fill=COLORS['text_gray'], font=font_sub)
    
    return img

def main():
    print("=" * 60)
    print("🎨 GENERANDO PREVIAS - Estilo Claude")
    print("=" * 60)
    
    # 5 FRAMES representando cada segmento
    frames_info = [
        {
            'num': 1,
            'titulo': 'Google Drive + Claude',
            'sub': 'Habla con tus documentos',
            'elems': ['Conexión directa', 'Análisis automático', 'Resultados en segundos']
        },
        {
            'num': 2,
            'titulo': 'El Problema',
            'sub': '20+ PDFs sin analizar',
            'elems': ['Informes de ventas', 'Contratos', 'Facturas', 'Horas de lectura']
        },
        {
            'num': 3,
            'titulo': 'La Solución',
            'sub': 'Un comando y listo',
            'elems': ['"Analiza mis documentos"', 'Claude procesa todo', 'Insights instantáneos']
        },
        {
            'num': 4,
            'titulo': 'Resultados',
            'sub': '+23% ventas · 3 alertas · 1 recomendación',
            'elems': ['Datos claros', 'Accionables', 'En segundos']
        },
        {
            'num': 5,
            'titulo': 'Prueba Ahora',
            'sub': 'Transforma tu workflow',
            'elems': ['Sígueme para más tips', 'Like + Comparte']
        }
    ]
    
    print("\n📸 Generando 5 pantallazos de preview...\n")
    
    for frame_info in frames_info:
        img = crear_frame_claude(
            frame_info['titulo'],
            frame_info['sub'],
            frame_info['elems'],
            frame_info['num']
        )
        
        path = f"assets/preview/frame_0{frame_info['num']}_claude_style.jpg"
        img.save(path, quality=95)
        print(f"   ✅ Frame {frame_info['num']}: {frame_info['titulo']}")
    
    print("\n" + "=" * 60)
    print("📸 PREVIAS GENERADAS")
    print("=" * 60)
    print("\nRevisa los frames en: assets/preview/")
    print("\nSi te gustan, ejecuto:")
    print("  python create_video_claude_style.py")
    print("\nPara generar el video final.")
    print("=" * 60)

if __name__ == "__main__":
    main()
