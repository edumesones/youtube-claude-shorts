#!/usr/bin/env python3
"""
Generador de video con VOZ CLONADA (ElevenLabs)
API key: [SE CREA UN SECRETO]
Voice ID: edus
"""
import os
import subprocess
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil

# === CONFIGURACIÓN ===
# La API key debe venir de variable de entorno para seguridad
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')
VOICE_ID = 'edus'
FONT_PATH = "fonts/Roboto-Bold.ttf"

Path('output').mkdir(exist_ok=True)
Path('frames_voice').mkdir(exist_ok=True)

def generar_voz_edus(texto, output_path):
    """Genera audio usando la voz clonada de Edu"""
    if not ELEVENLABS_API_KEY:
        print("❌ Error: ELEVENLABS_API_KEY no configurada")
        print("   Ejecuta: export ELEVENLABS_API_KEY='sk_...'")
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    print(f"🎙️ Generando voz con 'edus'...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"   ✅ Audio guardado: {output_path}")
        return True
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text[:200]}")
        return False

# === SCRIPT DEL VIDEO ===
SCRIPT_EDU = """Hoy te muestro cómo ahorrar 40 horas semanales con Claude Code y Google Drive. 
Tienes decenas de documentos sin analizar. 
La solución es un solo click. 
Obtén resultados como más ventas, alertas automáticas, y todo es completamente gratis. 
Prueba ahora y transforma tu workflow."""

# === GENERAR VOZ ===
print("="*60)
print("🎬 VIDEO CON VOZ EDU (ElevenLabs)")
print("="*60)

audio_path = "output/voz_edu.mp3"
if not generar_voz_edus(SCRIPT_EDU, audio_path):
    print("\n⚠️  Usando voz alternativa (edge-tts)...")
    from src.generate_voice import generate_voice
    generate_voice(SCRIPT_EDU, audio_path, voice='es-ES-AlvaroNeural')

# === GENERAR FRAMES ===
print("\n🎨 Generando frames...")

# Obtener duración del audio
result = subprocess.run(
    f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_path}",
    shell=True, capture_output=True, text=True
)
duracion_total = float(result.stdout.strip()) if result.returncode == 0 else 17.0
print(f"⏱️  Duración audio: {duracion_total:.1f}s")

# Segmentos proporcionales a la duración real
SEGMENTOS = [
    ('AHORRA', '40h', 'horas semanales', (230,100,30)),
    ('PROBLEMA', '20+', 'documentos', (200,60,60)),
    ('SOLUCIÓN', '1', 'solo click', (50,150,50)),
    ('RESULTADOS', '+23%', 'más ventas', (50,100,200)),
    ('GRATIS', '$0', 'prueba ya', (230,100,30)),
]

segundos_por_seg = duracion_total / 5
fps = 30
frames_por_seg = int(segundos_por_seg * fps)

print(f"📊 Cada segmento: {segundos_por_seg:.1f}s ({frames_por_seg} frames)")

frame_count = 0
for num, (titulo, numero, sub, color) in enumerate(SEGMENTOS, 1):
    for f in range(frames_por_seg):
        img = Image.new('RGB', (1080, 1920), (253,253,247))
        draw = ImageDraw.Draw(img)
        
        try:
            font_titulo = ImageFont.truetype(FONT_PATH, 130)
            font_numero = ImageFont.truetype(FONT_PATH, 220)
            font_sub = ImageFont.truetype(FONT_PATH, 60)
            font_badge = ImageFont.truetype(FONT_PATH, 45)
        except:
            font_titulo = font_numero = font_sub = font_badge = ImageFont.load_default()
        
        # Header
        draw.rounded_rectangle([30, 30, 130, 100], radius=15, fill=color)
        draw.text((45, 40), f"0{num}", fill=(255,255,255), font=font_sub)
        
        # Título
        bbox = draw.textbbox((0,0), titulo, font=font_titulo)
        w = bbox[2] - bbox[0]
        x = (1080 - w) // 2
        draw.text((x, 180), titulo, fill=(13,13,13), font=font_titulo)
        
        # Número en caja
        box_y = 420
        draw.rounded_rectangle([120, box_y, 960, box_y+280], radius=30, fill=color)
        bbox = draw.textbbox((0,0), numero, font=font_numero)
        w = bbox[2] - bbox[0]
        x = (1080 - w) // 2
        y = box_y + (280 - (bbox[3]-bbox[1]))//2 - 20
        draw.text((x, y), numero, fill=(255,255,255), font=font_numero)
        
        # Subtítulo
        bbox = draw.textbbox((0,0), sub, font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text(((1080-w)//2, 730), sub, fill=(100,100,100), font=font_sub)
        
        # Badges (3)
        badges = [['Auto', 'Rápido', 'Fácil'], ['PDFs', 'Excels', 'Word'], ['Conectar', 'Analizar', 'Listo'], ['Datos', 'Alertas', 'Tips'], ['Prueba', 'Suscríbete', 'Like']][num-1]
        y_badge = 850
        for i, badge in enumerate(badges):
            x = 90 + (i * 340)
            draw.rounded_rectangle([x, y_badge, x+300, y_badge+80], radius=15, fill=color)
            bbox = draw.textbbox((0,0), badge, font=font_badge)
            w = bbox[2] - bbox[0]
            draw.text((x + (300-w)//2, y_badge+20), badge, fill=(255,255,255), font=font_badge)
        
        # Stats extras
        stats = ['⚡ Ahorra tiempo', '💰 Reduce costos', '✓ Mejora ROI']
        for i, stat in enumerate(stats):
            draw.text((100, 1000 + i*70), stat, fill=(80,80,80), font=font_sub)
        
        # Footer
        draw.text((80, 1200), "Claude + Drive", fill=color, font=font_sub)
        draw.rounded_rectangle([350, 1350, 730, 1450], radius=25, fill=(13,13,13))
        bbox = draw.textbbox((0,0), "EMPEZAR", font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text((350 + (380-w)//2, 1370), "EMPEZAR", fill=(255,255,255), font=font_sub)
        
        img.save(f"frames_voice/frame_{frame_count:04d}.jpg", quality=95)
        frame_count += 1

print(f"✅ {frame_count} frames generados")

# === RENDERIZAR ===
print("\n🎬 Renderizando video final...")
cmd = f"ffmpeg -y -framerate {fps} -i frames_voice/frame_%04d.jpg -i {audio_path} -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output/VIDEO_VOZ_EDU.mp4"
result = subprocess.run(cmd, shell=True, capture_output=True)

shutil.rmtree('frames_voice')

if os.path.exists('output/VIDEO_VOZ_EDU.mp4'):
    size = os.path.getsize('output/VIDEO_VOZ_EDU.mp4') / (1024*1024)
    print(f"\n" + "="*60)
    print("✅ VIDEO CON VOZ EDU LISTO")
    print("="*60)
    print(f"📁 output/VIDEO_VOZ_EDU.mp4")
    print(f"💾 {size:.1f} MB")
    print(f"🎙️  Voz: edus (ElevenLabs)")
    print(f"⏱️  {duracion_total:.1f} segundos")
    print("="*60)
else:
    print("❌ Error al renderizar")
    print(result.stderr[:300])
