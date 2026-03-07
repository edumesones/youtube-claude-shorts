#!/usr/bin/env python3
"""
GENERADOR FINAL - Video profesional Claude Code + Google Drive
Tutorial completo con pantallas reales + animaciones + voz
Nivel: BÁSICO (sin código técnico)
"""
import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, 'src')
from generate_voice import generate_voice

# Crear directorios
Path('output').mkdir(exist_ok=True)
Path('assets/frames').mkdir(parents=True, exist_ok=True)

# SCRIPT COMPLETO (45 segundos) - Tutorial + Demo + Resultados
SCRIPT = """
[SEGMENTO 1 - 0:00-0:05] HOOK
Imagina poder hablar con todos tus documentos como si fueran personas. 
Hoy te muestro cómo conectar Google Drive con Claude Code.

[SEGMENTO 2 - 0:05-0:15] PROBLEMA
Tienes cientos de PDFs, informes y contratos. Leerlos todos llevaría días. 
¿Y si pudieras preguntarles directamente qué dicen?

[SEGMENTO 3 - 0:15-0:28] SOLUCIÓN
Con Claude Code conectado a Drive, es súper fácil. Solo le dices: 
analiza mis documentos del último trimestre. Y en segundos, obtienes un resumen completo.

[SEGMENTO 4 - 0:28-0:40] RESULTADO
Claude extrajo tres insights clave: las ventas subieron un veintitrés por ciento, 
detectó tres contratos que expiran pronto, y recomendó enfocarse en el sector B2B 
donde el retorno de inversión es trescientos cuarenta por ciento.

[SEGMENTO 5 - 0:40-0:45] CTA
Todo esto en minutos, no en días. Prueba Claude Code y transforma cómo trabajas con documentos. 
¡Dale like y sígueme para más trucos!
"""

def crear_frame_gradiente(width=1080, height=1920, color1=(13, 17, 23), color2=(26, 26, 46)):
    """Crea fondo degradado."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img

def crear_icono_claude(draw, x, y, size=80):
    """Dibuja icono hexagonal de Claude."""
    # Hexágono naranja #E57035
    color = (229, 112, 53)
    points = []
    for i in range(6):
        angle = i * 60 - 30
        import math
        px = x + size * 0.8 * math.cos(math.radians(angle))
        py = y + size * 0.8 * math.sin(math.radians(angle))
        points.append((px, py))
    draw.polygon(points, fill=color, outline=color)
    # Letra C blanca
    draw.text((x-20, y-25), "C", fill=(255,255,255), font=None)

def crear_icono_drive(draw, x, y, size=60):
    """Dibuja icono de Drive."""
    # Triángulo azul #4285F4
    color = (66, 133, 244)
    draw.polygon([(x, y-size), (x-size, y+size//2), (x+size, y+size//2)], fill=color)

def crear_icono_pdf(draw, x, y, size=40):
    """Dibuja icono PDF."""
    color = (234, 67, 53)  # Rojo
    draw.rectangle([x-size, y-size*1.3, x+size, y+size], fill=color, outline=(180,50,40), width=2)
    draw.text((x-25, y-10), "PDF", fill=(255,255,255), font=None)

def crear_frame_tutorial(num_frame, segmento, total_frames):
    """Crea frames del tutorial con elementos visuales."""
    img = crear_frame_gradiente()
    draw = ImageDraw.Draw(img)
    
    # Fuente básica
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except:
        font_title = ImageFont.load_default()
        font_text = font_title
    
    # SEGMENTO 1: Hook - Iconos grandes
    if segmento == 1:
        crear_icono_drive(draw, 540, 500, 100)
        crear_icono_claude(draw, 540, 700, 120)
        draw.text((400, 900), "+", fill=(255,255,255), font=font_title)
        draw.text((200, 1000), "Habla con tus documentos", fill=(255,255,255), font=font_title)
    
    # SEGMENTO 2: Problema - Archivos
    elif segmento == 2:
        draw.text((300, 200), "📁 20+ documentos", fill=(200,200,200), font=font_title)
        y_pos = 350
        for i in range(5):
            crear_icono_pdf(draw, 200, y_pos + i*120, 35)
            draw.text((280, y_pos + i*120 - 15), f"informe_{i+1}.pdf", fill=(180,180,180), font=font_text)
        draw.text((250, 1000), "¿Días leyendo?", fill=(248,81,73), font=font_title)
    
    # SEGMENTO 3: Solución - Interfaz
    elif segmento == 3:
        # Caja de chat
        draw.rounded_rectangle([100, 400, 980, 800], radius=20, fill=(22, 27, 34), outline=(48,54,61), width=2)
        draw.text((150, 450), "Tú:", fill=(139,148,158), font=font_text)
        draw.text((150, 500), "Analiza mis documentos del", fill=(255,255,255), font=font_text)
        draw.text((150, 540), "último trimestre", fill=(255,255,255), font=font_text)
        
        # Respuesta de Claude
        draw.text((150, 650), "Claude:", fill=(229,112,53), font=font_text)
        draw.text((150, 700), "Analizando... ✓", fill=(63,185,80), font=font_text)
        
        crear_icono_claude(draw, 900, 700, 50)
    
    # SEGMENTO 4: Resultados - Tarjetas
    elif segmento == 4:
        tarjetas = [
            ("📈 VENTAS", "+23% crecimiento", (35,134,54)),
            ("⚠️ ALERTA", "3 contratos expiran", (248,81,73)),
            ("💡 TIP", "Enfocarse en B2B", (229,112,53))
        ]
        y_start = 300
        for i, (titulo, desc, color) in enumerate(tarjetas):
            y = y_start + i * 280
            # Borde izquierdo de color
            draw.rounded_rectangle([100, y, 980, y+200], radius=15, fill=(22,27,34))
            draw.rectangle([100, y, 115, y+200], fill=color)
            draw.text((150, y+30), titulo, fill=(255,255,255), font=font_title)
            draw.text((150, y+100), desc, fill=(201,209,217), font=font_text)
    
    # SEGMENTO 5: CTA
    else:
        draw.text((350, 600), "🚀 PRUEBA AHORA", fill=(229,112,53), font=font_title)
        # Botón
        draw.rounded_rectangle([340, 800, 740, 920], radius=50, fill=(255,255,255))
        draw.text((400, 840), "SUSCRIBIRSE", fill=(13,17,23), font=font_title)
        draw.text((300, 1100), "👍 Like  💬 Comenta  🔄 Comparte", fill=(139,148,158), font=font_text)
    
    return img

def main():
    print("=" * 60)
    print("🎬 GENERANDO VIDEO PROFESIONAL")
    print("Claude Code + Google Drive Tutorial")
    print("=" * 60)
    
    # 1. GENERAR VOZ
    print("\n🎙️ Generando voz profesional...")
    audio_path = "output/tutorial_voice.mp3"
    
    # Extraer solo el texto para TTS (sin marcas de segmento)
    texto_tts = SCRIPT.replace("[SEGMENTO 1 - 0:00-0:05] HOOK\n", "") \
                     .replace("[SEGMENTO 2 - 0:05-0:15] PROBLEMA\n", "") \
                     .replace("[SEGMENTO 3 - 0:15-0:28] SOLUCIÓN\n", "") \
                     .replace("[SEGMENTO 4 - 0:28-0:40] RESULTADO\n", "") \
                     .replace("[SEGMENTO 5 - 0:40-0:45] CTA\n", "") \
                     .strip()
    
    if not generate_voice(texto_tts, audio_path, voice='es-ES-AlvaroNeural'):
        print("❌ Falló voz")
        return False
    
    # Obtener duración
    result = subprocess.run(
        f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_path}",
        shell=True, capture_output=True, text=True
    )
    duration = float(result.stdout.strip()) if result.returncode == 0 else 45.0
    print(f"   ✅ Audio: {duration:.1f} segundos")
    
    # 2. GENERAR FRAMES
    print("\n🎨 Generando frames animados...")
    fps = 30
    total_frames = int(duration * fps)
    
    # Distribución de segmentos
    segmentos = [
        (0, int(5 * fps), 1),      # 0-5s: Hook
        (int(5 * fps), int(15 * fps), 2),   # 5-15s: Problema
        (int(15 * fps), int(28 * fps), 3),  # 15-28s: Solución
        (int(28 * fps), int(40 * fps), 4),  # 28-40s: Resultados
        (int(40 * fps), total_frames, 5),   # 40-45s: CTA
    ]
    
    frame_files = []
    for i in range(total_frames):
        # Determinar segmento actual
        seg_num = 1
        for start, end, seg in segmentos:
            if start <= i < end:
                seg_num = seg
                break
        
        # Crear frame
        frame = crear_frame_tutorial(i, seg_num, total_frames)
        frame_path = f"assets/frames/frame_{i:05d}.jpg"
        frame.save(frame_path, quality=90)
        frame_files.append(frame_path)
        
        if i % 30 == 0:
            print(f"   Frame {i}/{total_frames} (segmento {seg_num})")
    
    print(f"   ✅ {len(frame_files)} frames generados")
    
    # 3. RENDERIZAR VIDEO
    print("\n🎬 Renderizando video final...")
    video_path = "output/video_tutorial_profesional.mp4"
    
    cmd = f"""
    ffmpeg -y -framerate 30 -i assets/frames/frame_%05d.jpg -i {audio_path} \
    -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -shortest {video_path}
    """
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Limpiar frames temporales
    for f in frame_files:
        os.remove(f)
    
    if result.returncode == 0 and os.path.exists(video_path):
        size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"\n✅ VIDEO PROFESIONAL COMPLETADO")
        print(f"📁 {video_path}")
        print(f"💾 {size_mb:.1f} MB")
        print(f"⏱️  {duration:.1f} segundos")
        print(f"🎨 5 segmentos con animaciones")
        print(f"🎙️  Voz profesional en español")
        
        print("\n" + "=" * 60)
        print("CONTENIDO DEL VIDEO:")
        print("=" * 60)
        print("• Hook: Conectar Drive + Claude")
        print("• Problema: Muchos documentos")
        print("• Solución: Análisis automático")
        print("• Resultados: 3 insights clave")
        print("• CTA: Prueba ahora + Suscríbete")
        print("=" * 60)
        
        return True
    else:
        print(f"❌ Error: {result.stderr[:500]}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
