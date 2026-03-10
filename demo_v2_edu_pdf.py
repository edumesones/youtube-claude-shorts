#!/usr/bin/env python3
"""
DEMO TÉCNICO v2 - Con voz Edu REAL + PDF con scroll al final
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil
import requests

os.makedirs('demo_v2_output', exist_ok=True)
os.makedirs('demo_v2_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"

# CONFIGURACIÓN ELEVENLABS - VOZ EDU
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')
VOICE_ID = 'edus'

def generar_voz_edus(texto, output_path):
    """Genera audio con voz clonada de Edu"""
    if not ELEVENLABS_API_KEY:
        print("⚠️  Usando voz alternativa (edge-tts)")
        from src.generate_voice import generate_voice
        generate_voice(texto, output_path, voice='es-ES-AlvaroNeural')
        return
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    
    print(f"🎙️ Generando voz con 'edus'...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"   ✅ Voz Edu generada")
    else:
        print(f"   ⚠️  Error ElevenLabs, usando alternativa")
        from src.generate_voice import generate_voice
        generate_voice(texto, output_path, voice='es-ES-AlvaroNeural')

# COLORES
colors = {
    'bg': (30, 30, 30),
    'text': (200, 200, 200),
    'prompt': (50, 150, 50),
    'command': (255, 255, 255),
    'output': (150, 150, 150),
    'highlight': (230, 100, 30),
    'pdf': (200, 50, 50),
    'success': (50, 200, 50),
    'pdf_bg': (255, 255, 255),
    'pdf_text': (50, 50, 50),
}

def draw_terminal_line(draw, y, text, color, font, x=50):
    draw.text((x, y), text, fill=color, font=font)

def crear_pdf_visual(draw, font_title, font_body, scroll_offset=0):
    """Dibuja un PDF de reporte con contenido realista"""
    # Fondo PDF
    draw.rectangle([100, 200, 980, 1700], fill=colors['pdf_bg'], outline=(200,200,200), width=2)
    
    # Header PDF
    draw.rectangle([100, 200, 980, 280], fill=(240,240,240))
    draw.text((150, 220), "📊 REPORTE DE ANÁLISIS FINANCIERO", fill=(13,13,13), font=font_title)
    draw.text((150, 260), "Generado por Claude Code • Marzo 2024", fill=(100,100,100), font=font_body)
    
    # Contenido del PDF (con scroll)
    y_start = 320 - scroll_offset
    
    contenido = [
        ("", 0),
        ("1. RESUMEN EJECUTIVO", 30),
        ("", 0),
        ("Este informe presenta el análisis completo de", 0),
        ("los documentos financieros del Q1 2024.", 0),
        ("", 0),
        ("2. MÉTRICAS CLAVE", 30),
        ("", 0),
        ("   • Crecimiento de ventas: +23%", 0),
        ("   • Nuevos clientes: 156", 0),
        ("   • Tasa de retención: 92%", 0),
        ("   • Ingresos totales: $2.4M", 0),
        ("", 0),
        ("3. ALERTAS IDENTIFICADAS", 30),
        ("", 0),
        ("   ⚠️  Contrato Enterprise vence en 15 días", 0),
        ("   ⚠️  Pago pendiente Cliente ABC: $45K", 0),
        ("   ⚠️  Churn rate aumentó 2% en sector retail", 0),
        ("", 0),
        ("4. RECOMENDACIONES", 30),
        ("", 0),
        ("   ✓ Renegociar contratos críticos antes del", 0),
        ("     cierre del mes", 0),
        ("   ✓ Implementar campaña de retención para", 0),
        ("     clientes enterprise", 0),
        ("   ✓ Aumentar presupuesto marketing B2B", 0),
        ("     (ROI proyectado: 340%)", 0),
        ("", 0),
        ("5. CONCLUSIONES", 30),
        ("", 0),
        ("El análisis revela un crecimiento sólido con", 0),
        ("algunas áreas que requieren atención inmediata.", 0),
        ("Se recomienda revisión semanal de métricas.", 0),
        ("", 0),
        ("Tiempo de análisis: 4.2 segundos", 0),
        ("Documentos procesados: 5 PDFs", 0),
        ("Páginas analizadas: 411", 0),
        ("", 0),
        ("— Fin del reporte —", 0),
    ]
    
    line_height = 35
    for texto, indent in contenido:
        if texto:
            x_pos = 150 + indent
            y_pos = y_start
            if 280 < y_pos < 1650:  # Solo dibujar si está visible
                draw.text((x_pos, y_pos), texto, fill=colors['pdf_text'], font=font_body)
        y_start += line_height
    
    # Scroll bar
    draw.rectangle([960, 280, 980, 1700], fill=(220,220,220))
    thumb_pos = 280 + (scroll_offset / 800) * 1400  # Aproximado
    draw.rectangle([960, int(thumb_pos), 980, int(thumb_pos)+100], fill=(150,150,150))

def crear_frame_demo_v2(frame_num, escena, scroll_pos=0):
    """Crea frame de la demo"""
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
    
    # Header
    draw.rectangle([0, 0, 1080, 80], fill=(40, 40, 40))
    draw.text((350, 20), "Claude Code Demo", fill=colors['text'], font=font_header)
    
    if escena == 'pdf_scroll':
        # Escena especial: PDF con scroll
        crear_pdf_visual(draw, font_pdf_title, font_pdf_body, scroll_pos)
        
        # Indicador de scroll
        draw.text((400, 1750), "📜 Scrolleando PDF...", fill=colors['highlight'], font=font_title)
        
    else:
        # Terminal normal
        y = 120
        line_height = 42
        
        if escena == 'intro':
            lines = [
                ("$", colors['prompt'], 50), (" claude", colors['command'], 80),
                ("", 0, 50),
                ("🤖 Claude Code ready", colors['success'], 50),
                ("", 0, 50), ("Connected to:", colors['output'], 50),
                ("  • Google Drive ✓", colors['highlight'], 50),
                ("", 0, 50), ("Type /help for commands", colors['output'], 50),
            ]
        elif escena == 'list_pdfs':
            lines = [
                ("$", colors['prompt'], 50), (" ls *.pdf", colors['command'], 80),
                ("", 0, 50),
                ("📄 informe_ventas_Q1.pdf      2.3 MB  45p", colors['pdf'], 50),
                ("📄 datos_clientes_2024.pdf    5.1 MB 120p", colors['pdf'], 50),
                ("📄 contratos_pendientes.pdf   1.8 MB  23p", colors['pdf'], 50),
                ("📄 facturas_trimestre.pdf     3.4 MB  67p", colors['pdf'], 50),
                ("📄 reporte_financiero.pdf     8.9 MB 156p", colors['pdf'], 50),
                ("", 0, 50), ("Total: 21.5 MB | 411 páginas", colors['highlight'], 50),
            ]
        elif escena == 'analyze':
            lines = [
                ("$", colors['prompt'], 50), (" /analyze *.pdf", colors['command'], 80),
                ("", 0, 50), ("Seleccionados: 5 archivos", colors['output'], 50),
                ("", 0, 50), ("Prompt: 'Resume métricas clave'", colors['command'], 50),
                ("", 0, 50), ("⏳ Analizando con Claude...", colors['highlight'], 50),
                ("  [████████████████████] 100%", colors['success'], 50),
                ("", 0, 50), ("✅ Análisis completado", colors['success'], 50),
            ]
        elif escena == 'open_pdf':
            lines = [
                ("$", colors['prompt'], 50), (" open reporte.pdf", colors['command'], 80),
                ("", 0, 50), ("📄 Abriendo reporte_analisis.pdf...", colors['highlight'], 50),
                ("", 0, 50), ("✅ Documento listo para visualizar", colors['success'], 50),
                ("", 0, 50), ("🖱️  Iniciando scroll automático...", colors['output'], 50),
            ]
        
        for line, color, x in lines:
            if line:
                draw_terminal_line(draw, y, line, color, font_terminal, x)
            y += line_height
            if y > 1800:
                break
        
        # Cursor
        if frame_num % 30 < 15:
            draw.rectangle([50, y, 70, y+25], fill=colors['text'])
    
    return img

print("="*60)
print("🎬 DEMO TÉCNICO v2 - Voz Edu + PDF Real con Scroll")
print("="*60)

# Generar voz con Edu
print("\n🎙️ Generando voz con 'edus'...")
audio_texto = "Voy a analizar estos cinco PDFs financieros. Primero los listo, luego ejecuto el análisis con Claude. En segundos, extrae todas las métricas. Y aquí está el reporte completo, listo para revisar."
generar_voz_edus(audio_texto, 'demo_v2_output/audio_edu.mp3')

# Generar frames
ESCENAS = [
    ('intro', 60),
    ('list_pdfs', 90),
    ('analyze', 90),
    ('open_pdf', 60),
]

frame_count = 0
FPS = 30

for escena, num_frames in ESCENAS:
    print(f"\n📦 {escena}: {num_frames//FPS}s")
    for f in range(num_frames):
        img = crear_frame_demo_v2(f, escena)
        img.save(f"demo_v2_frames/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1

# Escena especial: PDF con scroll (6 segundos)
print(f"\n📄 PDF con scroll: 6s")
scroll_frames = 6 * FPS
for f in range(scroll_frames):
    scroll_pos = int((f / scroll_frames) * 600)  # Scroll gradual
    img = crear_frame_demo_v2(f, 'pdf_scroll', scroll_pos)
    img.save(f"demo_v2_frames/frame_{frame_count:04d}.jpg", quality=95)
    frame_count += 1

print(f"\n📊 Total: {frame_count} frames ({frame_count//FPS}s)")

# Renderizar
print("\n🎬 Renderizando...")
cmd = "ffmpeg -y -framerate 30 -i demo_v2_frames/frame_%04d.jpg -i demo_v2_output/audio_edu.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest demo_v2_output/DEMO_VOZ_EDU_PDF.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('demo_v2_frames')

if os.path.exists('demo_v2_output/DEMO_VOZ_EDU_PDF.mp4'):
    size = os.path.getsize('demo_v2_output/DEMO_VOZ_EDU_PDF.mp4') / (1024*1024)
    print(f"\n✅ DEMO COMPLETADO: {size:.1f} MB")
else:
    print("❌ Error")
