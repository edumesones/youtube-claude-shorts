#!/usr/bin/env python3
"""
RENDER FINAL v3 - VERSIÓN NO TÉCNICA
Lenguaje natural para público general (no desarrolladores)
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil

os.makedirs('demo_natural_output', exist_ok=True)
os.makedirs('demo_natural_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"
FPS = 30

colors = {
    'bg': (30, 30, 30), 'text': (200, 200, 200),
    'highlight': (230, 100, 30), 'success': (50, 200, 50),
    'pdf_bg': (255, 255, 255), 'pdf_text': (50, 50, 50),
    'chat_user': (50, 100, 200), 'chat_ai': (50, 150, 50),
}

def draw_chat_bubble(draw, x, y, w, h, color, text, font, is_ai=True):
    """Dibuja burbuja de chat tipo WhatsApp/Claude"""
    # Burbuja redondeada
    r = 20
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=color)
    
    # Pico de la burbuja
    if is_ai:
        draw.polygon([(x-15, y+20), (x, y+10), (x, y+30)], fill=color)
    else:
        draw.polygon([(x+w, y+10), (x+w+15, y+20), (x+w, y+30)], fill=color)
    
    # Texto
    draw.text((x+20, y+15), text, fill=(255,255,255), font=font)

def draw_chart_bars(draw, x, y, values, colors_list, labels, font):
    bar_width, spacing, max_val = 60, 20, max(values)
    for i, (val, col, label) in enumerate(zip(values, colors_list, labels)):
        bar_h = int((val / max_val) * 120)
        bar_x, bar_y = x + i * (bar_width + spacing), y + 120 - bar_h
        draw.rectangle([bar_x, bar_y, bar_x+bar_width, y+120], fill=col, outline=(0,0,0))
        draw.text((bar_x+5, bar_y-20), f"{val}%", fill=(0,0,0), font=font)
        draw.text((bar_x, y+130), label, fill=(100,100,100), font=font)

def crear_pdf_con_graficos(draw, scroll_pos, fonts):
    font_title, font_sub, font_body, font_chart = fonts
    
    # Fondo PDF
    draw.rectangle([80, 180, 1000, 1750], fill=colors['pdf_bg'], outline=(200,200,200), width=3)
    draw.rectangle([80, 180, 1000, 270], fill=(240,240,240))
    draw.text((120, 200), "📊 TU ANÁLISIS FINANCIERO - Q1 2024", fill=(13,13,13), font=font_title)
    draw.text((120, 240), "Generado automáticamente por IA", fill=(100,100,100), font=font_sub)
    
    y = 300 - scroll_pos
    
    # KPIs
    if y > 200:
        draw.text((120, y), "RESUMEN EJECUTIVO", fill=colors['chat_ai'], font=font_sub)
    y += 50
    
    kpis = [("💰 Ventas", "+23%", (50,150,50)), ("👥 Clientes nuevos", "156", (50,100,200)), ("📈 Retención", "92%", (230,150,30))]
    for i, (label, val, col) in enumerate(kpis):
        x = 120 + i * 290
        if y > 200:
            draw.rounded_rectangle([x, y, x+270, y+90], radius=12, fill=col)
            draw.text((x+15, y+15), label, fill=(255,255,255), font=font_body)
            draw.text((x+15, y+50), val, fill=(255,255,255), font=font_title)
    y += 120
    
    # Gráfico barras
    if y > 200:
        draw.text((120, y), "CRECIMIENTO POR TRIMESTRE", fill=(13,13,13), font=font_sub)
    y += 50
    if y > 100:
        draw_chart_bars(draw, 150, y, [15, 18, 23, 28], [(230,100,30), (50,100,200), (50,150,50), (50,100,200)], ['Q1', 'Q2', 'Q3', 'Q4'], font_chart)
    y += 200
    
    # Gráfico circular simplificado
    if y > 200:
        draw.text((120, y), "DE DÓNDE VIENEN TUS INGRESOS", fill=(13,13,13), font=font_sub)
    y += 50
    if y > 100:
        # Simulado con rectángulos coloridos
        ingresos = [("SaaS - 45%", (50,100,200)), ("Servicios - 30%", (50,150,50)), ("Otros - 25%", (230,100,30))]
        for i, (txt, col) in enumerate(ingresos):
            draw.rounded_rectangle([150, y + i*50, 190, y + i*50 + 35], radius=5, fill=col)
            draw.text((210, y + i*50 + 5), txt, fill=(0,0,0), font=font_body)
    y += 200
    
    # Alertas
    if y > 200:
        draw.text((120, y), "⚠️  ALERTAS IMPORTANTES", fill=(200,50,50), font=font_sub)
    y += 50
    alertas = [
        "3 contratos importantes expiran este mes",
        "Algunos clientes están tardando más en pagar",
        "El sector retail está perdiendo interés",
    ]
    for alerta in alertas:
        if y > 200 and y < 1680:
            draw.text((140, y), "• " + alerta, fill=(200,50,50), font=font_body)
        y += 45
    
    # Recomendaciones
    y += 30
    if y > 200:
        draw.text((120, y), "✅ QUÉ HACER AHORA", fill=(50,150,50), font=font_sub)
    y += 50
    recs = [
        "Renovar contratos antes de que expiren",
        "Llamar a clientes con pagos pendientes",
        "Crear campaña para retener clientes",
    ]
    for rec in recs:
        if y > 200 and y < 1680:
            draw.text((140, y), "→ " + rec, fill=(50,150,50), font=font_body)
        y += 45
    
    if y < 1680:
        draw.text((350, y + 40), "— Reporte completo —", fill=(150,150,150), font=font_sub)

def crear_frame(frame_num, escena, scroll_pos=0):
    img = Image.new('RGB', (1080, 1920), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_chat = ImageFont.truetype(FONT, 32)
        font_title = ImageFont.truetype(FONT, 45)
        font_header = ImageFont.truetype(FONT, 35)
        font_pdf_title = ImageFont.truetype(FONT, 28)
        font_pdf_sub = ImageFont.truetype(FONT, 24)
        font_pdf_body = ImageFont.truetype(FONT, 22)
        font_chart = ImageFont.truetype(FONT, 20)
    except:
        font_chat = font_title = font_header = font_pdf_title = font_pdf_sub = font_pdf_body = font_chart = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 1080, 80], fill=(40, 40, 40))
    draw.text((350, 20), "Claude - Tu Asistente de IA", fill=colors['text'], font=font_header)
    
    if escena == 'silencio':
        pass  # Frame negro
        
    elif escena == 'intro':
        # Chat: Usuario pregunta
        draw_chat_bubble(draw, 100, 150, 500, 70, colors['chat_user'], 
                        "Hola Claude, tengo muchos documentos\npara analizar...", font_chat, is_ai=False)
        # Chat: AI responde
        draw_chat_bubble(draw, 350, 250, 550, 70, colors['chat_ai'],
                        "¡Perfecto! Déjame ayudarte.\n¿Cuántos archivos tienes?", font_chat, is_ai=True)
        
    elif escena == 'list_docs':
        draw_chat_bubble(draw, 100, 150, 520, 120, colors['chat_user'],
                        "Tengo 5 informes:\n• Ventas Q1\n• Clientes 2024\n• Contratos\n• Facturas\n• Reporte anual", font_chat, is_ai=False)
        draw_chat_bubble(draw, 350, 300, 550, 60, colors['chat_ai'],
                        "Entendido. Los analizo ahora...", font_chat, is_ai=True)
        
    elif escena == 'analyze':
        draw_chat_bubble(draw, 350, 150, 550, 80, colors['chat_ai'],
                        "⏳ Analizando documentos...\nBuscando patrones y alertas", font_chat, is_ai=True)
        # Barra de progreso
        draw.rectangle([350, 250, 900, 280], fill=(60,60,60), outline=(100,100,100))
        draw.rectangle([350, 250, 900, 280], fill=colors['success'])
        draw.text((550, 300), "¡Análisis completo!", fill=colors['success'], font=font_title)
        
    elif escena == 'results':
        draw_chat_bubble(draw, 350, 150, 580, 100, colors['chat_ai'],
                        "✅ Listo. He encontrado:\n• Ventas crecieron 23%\n• 156 clientes nuevos\n• 3 alertas importantes\n\n¿Quieres ver el informe?", font_chat, is_ai=True)
        draw_chat_bubble(draw, 100, 280, 300, 50, colors['chat_user'],
                        "¡Sí, por favor!", font_chat, is_ai=False)
        
    elif escena == 'open_pdf':
        draw_chat_bubble(draw, 350, 150, 550, 60, colors['chat_ai'],
                        "Aquí tienes tu informe completo:", font_chat, is_ai=True)
        draw.rectangle([200, 230, 880, 400], fill=(255,255,255), outline=colors['highlight'], width=3)
        draw.text((250, 260), "📊 reporte_q1_2024.pdf", fill=(13,13,13), font=font_title)
        draw.text((250, 320), "Generado en 4.2 segundos", fill=(100,100,100), font=font_chat)
        
    elif escena == 'pdf_scroll':
        crear_pdf_con_graficos(draw, scroll_pos, (font_pdf_title, font_pdf_sub, font_pdf_body, font_chart))
        draw.text((350, 1780), "📜 Scrolleando tu informe...", fill=colors['highlight'], font=font_title)
    
    return img

print("🎬 RENDER V3 - LENGUAJE NATURAL (No técnico)")

AUDIO_FILE = "demo_v2_output/audio_edu_natural.mp3"
result = subprocess.run(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {AUDIO_FILE}",
                       shell=True, capture_output=True, text=True)
audio_dur = float(result.stdout.strip()) if result.returncode == 0 else 11.5

SILENCIO_SEG = 1
PDF_SCROLL_SEG = 10  # Más tiempo para ver el PDF
total_dur = SILENCIO_SEG + audio_dur + PDF_SCROLL_SEG

print(f"⏱️  Silencio: {SILENCIO_SEG}s | Audio: {audio_dur:.1f}s | PDF: {PDF_SCROLL_SEG}s | Total: {total_dur:.1f}s")

# Generar frames
frame_count = 0

# Silencio
print("📦 Silencio inicial...")
for _ in range(SILENCIO_SEG * FPS):
    img = crear_frame(0, 'silencio')
    img.save(f"demo_natural_frames/frame_{frame_count:04d}.jpg", quality=95)
    frame_count += 1

# Escenas con audio
escenas = ['intro', 'list_docs', 'analyze', 'results', 'open_pdf']
audio_frames = int(audio_dur * FPS)
frames_por_escena = audio_frames // len(escenas)

print("📦 Escenas de conversación...")
for escena in escenas:
    for f in range(frames_por_escena):
        img = crear_frame(f, escena)
        img.save(f"demo_natural_frames/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1

# PDF scroll extendido
print("📦 PDF con gráficos (scroll lento)...")
pdf_frames = PDF_SCROLL_SEG * FPS
for f in range(pdf_frames):
    scroll_pos = int((f / pdf_frames) * 700)
    img = crear_frame(f, 'pdf_scroll', scroll_pos)
    img.save(f"demo_natural_frames/frame_{frame_count:04d}.jpg", quality=95)
    frame_count += 1

print(f"📊 {frame_count} frames generados")

# Audio con silencio
print("🔇 Creando audio final...")
os.system(f"ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t {SILENCIO_SEG} -acodec libmp3lame temp_sil.mp3 2>/dev/null")
os.system(f"ffmpeg -y -i 'concat:temp_sil.mp3|{AUDIO_FILE}' -acodec copy demo_natural_output/audio_final.mp3 2>/dev/null")
os.remove('temp_sil.mp3')

# Renderizar
print("🎬 Renderizando...")
cmd = "ffmpeg -y -framerate 30 -i demo_natural_frames/frame_%04d.jpg -i demo_natural_output/audio_final.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest demo_natural_output/DEMO_LENGUAJE_NATURAL.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('demo_natural_frames')

if os.path.exists('demo_natural_output/DEMO_LENGUAJE_NATURAL.mp4'):
    size = os.path.getsize('demo_natural_output/DEMO_LENGUAJE_NATURAL.mp4') / (1024*1024)
    print(f"\n✅ VIDEO NATURAL: {size:.1f} MB")
    print(f"📁 demo_natural_output/DEMO_LENGUAJE_NATURAL.mp4")
else:
    print("❌ Error:", result.stderr[:300])
