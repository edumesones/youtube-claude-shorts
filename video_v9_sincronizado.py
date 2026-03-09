#!/usr/bin/env python3
"""
VIDEO V9 - Sincronizado correctamente + más contenido + fuentes ajustadas
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil

os.makedirs('output', exist_ok=True)
os.makedirs('frames_v9', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"

# Duración REAL del audio: 17 segundos
# Distribución proporcional por segmento basado en palabras del script
# Script: "Hoy te muestro cómo ahorrar 40 horas semanales con Claude Code y Google Drive. (4s)
#          Tienes 20 documentos sin analizar. (3s)
#          La solución es un solo click. (3s)
#          Obtén resultados como más ventas y todo es completamente gratis. (4s)
#          Prueba ahora. (3s)"

SEGMENTOS = [
    {'num': 1, 'titulo': 'AHORRA', 'numero': '40h', 'sub': 'horas semanales', 'badges': ['Auto', 'Rápido', 'Fácil', 'Gratis', 'IA'], 'color': (230,100,30), 'duracion_s': 4},
    {'num': 2, 'titulo': 'PROBLEMA', 'numero': '20+', 'sub': 'documentos', 'badges': ['PDFs', 'Excels', 'Word', 'Imágenes', 'Videos'], 'color': (200,60,60), 'duracion_s': 3},
    {'num': 3, 'titulo': 'SOLUCIÓN', 'numero': '1', 'sub': 'solo click', 'badges': ['Conectar', 'Elegir', 'Analizar', 'Listo', 'Exportar'], 'color': (50,150,50), 'duracion_s': 3},
    {'num': 4, 'titulo': 'RESULTADOS', 'numero': '+23%', 'sub': 'más ventas', 'badges': ['Datos', 'Alertas', 'Tips', 'ROI', 'Gráficos'], 'color': (50,100,200), 'duracion_s': 4},
    {'num': 5, 'titulo': 'GRATIS', 'numero': '$0', 'sub': 'costo total', 'badges': ['Prueba', 'Suscríbete', 'Comparte', 'Like', 'Comenta'], 'color': (230,100,30), 'duracion_s': 3},
]

FPS = 30

print("="*60)
print("🎬 VIDEO V9 - Sincronizado + Enriquecido")
print("="*60)

frame_count = 0

for seg in SEGMENTOS:
    num_frames_seg = seg['duracion_s'] * FPS
    print(f"\n📦 Segmento {seg['num']}: {seg['titulo']} ({seg['duracion_s']}s = {num_frames_seg} frames)")
    
    for f in range(num_frames_seg):
        # Canvas
        img = Image.new('RGB', (1080, 1920), (253,253,247))
        draw = ImageDraw.Draw(img)
        
        try:
            # FUENTES AJUSTADAS - más pequeñas pero legibles
            font_titulo = ImageFont.truetype(FONT, 120)      # ANTES: 160
            font_numero = ImageFont.truetype(FONT, 200)      # ANTES: 300
            font_sub = ImageFont.truetype(FONT, 60)          # ANTES: 70
            font_badge = ImageFont.truetype(FONT, 40)        # ANTES: 50
            font_icono = ImageFont.truetype(FONT, 80)
            font_mini = ImageFont.truetype(FONT, 30)
        except:
            font_titulo = font_numero = font_sub = font_badge = font_icono = font_mini = ImageFont.load_default()
        
        # === HEADER ===
        draw.rounded_rectangle([30, 30, 140, 100], radius=12, fill=seg['color'])
        bbox = draw.textbbox((0,0), f"0{seg['num']}", font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text((30 + (110-w)//2, 38), f"0{seg['num']}", fill=(255,255,255), font=font_sub)
        
        # Icono decorativo (esquina)
        iconos = ['⚡', '⚠️', '💡', '📈', '🎁']
        draw.text((950, 40), iconos[seg['num']-1], fill=seg['color'], font=font_icono)
        
        # === TÍTULO ===
        bbox = draw.textbbox((0,0), seg['titulo'], font=font_titulo)
        w = bbox[2] - bbox[0]
        x = (1080 - w) // 2
        y = 160
        # Outline ligero
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                draw.text((x+dx, y+dy), seg['titulo'], font=font_titulo, fill=seg['color'])
        draw.text((x, y), seg['titulo'], font=font_titulo, fill=(13,13,13))
        
        # === SUBTÍTULO ===
        bbox = draw.textbbox((0,0), seg['sub'], font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text(((1080-w)//2, 310), seg['sub'], fill=(100,100,100), font=font_sub)
        
        # === NÚMERO CENTRAL ===
        box_y = 420
        draw.rounded_rectangle([150, box_y, 930, box_y+200], radius=25, fill=seg['color'], outline=(0,0,0), width=3)
        bbox = draw.textbbox((0,0), seg['numero'], font=font_numero)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (1080 - w) // 2
        y = box_y + (200 - h) // 2 - 15
        draw.text((x, y), seg['numero'], fill=(255,255,255), font=font_numero)
        
        # === MÁS CONTENIDO: Barras de progreso decorativas ===
        for i in range(3):
            y_bar = 660 + (i * 40)
            # Fondo barra
            draw.rounded_rectangle([100, y_bar, 980, y_bar+25], radius=10, fill=(220,220,220))
            # Progreso parcial
            progreso = [0.8, 0.6, 0.9][i]
            ancho = int(880 * progreso)
            draw.rounded_rectangle([100, y_bar, 100+ancho, y_bar+25], radius=10, fill=seg['color'])
        
        # === BADGES (5 en lugar de 4) ===
        y_badges = 820
        # Primera fila: 3 badges
        for i in range(3):
            x = 60 + (i * 340)
            draw.rounded_rectangle([x, y_badges, x+320, y_badges+70], radius=15, fill=seg['color'])
            bbox = draw.textbbox((0,0), seg['badges'][i], font=font_badge)
            w = bbox[2] - bbox[0]
            draw.text((x + (320-w)//2, y_badges+18), seg['badges'][i], fill=(255,255,255), font=font_badge)
        
        # Segunda fila: 2 badges
        y_badges2 = 910
        for i in range(2):
            x = 210 + (i * 340)
            draw.rounded_rectangle([x, y_badges2, x+320, y_badges2+70], radius=15, fill=seg['color'])
            badge_text = seg['badges'][3+i]
            bbox = draw.textbbox((0,0), badge_text, font=font_badge)
            w = bbox[2] - bbox[0]
            draw.text((x + (320-w)//2, y_badges2+18), badge_text, fill=(255,255,255), font=font_badge)
        
        # === MÁS CONTENIDO: Stats adicionales ===
        stats_y = 1050
        stats = ['⏱️ Ahorra tiempo', '💰 Reduce costos', '🎯 Mejora ROI']
        for i, stat in enumerate(stats):
            y_stat = stats_y + (i * 60)
            draw.text((100, y_stat), stat, fill=(80,80,80), font=font_sub)
            draw.text((900, y_stat), "✓", fill=seg['color'], font=font_sub)
        
        # === FOOTER con más info ===
        draw.line([(50, 1280), (1030, 1280)], fill=(200,200,200), width=2)
        
        draw.text((60, 1320), "⚡ Claude Code", fill=seg['color'], font=font_sub)
        draw.text((60, 1390), "+ Google Drive integration", fill=(120,120,120), font=font_mini)
        
        draw.text((60, 1470), "🤖 AI-powered analysis", fill=(120,120,120), font=font_mini)
        
        # CTA
        draw.rounded_rectangle([350, 1580, 730, 1680], radius=30, fill=(13,13,13))
        bbox = draw.textbbox((0,0), "EMPEZAR AHORA", font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text((350 + (380-w)//2, 1600), "EMPEZAR AHORA", fill=(255,255,255), font=font_sub)
        
        # Contador frames (debug)
        draw.text((950, 1880), f"{frame_count}", fill=(200,200,200), font=font_mini)
        
        # Guardar
        img.save(f"frames_v9/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1
    
    print(f"   ✅ {frame_count} frames totales acumulados")

print(f"\n📊 TOTAL: {frame_count} frames (debe ser ~510 para 17s)")

# Renderizar
print("\n🎬 Renderizando video V9...")
cmd = "ffmpeg -y -framerate 30 -i frames_v9/frame_%04d.jpg -i output/voz_final.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output/VIDEO_V9_SINCRONIZADO.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('frames_v9')

if os.path.exists('output/VIDEO_V9_SINCRONIZADO.mp4'):
    size = os.path.getsize('output/VIDEO_V9_SINCRONIZADO.mp4') / (1024*1024)
    print(f"\n" + "="*60)
    print("✅ VIDEO V9 SINCRONIZADO")
    print("="*60)
    print(f"📁 output/VIDEO_V9_SINCRONIZADO.mp4")
    print(f"💾 {size:.1f} MB")
    print(f"⏱️  ~17 segundos (cuadrado con audio)")
    print(f"🎨 5 segmentos proporcionales")
    print(f"✅ Fuentes ajustadas (más pequeñas)")
    print(f"✅ MÁS contenido por pantalla")
    print("="*60)
else:
    print("❌ Error:", result.stderr[:300])
