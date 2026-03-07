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
    
    # Fuentes MUY grandes para legibilidad móvil (casi pantalla completa)
    try:
        font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 200)  # ANTES: 140
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)      # ANTES: 70
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)         # ANTES: 60
    except:
        font_titulo = ImageFont.load_default()
        font_sub = font_titulo
        font_body = font_titulo
    
    # Header con número de segmento (pequeño, esquina)
    draw.text((60, 60), f"0{numero}", fill=COLORS['orange'], font=font_body)
    draw.line([(60, 140), (200, 140)], fill=COLORS['orange'], width=4)
    
    # Título principal GRANDE y centrado
    # Dividir en líneas si es largo
    palabras = titulo.split()
    lineas = []
    linea_actual = []
    
    for palabra in palabras:
        linea_actual.append(palabra)
        if len(' '.join(linea_actual)) > 12:  # Máx 12 chars por línea
            lineas.append(' '.join(linea_actual[:-1]))
            linea_actual = [linea_actual[-1]]
    if linea_actual:
        lineas.append(' '.join(linea_actual))
    
    # Dibujar título (máx 2 líneas, más espaciado)
    y_titulo = 500  # Más abajo para que quepa el texto grande
    for i, linea in enumerate(lineas[:2]):
        bbox = draw.textbbox((0, 0), linea, font=font_titulo)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_titulo + i*240), linea, fill=COLORS['text_dark'], font=font_titulo)  # Más espacio entre líneas
    
    # Subtítulo
    if subtitulo:
        y_sub = y_titulo + len(lineas)*240 + 150  # Más espacio
        bbox = draw.textbbox((0, 0), subtitulo, font=font_sub)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_sub), subtitulo, fill=COLORS['orange'], font=font_sub)
    
    # Elementos adicionales (iconos simples)
    if elementos:
        y_elem = 1000
        for elem in elementos:
            draw.text((100, y_elem), f"• {elem}", fill=COLORS['text_gray'], font=font_body)
            y_elem += 120
    
    # Footer con branding
    draw.text((60, height-150), "Claude", fill=COLORS['orange'], font=font_sub)
    draw.text((300, height-150), "Code", fill=COLORS['text_gray'], font=font_sub)
    
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
