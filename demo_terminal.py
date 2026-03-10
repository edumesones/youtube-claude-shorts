#!/usr/bin/env python3
"""
DEMO TÉCNICO - Terminal de Claude Code analizando PDFs
Muestra comandos reales, listado de archivos, y resultado de análisis
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil

os.makedirs('demo_output', exist_ok=True)
os.makedirs('demo_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"
FONT_MONO = "fonts/Roboto-Bold.ttf"  # Terminal monospace

# COLORES TERMINAL
colors = {
    'bg': (30, 30, 30),        # Fondo terminal oscuro
    'text': (200, 200, 200),    # Texto gris claro
    'prompt': (50, 150, 50),    # Verde prompt
    'command': (255, 255, 255), # Blanco comandos
    'output': (150, 150, 150),  # Gris output
    'highlight': (230, 100, 30), # Naranja resaltado
    'pdf': (200, 50, 50),       # Rojo PDFs
    'success': (50, 200, 50),   # Verde éxito
}

def draw_terminal_line(draw, y, text, color, font, x=50):
    """Dibuja una línea de terminal"""
    draw.text((x, y), text, fill=color, font=font)

def crear_frame_demo(frame_num, escena):
    """Crea un frame de la demo de terminal"""
    img = Image.new('RGB', (1080, 1920), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_terminal = ImageFont.truetype(FONT_MONO, 32)
        font_title = ImageFont.truetype(FONT, 50)
        font_header = ImageFont.truetype(FONT, 40)
    except:
        font_terminal = font_title = font_header = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 1080, 80], fill=(40, 40, 40))
    draw.text((400, 20), "Terminal - Claude Code", fill=colors['text'], font=font_header)
    
    y = 120
    line_height = 45
    
    if escena == 'intro':
        # Escena 1: Intro y prompt
        lines = [
            ("$", colors['prompt'], 50),
            (" claude", colors['command'], 80),
            ("", colors['text'], 50),
            ("🤖 Claude Code ready", colors['success'], 50),
            ("", colors['text'], 50),
            ("Connected to:", colors['output'], 50),
            ("  • Google Drive", colors['highlight'], 50),
            ("  • Current project: /docs/analysis", colors['output'], 50),
            ("", colors['text'], 50),
            ("Type /help for commands", colors['output'], 50),
        ]
        
    elif escena == 'list_pdfs':
        # Escena 2: Listando PDFs
        lines = [
            ("$", colors['prompt'], 50),
            (" ls *.pdf", colors['command'], 80),
            ("", colors['text'], 50),
            ("📄 informe_ventas_Q1.pdf", colors['pdf'], 50),
            ("   2.3 MB | 45 páginas", colors['output'], 80),
            ("", colors['text'], 50),
            ("📄 datos_clientes_2024.pdf", colors['pdf'], 50),
            ("   5.1 MB | 120 páginas", colors['output'], 80),
            ("", colors['text'], 50),
            ("📄 contratos_pendientes.pdf", colors['pdf'], 50),
            ("   1.8 MB | 23 páginas", colors['output'], 80),
            ("", colors['text'], 50),
            ("📄 facturas_trimestre.pdf", colors['pdf'], 50),
            ("   3.4 MB | 67 páginas", colors['output'], 80),
            ("", colors['text'], 50),
            ("📄 reporte_financiero_anual.pdf", colors['pdf'], 50),
            ("   8.9 MB | 156 páginas", colors['output'], 80),
            ("", colors['text'], 50),
            ("Total: 5 archivos PDF | 21.5 MB", colors['highlight'], 50),
        ]
        
    elif escena == 'analyze_command':
        # Escena 3: Comando de análisis
        lines = [
            ("$", colors['prompt'], 50),
            (" /analyze", colors['command'], 80),
            ("", colors['text'], 50),
            ("Selecciona archivos a analizar:", colors['output'], 50),
            ("", colors['text'], 50),
            ("[✓] informe_ventas_Q1.pdf", colors['success'], 50),
            ("[✓] datos_clientes_2024.pdf", colors['success'], 50),
            ("[✓] reporte_financiero_anual.pdf", colors['success'], 50),
            ("", colors['text'], 50),
            ("Análisis solicitado:", colors['output'], 50),
            ("'Resume métricas clave y detecta", colors['command'], 50),
            (" patrones de riesgo'", colors['command'], 50),
            ("", colors['text'], 50),
            ("⏳ Analizando...", colors['highlight'], 50),
            ("  [████████████████████] 100%", colors['success'], 50),
        ]
        
    elif escena == 'results':
        # Escena 4: Resultados del análisis (REPORTE)
        lines = [
            ("📊 REPORTE DE ANÁLISIS", colors['highlight'], 50),
            ("═══════════════════════════════", colors['text'], 50),
            ("", colors['text'], 50),
            ("🎯 INSIGHTS PRINCIPALES:", colors['success'], 50),
            ("", colors['text'], 50),
            ("1. CRECIMIENTO DE VENTAS", colors['highlight'], 50),
            ("   • Q1: +23% vs año anterior", colors['output'], 50),
            ("   • Top producto: SaaS Pro", colors['output'], 50),
            ("   • Clientes nuevos: 156", colors['output'], 50),
            ("", colors['text'], 50),
            ("2. ALERTAS DETECTADAS", colors['highlight'], 50),
            ("   ⚠️  3 contratos expiran en <30 días", colors['pdf'], 50),
            ("   ⚠️  Churn rate subió al 8%", colors['pdf'], 50),
            ("", colors['text'], 50),
            ("3. RECOMENDACIONES", colors['highlight'], 50),
            ("   ✓ Renovar contratos críticos", colors['success'], 50),
            ("   ✓ Focus en retención B2B", colors['success'], 50),
            ("   ✓ Aumentar marketing sector enterprise", colors['success'], 50),
        ]
        
    elif escena == 'export':
        # Escena 5: Exportar resultado
        lines = [
            ("✅ Análisis completado en 4.2 segundos", colors['success'], 50),
            ("", colors['text'], 50),
            ("$", colors['prompt'], 50),
            (" /export report", colors['command'], 80),
            ("", colors['text'], 50),
            ("Formatos disponibles:", colors['output'], 50),
            ("  [1] PDF Report", colors['highlight'], 50),
            ("  [2] Excel Dashboard", colors['output'], 50),
            ("  [3] Notion Page", colors['output'], 50),
            ("  [4] Slack Summary", colors['output'], 50),
            ("", colors['text'], 50),
            ("Seleccionado: PDF Report", colors['highlight'], 50),
            ("", colors['text'], 50),
            ("📄 reporte_analisis_2024.pdf generado", colors['success'], 50),
            ("   📥 Descargar: [Click aquí]", colors['highlight'], 50),
            ("", colors['text'], 50),
            ("⏱️  Tiempo ahorrado: ~3 horas", colors['highlight'], 50),
        ]
    
    # Dibujar líneas
    for line, color, x in lines:
        draw_terminal_line(draw, y, line, color, font_terminal, x)
        y += line_height
        if y > 1800:
            break
    
    # Cursor parpadeante (última línea)
    if frame_num % 30 < 15:  # Parpadea cada medio segundo
        draw.rectangle([50, y, 70, y+30], fill=colors['text'])
    
    return img

print("="*60)
print("🎬 DEMO TÉCNICO - Terminal Claude Code")
print("="*60)

# Generar escenas
ESCENAS = [
    ('intro', 90),        # 3s
    ('list_pdfs', 120),   # 4s
    ('analyze_command', 120),  # 4s
    ('results', 150),     # 5s
    ('export', 120),      # 4s
]

frame_count = 0
FPS = 30

for escena, num_frames in ESCENAS:
    print(f"\n📦 Escena: {escena} ({num_frames//FPS}s)")
    for f in range(num_frames):
        img = crear_frame_demo(f, escena)
        img.save(f"demo_frames/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1
    print(f"   ✅ {frame_count} frames totales")

print(f"\n📊 Total: {frame_count} frames ({frame_count//FPS}s)")

# Audio
print("\n🎙️ Generando audio...")
audio_texto = "Voy a analizar cinco PDFs de informes financieros. Primero listo los archivos. Luego ejecuto el análisis con un comando. En segundos, Claude extrae métricas clave, detecta tres alertas importantes y genera recomendaciones accionables. Todo exportado a un reporte PDF listo para compartir."

os.system(f"""python3 -c "
import sys
sys.path.insert(0, 'src')
from generate_voice import generate_voice
generate_voice('{audio_texto}', 'demo_output/audio_demo.mp3', voice='es-ES-AlvaroNeural')
" 2>/dev/null""")

# Renderizar
print("\n🎬 Renderizando demo...")
cmd = "ffmpeg -y -framerate 30 -i demo_frames/frame_%04d.jpg -i demo_output/audio_demo.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest demo_output/DEMO_TERMINAL.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('demo_frames')

if os.path.exists('demo_output/DEMO_TERMINAL.mp4'):
    size = os.path.getsize('demo_output/DEMO_TERMINAL.mp4') / (1024*1024)
    print(f"\n" + "="*60)
    print("✅ DEMO TÉRMINAL COMPLETADO")
    print("="*60)
    print(f"📁 demo_output/DEMO_TERMINAL.mp4")
    print(f"💾 {size:.1f} MB")
    print(f"⏱️  {frame_count//FPS} segundos")
    print(f"🖥️  5 escenas de terminal")
    print(f"📄 Listado de PDFs + Análisis + Reporte")
    print("="*60)
else:
    print("❌ Error:", result.stderr[:300])
