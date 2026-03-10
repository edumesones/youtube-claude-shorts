#!/usr/bin/env python3
"""
RENDER FINAL - Video con voz Edu NATURAL
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil

os.makedirs('demo_v2_output', exist_ok=True)
os.makedirs('demo_v2_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"

colors = {
    'bg': (30, 30, 30), 'text': (200, 200, 200),
    'prompt': (50, 150, 50), 'command': (255, 255, 255),
    'output': (150, 150, 150), 'highlight': (230, 100, 30),
    'pdf': (200, 50, 50), 'success': (50, 200, 50),
    'pdf_bg': (255, 255, 255), 'pdf_text': (50, 50, 50),
}

def crear_frame(frame_num, escena, scroll_pos=0):
    img = Image.new('RGB', (1080, 1920), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_terminal = ImageFont.truetype(FONT, 32)
        font_title = ImageFont.truetype(FONT, 45)
        font_header = ImageFont.truetype(FONT, 35)
        font_pdf_title = ImageFont.truetype(FONT, 28)
        font_pdf_body = ImageFont.truetype(FONT, 24)
    except:
        font_terminal = font_title = font_header = font_pdf_title = font_pdf_body = ImageFont.load_default()
    
    draw.rectangle([0, 0, 1080, 80], fill=(40, 40, 40))
    draw.text((350, 20), "Claude Code Demo", fill=colors['text'], font=font_header)
    
    if escena == 'pdf_scroll':
        draw.rectangle([100, 200, 980, 1700], fill=colors['pdf_bg'], outline=(200,200,200), width=2)
        draw.rectangle([100, 200, 980, 280], fill=(240,240,240))
        draw.text((150, 220), "📊 REPORTE DE ANÁLISIS FINANCIERO", fill=(13,13,13), font=font_pdf_title)
        draw.text((150, 260), "Generado por Claude Code • Marzo 2024", fill=(100,100,100), font=font_pdf_body)
        
        y_start = 320 - scroll_pos
        contenido = [
            ("", 0), ("1. RESUMEN EJECUTIVO", 30), ("", 0),
            ("Este informe presenta el análisis completo de", 0),
            ("los documentos financieros del Q1 2024.", 0), ("", 0),
            ("2. MÉTRICAS CLAVE", 30), ("", 0),
            ("   • Crecimiento de ventas: +23%", 0),
            ("   • Nuevos clientes: 156", 0),
            ("   • Tasa de retención: 92%", 0), ("", 0),
            ("3. ALERTAS IDENTIFICADAS", 30), ("", 0),
            ("   ⚠️  3 contratos expiran en <30 días", 0),
            ("   ⚠️  Churn rate subió al 8%", 0), ("", 0),
            ("4. RECOMENDACIONES", 30), ("", 0),
            ("   ✓ Renovar contratos críticos", 0),
            ("   ✓ Focus en retención B2B", 0), ("", 0),
            ("— Fin del reporte —", 0),
        ]
        line_height = 35
        for texto, indent in contenido:
            if texto:
                x_pos, y_pos = 150 + indent, y_start
                if 280 < y_pos < 1650:
                    draw.text((x_pos, y_pos), texto, fill=colors['pdf_text'], font=font_pdf_body)
            y_start += line_height
        draw.text((400, 1750), "📜 Scrolleando PDF...", fill=colors['highlight'], font=font_title)
    else:
        y = 120
        line_height = 42
        lines = {
            'intro': [
                ("$", colors['prompt'], 50), (" claude", colors['command'], 80),
                ("", 0, 50), ("🤖 Claude Code ready", colors['success'], 50),
            ],
            'list_pdfs': [
                ("$", colors['prompt'], 50), (" ls *.pdf", colors['command'], 80),
                ("", 0, 50),
                ("📄 informe_ventas_Q1.pdf      2.3 MB  45p", colors['pdf'], 50),
                ("📄 datos_clientes_2024.pdf    5.1 MB 120p", colors['pdf'], 50),
                ("📄 contratos_pendientes.pdf   1.8 MB  23p", colors['pdf'], 50),
            ],
            'analyze': [
                ("$", colors['prompt'], 50), (" /analyze *.pdf", colors['command'], 80),
                ("", 0, 50), ("⏳ Analizando con Claude...", colors['highlight'], 50),
                ("  [████████████████████] 100%", colors['success'], 50),
            ],
            'open_pdf': [
                ("$", colors['prompt'], 50), (" open reporte.pdf", colors['command'], 80),
                ("", 0, 50), ("📄 Abriendo reporte...", colors['highlight'], 50),
            ],
        }.get(escena, [])
        
        for line, color, x in lines:
            if line:
                draw.text((x, y), line, fill=color, font=font_terminal)
            y += line_height
        if frame_num % 30 < 15:
            draw.rectangle([50, y, 70, y+25], fill=colors['text'])
    
    return img

print("🎬 RENDERIZANDO VIDEO CON VOZ NATURAL...")

# Obtener duración del audio natural
result = subprocess.run(
    "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 demo_v2_output/audio_edu_natural.mp3",
    shell=True, capture_output=True, text=True
)
duracion = float(result.stdout.strip()) if result.returncode == 0 else 11.5
print(f"⏱️  Duración audio: {duracion:.1f}s")

# Distribuir escenas proporcionalmente
total_frames = int(duracion * 30)
escenas_frames = [30, 50, 50, 30, total_frames - 160]  # pdf_scroll toma el resto

frame_count = 0
for escena, num_frames in zip(['intro', 'list_pdfs', 'analyze', 'open_pdf', 'pdf_scroll'], escenas_frames):
    print(f"📦 {escena}: {num_frames//30}s")
    for f in range(max(0, num_frames)):
        scroll_pos = int((f / max(1, num_frames)) * 400) if escena == 'pdf_scroll' else 0
        img = crear_frame(f, escena, scroll_pos)
        img.save(f"demo_v2_frames/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1

print(f"📊 {frame_count} frames")

# Renderizar
cmd = "ffmpeg -y -framerate 30 -i demo_v2_frames/frame_%04d.jpg -i demo_v2_output/audio_edu_natural.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest demo_v2_output/DEMO_VOZ_NATURAL.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('demo_v2_frames')

if os.path.exists('demo_v2_output/DEMO_VOZ_NATURAL.mp4'):
    size = os.path.getsize('demo_v2_output/DEMO_VOZ_NATURAL.mp4') / (1024*1024)
    print(f"✅ VIDEO NATURAL: {size:.1f} MB")
else:
    print("❌ Error")
