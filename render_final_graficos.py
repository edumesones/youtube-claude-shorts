#!/usr/bin/env python3
"""
RENDER FINAL v2 - Silencio inicial + PDF con gráficos + Voz natural
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil
import numpy as np

os.makedirs('demo_final_output', exist_ok=True)
os.makedirs('demo_final_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"
FPS = 30

colors = {
    'bg': (30, 30, 30), 'text': (200, 200, 200),
    'prompt': (50, 150, 50), 'command': (255, 255, 255),
    'output': (150, 150, 150), 'highlight': (230, 100, 30),
    'pdf': (200, 50, 50), 'success': (50, 200, 50),
    'pdf_bg': (255, 255, 255), 'pdf_text': (50, 50, 50),
    'chart_blue': (50, 100, 200), 'chart_green': (50, 150, 50),
    'chart_orange': (230, 100, 30),
}

def draw_chart_bars(draw, x, y, values, colors_list, labels, font):
    """Dibuja gráfico de barras"""
    bar_width = 60
    spacing = 20
    max_val = max(values)
    
    for i, (val, color, label) in enumerate(zip(values, colors_list, labels)):
        bar_h = int((val / max_val) * 150)
        bar_x = x + i * (bar_width + spacing)
        bar_y = y + 150 - bar_h
        
        # Barra
        draw.rectangle([bar_x, bar_y, bar_x + bar_width, y + 150], fill=color, outline=(0,0,0), width=2)
        # Valor encima
        draw.text((bar_x + 10, bar_y - 25), f"{val}%", fill=(0,0,0), font=font)
        # Label abajo
        draw.text((bar_x, y + 160), label, fill=(100,100,100), font=font)

def draw_pie_chart(draw, cx, cy, radius, percentages, colors_list, font):
    """Dibuja gráfico circular"""
    start_angle = 0
    for pct, color in zip(percentages, colors_list):
        angle = int(360 * pct / 100)
        # Dibujar sector (simplificado como arco)
        draw.pieslice([cx-radius, cy-radius, cx+radius, cy+radius], 
                      start=start_angle, end=start_angle+angle, fill=color, outline=(255,255,255), width=2)
        start_angle += angle
    
    # Centro blanco
    draw.ellipse([cx-30, cy-30, cx+30, cy+30], fill=(255,255,255))
    draw.text((cx-20, cy-10), "2024", fill=(0,0,0), font=font)

def crear_pdf_con_graficos(draw, scroll_pos, fonts):
    """PDF con análisis financiero y gráficos"""
    font_title, font_sub, font_body, font_chart = fonts
    
    # Fondo PDF
    draw.rectangle([100, 200, 980, 1700], fill=colors['pdf_bg'], outline=(200,200,200), width=2)
    draw.rectangle([100, 200, 980, 280], fill=(240,240,240))
    draw.text((150, 220), "📊 ANÁLISIS FINANCIERO Q1 2024", fill=(13,13,13), font=font_title)
    draw.text((150, 260), "Generado por Claude Code • Enterprise Report", fill=(100,100,100), font=font_sub)
    
    y = 320 - scroll_pos
    
    # SECCIÓN 1: Métricas clave
    if y > 200:
        draw.text((150, y), "1. MÉTRICAS PRINCIPALES", fill=colors['chart_blue'], font=font_sub)
    y += 50
    
    # KPIs en cajas
    kpis = [
        ("Ventas", "+23%", colors['chart_green']),
        ("Clientes", "156", colors['chart_blue']),
        ("Retención", "92%", colors['chart_orange']),
    ]
    for i, (label, val, col) in enumerate(kpis):
        x = 150 + i * 270
        if y > 200:
            draw.rounded_rectangle([x, y, x+250, y+100], radius=10, fill=col)
            draw.text((x+20, y+20), label, fill=(255,255,255), font=font_body)
            draw.text((x+20, y+55), val, fill=(255,255,255), font=font_title)
    y += 130
    
    # SECCIÓN 2: Gráfico de barras
    if y > 200:
        draw.text((150, y), "2. CRECIMIENTO POR TRIMESTRE", fill=colors['chart_blue'], font=font_sub)
    y += 50
    if y > 100:
        draw_chart_bars(draw, 150, y, [15, 18, 23, 28], 
                       [colors['chart_orange'], colors['chart_blue'], colors['chart_green'], colors['chart_blue']],
                       ['Q1', 'Q2', 'Q3', 'Q4'], font_chart)
    y += 220
    
    # SECCIÓN 3: Gráfico circular
    if y > 200:
        draw.text((150, y), "3. DISTRIBUCIÓN DE INGRESOS", fill=colors['chart_blue'], font=font_sub)
    y += 50
    if y > 100:
        draw_pie_chart(draw, 350, y + 100, 80, [45, 30, 25], 
                      [colors['chart_blue'], colors['chart_green'], colors['chart_orange']], font_chart)
        # Leyenda
        leyenda = [("SaaS 45%", colors['chart_blue']), ("Servicios 30%", colors['chart_green']), ("Otros 25%", colors['chart_orange'])]
        for i, (txt, col) in enumerate(leyenda):
            draw.rectangle([500, y + i*40, 530, y + i*40 + 20], fill=col)
            draw.text((540, y + i*40), txt, fill=(0,0,0), font=font_body)
    y += 250
    
    # SECCIÓN 4: Alertas
    if y > 200:
        draw.text((150, y), "4. ALERTAS DETECTADAS", fill=colors['pdf'], font=font_sub)
    y += 50
    alertas = [
        "⚠️  3 contratos Enterprise expiran en <30 días",
        "⚠️  Churn rate sector retail: 8% (+2% vs Q4)",
        "⚠️  Pago pendiente Cliente ABC: $45,000",
    ]
    for alerta in alertas:
        if y > 200 and y < 1650:
            draw.text((170, y), alerta, fill=colors['pdf'], font=font_body)
        y += 40
    y += 30
    
    # SECCIÓN 5: Recomendaciones
    if y > 200:
        draw.text((150, y), "5. RECOMENDACIONES", fill=colors['chart_green'], font=font_sub)
    y += 50
    recs = [
        "✓ Renegociar contratos críticos antes del 30/marzo",
        "✓ Implementar campaña retención clientes enterprise",
        "✓ Aumentar presupuesto marketing B2B (ROI: 340%)",
        "✓ Revisión semanal de métricas de churn",
    ]
    for rec in recs:
        if y > 200 and y < 1650:
            draw.text((170, y), rec, fill=colors['chart_green'], font=font_body)
        y += 40
    
    # Footer
    if y < 1650:
        draw.text((350, y + 50), "— Fin del Análisis —", fill=(150,150,150), font=font_sub)
    
    # Scrollbar
    draw.rectangle([960, 280, 980, 1700], fill=(220,220,220))

def crear_frame(frame_num, escena, scroll_pos=0):
    img = Image.new('RGB', (1080, 1920), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_terminal = ImageFont.truetype(FONT, 32)
        font_title = ImageFont.truetype(FONT, 45)
        font_header = ImageFont.truetype(FONT, 35)
        font_pdf_title = ImageFont.truetype(FONT, 30)
        font_pdf_sub = ImageFont.truetype(FONT, 24)
        font_pdf_body = ImageFont.truetype(FONT, 22)
        font_chart = ImageFont.truetype(FONT, 20)
    except:
        font_terminal = font_title = font_header = font_pdf_title = font_pdf_sub = font_pdf_body = font_chart = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 1080, 80], fill=(40, 40, 40))
    draw.text((350, 20), "Claude Code Demo", fill=colors['text'], font=font_header)
    
    if escena == 'silencio':
        # Frame negro para silencio inicial
        pass
    elif escena == 'pdf_scroll':
        crear_pdf_con_graficos(draw, scroll_pos, (font_pdf_title, font_pdf_sub, font_pdf_body, font_chart))
        draw.text((400, 1750), "📊 Scrolleando análisis...", fill=colors['highlight'], font=font_title)
    else:
        y = 120
        line_height = 42
        lines = {
            'intro': [("$", colors['prompt'], 50), (" claude", colors['command'], 80), ("", 0, 50), ("🤖 Claude Code ready", colors['success'], 50)],
            'list_pdfs': [("$", colors['prompt'], 50), (" ls *.pdf", colors['command'], 80), ("", 0, 50), ("📄 informe_ventas_Q1.pdf      2.3 MB", colors['pdf'], 50), ("📄 datos_clientes_2024.pdf    5.1 MB", colors['pdf'], 50), ("📄 contratos_pendientes.pdf   1.8 MB", colors['pdf'], 50)],
            'analyze': [("$", colors['prompt'], 50), (" /analyze *.pdf", colors['command'], 80), ("", 0, 50), ("⏳ Analizando con Claude...", colors['highlight'], 50), ("  [████████████████████] 100%", colors['success'], 50)],
            'open_pdf': [("$", colors['prompt'], 50), (" open reporte.pdf", colors['command'], 80), ("", 0, 50), ("📄 Generando análisis...", colors['highlight'], 50)],
        }.get(escena, [])
        
        for line, color, x in lines:
            if line:
                draw.text((x, y), line, fill=color, font=font_terminal)
            y += line_height
    
    return img

print("🎬 RENDER FINAL v2 - Silencio + Terminal + PDF con Gráficos")

# Configuración
SILENCIO_SEG = 1
AUDIO_FILE = "demo_v2_output/audio_edu_natural.mp3"

# Obtener duración audio
result = subprocess.run(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {AUDIO_FILE}",
                       shell=True, capture_output=True, text=True)
audio_dur = float(result.stdout.strip()) if result.returncode == 0 else 11.5
total_dur = SILENCIO_SEG + audio_dur + 8  # +8s para PDF scroll extendido

print(f"⏱️  Silencio: {SILENCIO_SEG}s")
print(f"⏱️  Audio: {audio_dur:.1f}s")
print(f"⏱️  PDF scroll: 8s")
print(f"⏱️  Total: {total_dur:.1f}s")

# Generar frames
frame_count = 0

# 1. SILENCIO (1 segundo, 30 frames)
print("📦 Silencio inicial: 1s")
for _ in range(SILENCIO_SEG * FPS):
    img = crear_frame(0, 'silencio')
    img.save(f"demo_final_frames/frame_{frame_count:04d}.jpg", quality=95)
    frame_count += 1

# 2. ESCENAS CON AUDIO (distribuir proporcionalmente)
escenas = ['intro', 'list_pdfs', 'analyze', 'open_pdf']
audio_frames = int(audio_dur * FPS)
frames_por_escena = audio_frames // len(escenas)

print(f"📦 Terminal: {audio_dur:.1f}s")
for escena in escenas:
    for f in range(frames_por_escena):
        img = crear_frame(f, escena)
        img.save(f"demo_final_frames/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1

# 3. PDF SCROLL (8 segundos, extendido con gráficos)
print("📦 PDF con gráficos: 8s")
pdf_frames = 8 * FPS
for f in range(pdf_frames):
    scroll_pos = int((f / pdf_frames) * 600)
    img = crear_frame(f, 'pdf_scroll', scroll_pos)
    img.save(f"demo_final_frames/frame_{frame_count:04d}.jpg", quality=95)
    frame_count += 1

print(f"📊 Total frames: {frame_count}")

# Crear audio final (silencio + voz)
print("\n🔇 Creando audio con silencio inicial...")
os.system(f"ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t {SILENCIO_SEG} -acodec libmp3lame temp_silence.mp3 2>/dev/null")
os.system(f"ffmpeg -y -i 'concat:temp_silence.mp3|{AUDIO_FILE}' -acodec copy demo_final_output/audio_final.mp3 2>/dev/null")
os.remove('temp_silence.mp3')

# Renderizar video
print("\n🎬 Renderizando video final...")
cmd = "ffmpeg -y -framerate 30 -i demo_final_frames/frame_%04d.jpg -i demo_final_output/audio_final.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest demo_final_output/DEMO_FINAL_GRAFICOS.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('demo_final_frames')

if os.path.exists('demo_final_output/DEMO_FINAL_GRAFICOS.mp4'):
    size = os.path.getsize('demo_final_output/DEMO_FINAL_GRAFICOS.mp4') / (1024*1024)
    print(f"\n✅ VIDEO FINAL: {size:.1f} MB")
    print(f"📁 demo_final_output/DEMO_FINAL_GRAFICOS.mp4")
else:
    print("❌ Error:", result.stderr[:200])
