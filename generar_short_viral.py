#!/usr/bin/env python3
"""
GENERADOR DE SHORT VIRAL - Estilo TikTok/YouTube Shorts
Ritmo rápido, múltiples escenas, texto impactante
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil
from pathlib import Path

os.makedirs('viral_output', exist_ok=True)
os.makedirs('viral_frames', exist_ok=True)

FONT = "fonts/Roboto-Bold.ttf"

# ESTRUCTURA DEL SHORT VIRAL
# Hook (2s) -> Problema (3s) -> Solución (4s) -> Demo (4s) -> CTA (3s) = 16s total
ESCENAS = [
    {
        'tipo': 'HOOK',
        'duracion': 2,
        'texto': '¿40 HORAS?',
        'sub': 'Así las ahorro',
        'color': (255, 50, 50),  # Rojo impactante
        'efecto': 'zoom_in',
    },
    {
        'tipo': 'PROBLEMA', 
        'duracion': 3,
        'texto': '20+ PDFs',
        'sub': 'Sin analizar',
        'color': (200, 50, 50),
        'efecto': 'shake',
    },
    {
        'tipo': 'SOLUCIÓN',
        'duracion': 4,
        'texto': 'CLAUDE',
        'sub': '+ Google Drive',
        'color': (50, 150, 50),
        'efecto': 'slide',
    },
    {
        'tipo': 'DEMO',
        'duracion': 4,
        'texto': '1 CLICK',
        'sub': 'Y listo',
        'color': (50, 100, 200),
        'efecto': 'pulse',
    },
    {
        'tipo': 'CTA',
        'duracion': 3,
        'texto': 'GRATIS',
        'sub': 'Prueba ahora →',
        'color': (255, 150, 0),
        'efecto': 'bounce',
    },
]

FPS = 30

print("="*60)
print("🎬 GENERANDO SHORT VIRAL")
print("="*60)

frame_count = 0

for escena in ESCENAS:
    num_frames = escena['duracion'] * FPS
    print(f"\n📦 {escena['tipo']}: {escena['duracion']}s ({num_frames} frames)")
    
    for f in range(num_frames):
        # Progreso de la animación (0.0 a 1.0)
        progreso = f / num_frames
        
        # Crear imagen base
        img = Image.new('RGB', (1080, 1920), (13, 13, 13))  # Fondo oscuro
        draw = ImageDraw.Draw(img)
        
        try:
            font_grande = ImageFont.truetype(FONT, 200)
            font_sub = ImageFont.truetype(FONT, 80)
            font_mini = ImageFont.truetype(FONT, 40)
        except:
            font_grande = font_sub = font_mini = ImageFont.load_default()
        
        # === EFECTOS VISUALES ===
        
        # Efecto ZOOM IN
        if escena['efecto'] == 'zoom_in':
            scale = 1.0 + (progreso * 0.3)  # 1.0 a 1.3
            # Simulado cambiando tamaño de fuente
            size = int(200 * scale)
            try:
                font_dynamic = ImageFont.truetype(FONT, size)
            except:
                font_dynamic = font_grande
        else:
            font_dynamic = font_grande
        
        # Efecto SHAKE (vibración)
        shake_x, shake_y = 0, 0
        if escena['efecto'] == 'shake':
            import random
            shake_x = random.randint(-10, 10)
            shake_y = random.randint(-10, 10)
        
        # Efecto SLIDE (deslizar)
        slide_x = 0
        if escena['efecto'] == 'slide':
            if progreso < 0.3:
                slide_x = int(200 * (1 - progreso/0.3))  # Entra
            elif progreso > 0.7:
                slide_x = int(-200 * ((progreso-0.7)/0.3))  # Sale
        
        # Efecto PULSE (latido)
        pulse = 1.0
        if escena['efecto'] == 'pulse':
            pulse = 1.0 + 0.1 * (0.5 - abs(progreso - 0.5)) * 2
        
        # Efecto BOUNCE (rebote)
        bounce_y = 0
        if escena['efecto'] == 'bounce':
            if progreso < 0.3:
                bounce_y = -int(50 * (1 - progreso/0.3))
        
        # === DIBUJAR TEXTO PRINCIPAL ===
        bbox = draw.textbbox((0,0), escena['texto'], font=font_dynamic)
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        x = (1080 - w) // 2 + shake_x + slide_x
        y = 600 + shake_y + bounce_y
        
        # Glow effect (múltiples capas)
        for offset in [15, 10, 5]:
            alpha = int(255 * (1 - offset/20))
            glow_color = tuple(min(255, c + 50) for c in escena['color'])
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    draw.text((x+dx, y+dy), escena['texto'], font=font_dynamic, fill=glow_color)
        
        # Texto principal
        draw.text((x, y), escena['texto'], font=font_dynamic, fill=escena['color'])
        
        # === SUBTÍTULO ===
        bbox = draw.textbbox((0,0), escena['sub'], font=font_sub)
        w = bbox[2]-bbox[0]
        x_sub = (1080 - w) // 2 + shake_x
        y_sub = 900 + shake_y
        draw.text((x_sub, y_sub), escena['sub'], font=font_sub, fill=(255,255,255))
        
        # === BARRA DE PROGRESO (abajo) ===
        bar_y = 1800
        draw.rectangle([100, bar_y, 980, bar_y+20], fill=(50,50,50), outline=(100,100,100))
        progreso_total = frame_count / (16 * FPS)  # Progreso total del video
        bar_width = int(880 * progreso_total)
        draw.rectangle([100, bar_y, 100+bar_width, bar_y+20], fill=escena['color'])
        
        # === CONTADOR ===
        draw.text((50, 50), f"{escena['tipo']}", fill=(200,200,200), font=font_mini)
        
        # Guardar
        img.save(f"viral_frames/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1
    
    print(f"   ✅ {frame_count} frames totales")

print(f"\n📊 TOTAL: {frame_count} frames ({frame_count/FPS:.1f}s)")

# === GENERAR AUDIO ===
print("\n🎙️ Generando audio...")
audio_texto = "¿Cómo ahorrar 40 horas semanales? Tengo 20 documentos sin analizar. La solución es Claude más Google Drive. Un click y listo. Completamente gratis. Prueba ahora."

# Usar edge-tts
os.system(f"""python3 -c "
import sys
sys.path.insert(0, 'src')
from generate_voice import generate_voice
generate_voice('{audio_texto}', 'viral_output/audio_viral.mp3', voice='es-ES-AlvaroNeural')
" 2>/dev/null""")

# Verificar duración audio
result = subprocess.run(
    "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 viral_output/audio_viral.mp3",
    shell=True, capture_output=True, text=True
)
audio_dur = float(result.stdout.strip()) if result.returncode == 0 else 16.0
print(f"⏱️  Audio: {audio_dur:.1f}s")

# === RENDERIZAR VIDEO ===
print("\n🎬 Renderizando video viral...")
cmd = f"ffmpeg -y -framerate {FPS} -i viral_frames/frame_%04d.jpg -i viral_output/audio_viral.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest viral_output/SHORT_VIRAL.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

# Limpiar
shutil.rmtree('viral_frames')

if os.path.exists('viral_output/SHORT_VIRAL.mp4'):
    size = os.path.getsize('viral_output/SHORT_VIRAL.mp4') / (1024*1024)
    print(f"\n" + "="*60)
    print("✅ SHORT VIRAL COMPLETADO")
    print("="*60)
    print(f"📁 viral_output/SHORT_VIRAL.mp4")
    print(f"💾 {size:.1f} MB")
    print(f"⏱️  ~{frame_count/FPS:.1f} segundos")
    print(f"⚡ 5 escenas con efectos")
    print(f"🎨 Zoom, shake, slide, pulse, bounce")
    print("="*60)
else:
    print("❌ Error:", result.stderr[:300])
